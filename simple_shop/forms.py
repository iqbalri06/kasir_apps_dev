from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, UserChangeForm
from django.core.validators import EmailValidator
from .models import Product, Category, Role

User = get_user_model()

class UserForm(UserChangeForm):
    """Custom user form that allows changing username and doesn't require password"""
    # Enhanced email field with custom validation
    email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message="Masukkan alamat email yang valid.")],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'contoh@email.com',
            'autocomplete': 'email'
        })
    )
    
    # Username field with custom validation
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autocomplete': 'username'
        })
    )
    
    # Improved role field with better styling
    role = forms.ModelChoiceField(
        queryset=Role.objects.all().order_by('name'),  # Sort roles alphabetically
        required=True,
        empty_label="Pilih Role",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'data-placeholder': 'Pilih role pengguna'
        })
    )
    
    # Make password fields optional for user updates
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'autocomplete': 'new-password',
            'placeholder': 'Masukkan password baru'
        }),
        required=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'autocomplete': 'new-password',
            'placeholder': 'Konfirmasi password baru'
        }),
        strip=False,
        required=False,
        help_text="Masukkan password yang sama untuk verifikasi.",
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Depan'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Belakang'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the built-in password field from UserChangeForm
        if 'password' in self.fields:
            self.fields.pop('password')
            
    def clean_username(self):
        """Custom validation to check if username exists but exclude the current user"""
        username = self.cleaned_data.get('username')
        if self.instance and self.instance.pk:
            # If this is an existing user, allow them to keep their username
            if username == self.instance.username:
                return username
            # Only check for uniqueness if username is changed
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Username sudah digunakan. Silakan pilih username lain.")
        else:
            # For new users, always check for uniqueness
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Username sudah digunakan. Silakan pilih username lain.")
        return username
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        # If at least one password field is filled, validate both
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError(
                    "Kedua password tidak cocok.",
                    code="password_mismatch"
                )
            return password2
        # If both are empty during an update, just return None
        return None
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']  # Ensure username is updated
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = True  # Always set users as staff
        
        # Set password only if one was provided
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
            
        if commit:
            user.save()
            if self.cleaned_data.get('role'):
                user.role = self.cleaned_data['role']
                user.save()
        return user

# Keep UserCreationForm for new users
class AddUserForm(UserCreationForm):
    # Enhanced email field with custom validation
    email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message="Masukkan alamat email yang valid.")],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'contoh@email.com',
            'autocomplete': 'email'
        })
    )
    
    # Improved role field with better styling
    role = forms.ModelChoiceField(
        queryset=Role.objects.all().order_by('name'),  # Sort roles alphabetically
        required=True,
        empty_label="Pilih Role",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'data-placeholder': 'Pilih role pengguna'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'autocomplete': 'username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Depan'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Belakang'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = True  # Always set users as staff
            
        if commit:
            user.save()
            if self.cleaned_data.get('role'):
                user.role = self.cleaned_data['role']
                user.save()
        return user

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    def clean_price(self):
        """Clean price by removing all non-digits and ignoring decimals"""
        price = self.cleaned_data.get('price')
        if isinstance(price, str):
            # Split on decimal point (if any) and only use the integer part
            price = price.split('.')[0]
            # Remove any non-digit characters
            price = ''.join(filter(str.isdigit, price))
        # Handle numeric inputs (like floats) by truncating decimals
        elif isinstance(price, (int, float)):
            price = int(price)
        return int(price) if price else 0

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'inputmode': 'numeric',
                'pattern': '[0-9]*'
            }),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
