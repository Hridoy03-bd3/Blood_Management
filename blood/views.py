from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from .models import BloodBank, BloodInventory, BloodDonation, BloodRequest
from .serializers import BloodBankSerializer, BloodInventorySerializer, BloodDonationSerializer, BloodRequestSerializer
from accounts.models import DonorProfile, BLOOD_GROUPS, CustomUser


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# ─── API Views ────────────────────────────────────────────────
class BloodBankListCreateAPIView(generics.ListCreateAPIView):
    queryset = BloodBank.objects.filter(is_active=True)
    serializer_class = BloodBankSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class BloodBankDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer


class BloodInventoryAPIView(generics.ListCreateAPIView):
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blood_group', 'blood_bank']


class BloodDonationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BloodDonationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'blood_group']
    search_fields = ['donor__first_name', 'donor__last_name', 'blood_group']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return BloodDonation.objects.all()
        return BloodDonation.objects.filter(donor=user)

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user, blood_group=self.request.user.donor_profile.blood_group)


class BloodDonationDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = BloodDonationSerializer

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return BloodDonation.objects.all()
        return BloodDonation.objects.filter(donor=self.request.user)


class ApproveDonationAPIView(APIView):
    def post(self, request, pk):
        if not is_admin(request.user):
            return Response({'error': 'Admin access required'}, status=403)
        donation = get_object_or_404(BloodDonation, pk=pk)
        action = request.data.get('action')
        if action == 'approve':
            donation.status = 'approved'
            inv, _ = BloodInventory.objects.get_or_create(
                blood_bank=donation.blood_bank,
                blood_group=donation.blood_group,
                defaults={'units_available': 0}
            )
            inv.units_available += donation.units
            inv.save()
            profile = donation.donor.donor_profile
            profile.total_donations += 1
            profile.last_donation_date = donation.donation_date
            profile.save()
        elif action == 'reject':
            donation.status = 'rejected'
        donation.admin_remarks = request.data.get('remarks', '')
        donation.save()
        return Response({'message': f'Donation {donation.status}.', 'status': donation.status})


class BloodRequestListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BloodRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'blood_group', 'urgency']
    search_fields = ['patient_name', 'hospital_name', 'blood_group']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return BloodRequest.objects.all()
        return BloodRequest.objects.filter(requester=user)

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


class BloodRequestDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = BloodRequestSerializer

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return BloodRequest.objects.all()
        return BloodRequest.objects.filter(requester=self.request.user)


class ApproveRequestAPIView(APIView):
    def post(self, request, pk):
        if not is_admin(request.user):
            return Response({'error': 'Admin access required'}, status=403)
        blood_request = get_object_or_404(BloodRequest, pk=pk)
        action = request.data.get('action')
        if action in ['approve', 'reject', 'fulfill']:
            blood_request.status = action if action != 'fulfill' else 'fulfilled'
        blood_request.admin_remarks = request.data.get('remarks', '')
        blood_request.save()
        return Response({'message': f'Request {blood_request.status}.', 'status': blood_request.status})


class StatisticsAPIView(APIView):
    def get(self, request):
        if not is_admin(request.user):
            return Response({'error': 'Admin access required'}, status=403)
        total_donors = DonorProfile.objects.count()
        available_donors = DonorProfile.objects.filter(is_available=True).count()
        total_donations = BloodDonation.objects.count()
        pending_donations = BloodDonation.objects.filter(status='pending').count()
        total_requests = BloodRequest.objects.count()
        pending_requests = BloodRequest.objects.filter(status='pending').count()
        blood_by_group = {}
        for bg_code, _ in BLOOD_GROUPS:
            total = BloodInventory.objects.filter(blood_group=bg_code).aggregate(total=Sum('units_available'))['total'] or 0
            blood_by_group[bg_code] = total
        return Response({
            'total_donors': total_donors,
            'available_donors': available_donors,
            'total_donations': total_donations,
            'pending_donations': pending_donations,
            'total_requests': total_requests,
            'pending_requests': pending_requests,
            'blood_by_group': blood_by_group,
        })


