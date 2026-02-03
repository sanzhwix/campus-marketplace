from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.html import strip_tags
from django.core.validators import RegexValidator


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        max_length=70,
        widget=forms.EmailInput(attrs={
            'class': 'input-register form-control',
            'placeholder': 'Email'
        })
    )

    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'input-register form-control',
            'placeholder': 'First name'
        })
    )

    last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'input-register form-control',
            'placeholder': 'Last name'
        })
    )
    phone = forms.CharField(
            required=True,
            validators=[
                RegexValidator(
                    r'^\+?\d{9,15}$',
                    'Enter a valid phone number (9–15 digits).'
                )
            ],
            widget=forms.TextInput(attrs={
                'class': 'input-register form-control',
                'placeholder': '+77071234567'
            })
        )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-register form-control',
            'placeholder': 'Password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-register form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone',     
            'password1',
            'password2',
        )


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email
        email = email.strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # normalize email and set phone
        email = self.cleaned_data.get('email')
        if email:
            user.email = email.strip().lower()

        phone = self.cleaned_data.get('phone')
        if phone:
            user.phone = phone

        # Ensure password is set correctly (UserCreationForm already handles it,
        # but set explicitly from cleaned_data to be safe)
        raw_password = self.cleaned_data.get('password1')
        if raw_password:
            user.set_password(raw_password)

        if commit:
            user.save()
        return user

    

class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'input-register form-control',
            'placeholder': 'Email'
        })
    )

    

class CustomUserUpdateForm(forms.ModelForm):
    phone = forms.CharField(
        required=False,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        widget=forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'Phone'})
    )
    
    first_name=forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'First name'})
    )

    last_name=forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'Last name'})
    )

    email=forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input-regiter form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'Last name'}),
        }

    def clean_email(self):
        # Fix typo and ensure we validate against other users
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        # ensure email remains the same if user didn't provide one
        if not cleaned_data.get('email'):
            cleaned_data['email'] = self.instance.email

        # sanitize fields
        for field in ['phone']:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])

        return cleaned_data


