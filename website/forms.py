from django import forms
from django.core.validators import EmailValidator
from .models import *
from django.utils import timezone

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0712345678'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What is this regarding?',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'How can we help you?',
                'rows': 5,
                'required': True
            }),
        }

class AppointmentForm(forms.ModelForm):
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': timezone.now().date().isoformat()
        })
    )
    
    preferred_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Appointment
        fields = [
            'name', 'email', 'phone', 'preferred_date', 'preferred_time',
            'appointment_type', 'session_mode', 'counselor', 'concerns',
            'is_new_client', 'hear_about_us'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0712345678'
            }),
            'appointment_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'session_mode': forms.Select(attrs={
                'class': 'form-select'
            }),
            'counselor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'concerns': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Please briefly describe what you\'d like support with...',
                'rows': 4
            }),
            'is_new_client': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hear_about_us': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Google, Friend, Social Media'
            }),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Add custom validation for Kenyan phone numbers
        if phone and not (phone.startswith('07') or phone.startswith('+2547')):
            raise forms.ValidationError('Please enter a valid Kenyan phone number (e.g., 0712345678 or +254712345678)')
        return phone

class NewsletterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address',
            'required': True
        })
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your first name (optional)'
        })
    )

class BlogSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search articles...'
        })
    )

class EventRegistrationForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0712345678'
        })
    )
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not (phone.startswith('07') or phone.startswith('+2547')):
            raise forms.ValidationError('Please enter a valid Kenyan phone number')
        return phone

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['client_name', 'client_initials', 'location', 'testimonial', 'rating', 'service_received']
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name (will not be published)'
            }),
            'client_initials': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., M.K.'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mombasa'
            }),
            'testimonial': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your experience with our services...',
                'rows': 5
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            'service_received': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def clean_client_initials(self):
        initials = self.cleaned_data.get('client_initials')
        if len(initials) > 10:
            raise forms.ValidationError('Initials must be 10 characters or less')
        return initials

class ResourceFilterForm(forms.Form):
    resource_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Resource.RESOURCE_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get unique categories
        categories = Resource.objects.values_list('category', flat=True).distinct()
        category_choices = [('', 'All Categories')] + [(cat, cat) for cat in categories if cat]
        self.fields['category'].choices = category_choices