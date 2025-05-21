from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from allauth.socialaccount.models import SocialAccount
from .forms import CustomUserRegistrationForm  # Adjust import if needed

CustomUser = get_user_model()

def register(request):
    social_email = None
    is_social_user = False

    # Check if the user is already authenticated (possibly via Google)
    if request.user.is_authenticated:
        try:
            social_account = SocialAccount.objects.get(user=request.user)
            if social_account.provider == 'google':
                is_social_user = True
                social_email = request.user.email
        except SocialAccount.DoesNotExist:
            pass

        # Redirect if user is already fully registered
        if request.user.ruc and request.user.company and request.user.rol:
            return redirect('quotes:quotes_all')

    if request.method == 'POST':
        if request.user.is_authenticated:
            # Existing social-authenticated user completing registration
            form = CustomUserRegistrationForm(request.POST, instance=request.user, social_email=social_email)
        else:
            # New anonymous registration
            form = CustomUserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()  # ✅ Password now saved even for social-auth users without a password
            user.backend = 'users.backends.EmailBackend' 
            login(request, user)
            
            # if not request.user.is_authenticated:
            #     # Log in the newly registered (non-social) user
            #     raw_email = form.cleaned_data['email']
            #     raw_password = form.cleaned_data['password1']
            #     authenticated_user = authenticate(request, email=raw_email, password=raw_password)
            #     if authenticated_user:
            #         login(request, authenticated_user)
                  

                    
            return redirect('quotes:quotes_all')
        else:
            print(form.errors)  # Optional: use logging here for production

    else:
        # Handle GET request to show the registration form
        if request.user.is_authenticated:
            form = CustomUserRegistrationForm(instance=request.user, social_email=social_email)
        else:
            form = CustomUserRegistrationForm()

    return render(request, 'users/register.html', {
        'form': form,
        'is_social_registration': is_social_user
    })
