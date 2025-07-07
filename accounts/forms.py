# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# ✅ نموذج إنشاء مستخدم جديد
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'phone',
            'email',
            'city',
            'district',
            'val_license',
            'role',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['full_name'].label = 'الاسم الكامل'
        self.fields['phone'].label = 'رقم الجوال'
        self.fields['email'].label = 'البريد الإلكتروني'
        self.fields['city'].label = 'المدينة'
        self.fields['district'].label = 'الحي'
        self.fields['val_license'].label = 'رقم الرخصة (اختياري)'
        self.fields['role'].label = 'الدور'
        self.fields['password1'].label = 'كلمة المرور'
        self.fields['password2'].label = 'تأكيد كلمة المرور'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# ✅ نموذج تسجيل دخول الأدمن
class AdminLoginForm(forms.Form):
    phone = forms.CharField(
        label="رقم الجوال",
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'أدخل رقم الجوال'
        })
    )

    password = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'أدخل كلمة المرور'
        })
    )

# ✅ نموذج تحديث بيانات المستخدم
class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'full_name', 'phone', 'email', 'city', 'district',
            'val_license', 'role', 'is_active'
        ]
        labels = {
            'full_name': 'الاسم الكامل',
            'phone': 'رقم الجوال',
            'email': 'البريد الإلكتروني',
            'city': 'المدينة',
            'district': 'الحي',
            'val_license': 'رخصة فال',
            'role': 'الدور',
            'is_active': 'الحالة',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# ✅ نموذج بسيط بديل لإنشاء مستخدم (اختياري)
class CustomUserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="كلمة المرور")

    class Meta:
        model = CustomUser
        fields = [
            'full_name', 'phone', 'email', 'city', 'district',
            'val_license', 'role', 'is_active', 'password'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
