from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, DonorProfile, BloodBankProfile, BLOOD_GROUPS
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, DonorProfileSerializer, BloodBankRegisterSerializer, BloodBankProfileSerializer


# ─── API Views ───────────────────────────────────────────────
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Registration successful.',
            'user': UserSerializer(user).data,
            'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)},
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful.',
            'user': UserSerializer(user).data,
            'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)},
        })


class LogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass
        return Response({'message': 'Logged out successfully.'})


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class DonorListAPIView(generics.ListAPIView):
    serializer_class = DonorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show donors, exclude admin users
        qs = DonorProfile.objects.select_related('user').filter(user__role='donor')
        blood_group = self.request.query_params.get('blood_group')
        city = self.request.query_params.get('city')
        available = self.request.query_params.get('available')
        if blood_group:
            qs = qs.filter(blood_group=blood_group)
        if city:
            qs = qs.filter(city__icontains=city)
        if available == 'true':
            qs = qs.filter(is_available=True)
        return qs


class DonorProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = DonorProfileSerializer

    def get_object(self):
        return self.request.user.donor_profile


class BloodBankRegisterAPIView(generics.CreateAPIView):
    serializer_class = BloodBankRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Blood Bank registration successful. Waiting for admin verification.',
            'user': UserSerializer(user).data,
            'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)},
        }, status=status.HTTP_201_CREATED)


class BloodBankProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = BloodBankProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.blood_bank_profile


# ─── Template Views ───────────────────────────────────────────
def registration_choice_view(request):
    """Show registration type selection page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/registration_choice.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        data = request.POST
        errors = {}
        if CustomUser.objects.filter(username=data.get('username')).exists():
            errors['username'] = 'Username already taken.'
        if CustomUser.objects.filter(email=data.get('email')).exists():
            errors['email'] = 'Email already registered.'
        if data.get('password') != data.get('confirm_password'):
            errors['password'] = 'Passwords do not match.'
        if len(data.get('password', '')) < 8:
            errors['password_len'] = 'Password must be at least 8 characters.'
        if errors:
            return render(request, 'accounts/register.html', {'errors': errors, 'blood_groups': BLOOD_GROUPS, 'form_data': data})
        user = CustomUser.objects.create_user(
            username=data['username'],
            email=data.get('email', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            password=data['password'],
            phone=data.get('phone', ''),
            role='donor',
        )
        DonorProfile.objects.create(user=user, blood_group=data.get('blood_group', 'A+'))
        login(request, user)
        messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
        return redirect('dashboard')
    return render(request, 'accounts/register.html', {'blood_groups': BLOOD_GROUPS})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'dashboard'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.email = request.POST.get('email', user.email)
        user.save()
        if user.is_donor():
            profile = user.donor_profile
            profile.blood_group = request.POST.get('blood_group', profile.blood_group)
            profile.city = request.POST.get('city', profile.city)
            profile.area = request.POST.get('area', profile.area)
            profile.address = request.POST.get('address', profile.address)
            profile.gender = request.POST.get('gender', profile.gender)
            profile.bio = request.POST.get('bio', profile.bio)
            profile.is_available = request.POST.get('is_available') == 'on'
            if 'date_of_birth' in request.POST and request.POST['date_of_birth']:
                profile.date_of_birth = request.POST['date_of_birth']
            if 'profile_photo' in request.FILES:
                profile.profile_photo = request.FILES['profile_photo']
            profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'blood_groups': BLOOD_GROUPS})


def blood_bank_register_view(request):
    """Blood Bank Registration View"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        data = request.POST
        errors = {}
        
        # Validation
        if CustomUser.objects.filter(username=data.get('username')).exists():
            errors['username'] = 'Username already taken.'
        if CustomUser.objects.filter(email=data.get('email')).exists():
            errors['email'] = 'Email already registered.'
        if BloodBankProfile.objects.filter(registration_number=data.get('registration_number')).exists():
            errors['registration_number'] = 'Blood Bank with this registration number already exists.'
        if data.get('password') != data.get('confirm_password'):
            errors['password'] = 'Passwords do not match.'
        if len(data.get('password', '')) < 8:
            errors['password_len'] = 'Password must be at least 8 characters.'
        
        if errors:
            return render(request, 'accounts/blood_bank_register.html', {'errors': errors, 'form_data': data})
        
        # Create user
        user = CustomUser.objects.create_user(
            username=data['username'],
            email=data.get('email', ''),
            password=data['password'],
            phone=data.get('contact_number', ''),
            role='blood_bank',
        )
        
        # Create blood bank profile
        BloodBankProfile.objects.create(
            user=user,
            bank_name=data.get('bank_name', ''),
            registration_number=data['registration_number'],
            contact_number=data.get('contact_number', ''),
            email=data.get('email', ''),
            location=data.get('location', ''),
            city=data.get('city', ''),
            address=data.get('address', ''),
            license_number=data.get('license_number', ''),
        )
        
        login(request, user)
        messages.success(request, 'Blood Bank account created! Waiting for admin verification.')
        return redirect('dashboard')
    
    return render(request, 'accounts/blood_bank_register.html')