class DonorSearchAPIView(generics.ListAPIView):
    from accounts.serializers import DonorProfileSerializer
    serializer_class = DonorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = DonorProfile.objects.select_related('user').filter(is_available=True)
        blood_group = self.request.query_params.get('blood_group')
        city = self.request.query_params.get('city')
        if blood_group:
            qs = qs.filter(blood_group=blood_group)
        if city:
            qs = qs.filter(city__icontains=city)
        return qs


# ─── Template Views ───────────────────────────────────────────
@login_required
@login_required
def dashboard_view(request):
    user = request.user
    if user.role == 'admin':
        total_donors = DonorProfile.objects.count()
        available_donors = DonorProfile.objects.filter(is_available=True).count()
        pending_donations = BloodDonation.objects.filter(status='pending').count()
        pending_requests = BloodRequest.objects.filter(status='pending').count()
        total_banks = BloodBank.objects.filter(is_active=True).count()
        blood_inventory = {}
        for bg_code, bg_label in BLOOD_GROUPS:
            total = BloodInventory.objects.filter(blood_group=bg_code).aggregate(total=Sum('units_available'))['total'] or 0
            blood_inventory[bg_label] = total
        recent_donations = BloodDonation.objects.order_by('-created_at')[:5]
        recent_requests = BloodRequest.objects.order_by('-created_at')[:5]
        ctx = {
            'total_donors': total_donors, 'available_donors': available_donors,
            'pending_donations': pending_donations, 'pending_requests': pending_requests,
            'total_banks': total_banks, 'blood_inventory': blood_inventory,
            'recent_donations': recent_donations, 'recent_requests': recent_requests,
        }
        return render(request, 'blood/admin_dashboard.html', ctx)
    elif user.role == 'blood_bank':
        try:
            bb_profile = user.blood_bank_profile
        except:
            from accounts.models import BloodBankProfile
            bb_profile = BloodBankProfile.objects.create(user=user, bank_name='Blood Bank', registration_number=user.username)
        
        # Get the blood bank record(s) for this blood bank profile
        try:
            blood_banks = BloodBank.objects.filter(name__icontains=bb_profile.bank_name)
        except:
            blood_banks = []
        
        # Get inventory for any blood banks managed by this user
        bb_inventory = BloodInventory.objects.filter(blood_bank__in=blood_banks)
        inventory_data = {}
        for bg_code, bg_label in BLOOD_GROUPS:
            total = bb_inventory.filter(blood_group=bg_code).aggregate(total=Sum('units_available'))['total'] or 0
            inventory_data[bg_label] = total
        
        ctx = {
            'bb_profile': bb_profile,
            'inventory': inventory_data,
            'total_units': sum(inventory_data.values()),
            'is_verified': bb_profile.is_verified,
        }
        return render(request, 'blood/blood_bank_dashboard.html', ctx)
    else:
        try:
            profile = user.donor_profile
        except:
            profile = DonorProfile.objects.create(user=user, blood_group='A+')
        donations = BloodDonation.objects.filter(donor=user).order_by('-created_at')[:5]
        requests = BloodRequest.objects.filter(requester=user).order_by('-created_at')[:5]
        blood_inventory = {}
        for bg_code, bg_label in BLOOD_GROUPS:
            total = BloodInventory.objects.filter(blood_group=bg_code).aggregate(total=Sum('units_available'))['total'] or 0
            blood_inventory[bg_label] = total
        ctx = {
            'profile': profile, 'donations': donations,
            'requests': requests, 'blood_inventory': blood_inventory,
        }
        return render(request, 'blood/donor_dashboard.html', ctx)


@login_required
def donation_create_view(request):
    if request.method == 'POST':
        blood_bank_id = request.POST.get('blood_bank')
        donation_date = request.POST.get('donation_date')
        units = int(request.POST.get('units', 1))
        notes = request.POST.get('notes', '')
        blood_bank = get_object_or_404(BloodBank, pk=blood_bank_id)
        profile = request.user.donor_profile
        BloodDonation.objects.create(
            donor=request.user,
            blood_bank=blood_bank,
            blood_group=profile.blood_group,
            units=units,
            donation_date=donation_date,
            notes=notes,
        )
        messages.success(request, 'Donation request submitted! Awaiting admin approval.')
        return redirect('dashboard')
    blood_banks = BloodBank.objects.filter(is_active=True)
    return render(request, 'blood/donation_form.html', {'blood_banks': blood_banks})


@login_required
def request_create_view(request):
    if request.method == 'POST':
        BloodRequest.objects.create(
            requester=request.user,
            blood_group=request.POST['blood_group'],
            units_needed=request.POST.get('units_needed', 1),
            patient_name=request.POST['patient_name'],
            hospital_name=request.POST['hospital_name'],
            hospital_city=request.POST.get('hospital_city', ''),
            contact_number=request.POST['contact_number'],
            urgency=request.POST.get('urgency', 'normal'),
            reason=request.POST.get('reason', ''),
            required_date=request.POST.get('required_date') or None,
        )
        messages.success(request, 'Blood request submitted successfully!')
        return redirect('dashboard')
    return render(request, 'blood/request_form.html', {'blood_groups': BLOOD_GROUPS})


@login_required
def donation_list_view(request):
    if request.user.role == 'admin':
        donations = BloodDonation.objects.select_related('donor', 'blood_bank').all()
        status_filter = request.GET.get('status')
        bg_filter = request.GET.get('blood_group')
        if status_filter:
            donations = donations.filter(status=status_filter)
        if bg_filter:
            donations = donations.filter(blood_group=bg_filter)
    else:
        donations = BloodDonation.objects.filter(donor=request.user)
    return render(request, 'blood/donation_list.html', {'donations': donations, 'blood_groups': BLOOD_GROUPS})


@login_required
def request_list_view(request):
    if request.user.role == 'admin':
        requests = BloodRequest.objects.select_related('requester').all()
        status_filter = request.GET.get('status')
        if status_filter:
            requests = requests.filter(status=status_filter)
    else:
        requests = BloodRequest.objects.filter(requester=request.user)
    return render(request, 'blood/request_list.html', {'requests': requests, 'blood_groups': BLOOD_GROUPS})


@login_required
def approve_donation_view(request, pk):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    donation = get_object_or_404(BloodDonation, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '')
        if action == 'approve':
            donation.status = 'approved'
            inv, _ = BloodInventory.objects.get_or_create(
                blood_bank=donation.blood_bank, blood_group=donation.blood_group,
                defaults={'units_available': 0}
            )
            inv.units_available += donation.units
            inv.save()
            profile = donation.donor.donor_profile
            profile.total_donations += 1
            profile.last_donation_date = donation.donation_date
            profile.save()
        elif action == 'reject':
            donation.status = 'rejected'
        donation.admin_remarks = remarks
        donation.save()
        messages.success(request, f'Donation {donation.status} successfully.')
        return redirect('donation_list')
    return render(request, 'blood/approve_donation.html', {'donation': donation})


@login_required
def approve_request_view(request, pk):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ['approve', 'reject', 'fulfill']:
            blood_request.status = 'fulfilled' if action == 'fulfill' else action
        blood_request.admin_remarks = request.POST.get('remarks', '')
        blood_request.save()
        messages.success(request, f'Request status updated to {blood_request.status}.')
        return redirect('request_list')
    return render(request, 'blood/approve_request.html', {'blood_request': blood_request})


@login_required
def blood_bank_list_view(request):
    banks = BloodBank.objects.filter(is_active=True)
    return render(request, 'blood/bank_list.html', {'banks': banks})


@login_required
def blood_bank_manage_view(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            BloodBank.objects.create(
                name=request.POST['name'], location=request.POST['location'],
                city=request.POST['city'], contact_number=request.POST['contact_number'],
                email=request.POST.get('email', ''),
            )
            messages.success(request, 'Blood bank added.')
        elif action == 'delete':
            BloodBank.objects.filter(pk=request.POST['bank_id']).update(is_active=False)
            messages.success(request, 'Blood bank removed.')
        return redirect('blood_bank_manage')
    banks = BloodBank.objects.all()
    return render(request, 'blood/bank_manage.html', {'banks': banks})


@login_required
def donor_list_view(request):
    # Only show donors, exclude admin users
    donors = DonorProfile.objects.select_related('user').filter(user__role='donor')
    blood_group = request.GET.get('blood_group')
    city = request.GET.get('city')
    available = request.GET.get('available')
    if blood_group:
        donors = donors.filter(blood_group=blood_group)
    if city:
        donors = donors.filter(city__icontains=city)
    if available:
        donors = donors.filter(is_available=True)
    return render(request, 'blood/donor_list.html', {
        'donors': donors, 'blood_groups': BLOOD_GROUPS,
        'selected_bg': blood_group, 'selected_city': city,
    })


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    blood_inventory = {}
    for bg_code, bg_label in BLOOD_GROUPS:
        total = BloodInventory.objects.filter(blood_group=bg_code).aggregate(total=Sum('units_available'))['total'] or 0
        blood_inventory[bg_label] = total
    return render(request, 'home.html', {'blood_inventory': blood_inventory})


# ─── Admin User Management Views ──────────────────────────────
@login_required
@login_required
def admin_user_management_view(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    users = CustomUser.objects.all().order_by('-date_joined')

    # Filters
    search = request.GET.get('search', '')
    role = request.GET.get('role', '')
    status = request.GET.get('status', '')

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    if role:
        users = users.filter(role=role)
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)

    ctx = {
        'users': users,
        'total_users': CustomUser.objects.count(),
        'admin_count': CustomUser.objects.filter(role='admin').count(),
        'donor_count': CustomUser.objects.filter(role='donor').count(),
        'active_count': CustomUser.objects.filter(is_active=True).count(),
    }
    return render(request, 'blood/admin_user_management.html', ctx)


@login_required
def admin_user_detail_view(request, pk):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    from accounts.models import DonorProfile
    viewed_user = get_object_or_404(CustomUser, pk=pk)
    donor_profile = None
    if viewed_user.role == 'donor':
        try:
            donor_profile = viewed_user.donor_profile
        except Exception:
            pass

    # Get donations and requests with proper error handling
    try:
        donations = BloodDonation.objects.filter(donor=viewed_user).order_by('-created_at')[:10]
    except Exception:
        donations = []
    
    try:
        blood_requests = BloodRequest.objects.filter(requester=viewed_user).order_by('-created_at')[:10]
    except Exception:
        blood_requests = []

    ctx = {
        'viewed_user': viewed_user,
        'donor_profile': donor_profile,
        'donations': donations,
        'blood_requests': blood_requests,
    }
    return render(request, 'blood/admin_user_detail.html', ctx)


@login_required
def admin_delete_user_view(request, pk):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=pk)
        if user == request.user:
            messages.error(request, 'You cannot delete your own account.')
        else:
            username = user.username
            user.delete()
            messages.success(request, f'User "{username}" has been permanently deleted.')
    return redirect('admin_user_management')


@login_required
def admin_toggle_user_view(request, pk):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=pk)
        if user == request.user:
            messages.error(request, 'You cannot deactivate your own account.')
        else:
            user.is_active = not user.is_active
            user.save()
            action = 'activated' if user.is_active else 'deactivated'
            messages.success(request, f'User "{user.username}" has been {action}.')
    return redirect(request.META.get('HTTP_REFERER', 'admin_user_management'))


@login_required
def admin_promote_user_view(request, pk):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=pk)
        if user == request.user:
            messages.error(request, 'You cannot change your own role.')
        else:
            if user.role == 'admin':
                user.role = 'donor'
                user.is_staff = False
                messages.success(request, f'"{user.username}" has been demoted to Donor.')
            else:
                user.role = 'admin'
                user.is_staff = True
                messages.success(request, f'"{user.username}" has been promoted to Admin.')
            user.save()
    return redirect(request.META.get('HTTP_REFERER', 'admin_user_management'))
