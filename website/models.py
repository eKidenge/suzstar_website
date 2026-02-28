from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.core.validators import EmailValidator, RegexValidator

# Phone number validator for Kenyan numbers
kenyan_phone_validator = RegexValidator(
    regex=r'^(\+254|0)[7][0-9]{8}$',
    message='Enter a valid Kenyan phone number (e.g., 0712345678 or +254712345678)'
)

class Service(models.Model):
    """Model for counseling services offered"""
    SERVICE_TYPES = [
        ('individual', 'Individual Counseling'),
        ('group', 'Group Therapy & Support Circles'),
        ('workshop', 'Psychoeducation Workshops'),
        ('outreach', 'Community Outreach & Awareness'),
    ]
    
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    short_description = models.CharField(max_length=255)
    description = RichTextField()
    icon_name = models.CharField(max_length=50, help_text="FontAwesome icon name (e.g., 'heart', 'users')")
    price_range = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., 45-60 minutes")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('service_detail', args=[str(self.id)])

class Counselor(models.Model):
    """Model for counselors/therapists"""
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, help_text="e.g., Licensed Professional Counselor")
    bio = RichTextField()
    #image = models.ImageField(upload_to='counselors/', blank=True, null=True)
    image = models.FileField(upload_to='counselors/', blank=True, null=True)
    specialties = models.CharField(max_length=500, help_text="Comma-separated list of specialties")
    languages = models.CharField(max_length=200, help_text="Languages spoken", default="English")
    experience_years = models.IntegerField(default=0)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.name
    
    def get_specialties_list(self):
        return [s.strip() for s in self.specialties.split(',')]

class BlogPost(models.Model):
    """Model for blog articles and mental health resources"""
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=300)
    author = models.CharField(max_length=200, default="Suzstar Counseling Team")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    excerpt = models.TextField(max_length=500, help_text="Brief summary for blog listings")
    content = RichTextField()
    category = models.CharField(max_length=100, choices=[
        ('anxiety', 'Anxiety & Stress'),
        ('depression', 'Depression & Mood'),
        ('relationships', 'Relationships'),
        ('self_care', 'Self-Care & Wellness'),
        ('trauma', 'Trauma & Recovery'),
        ('youth', 'Youth & Teen Support'),
        ('general', 'General Mental Health'),
    ])
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

class Appointment(models.Model):
    """Model for appointment bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    APPOINTMENT_TYPES = [
        ('individual', 'Individual Counseling'),
        ('group', 'Group Therapy'),
        ('workshop', 'Workshop'),
        ('consultation', 'Initial Consultation'),
    ]
    
    SESSION_MODES = [
        ('in_person', 'In-Person'),
        ('online_video', 'Online Video'),
        ('online_voice', 'Online Voice'),
        ('phone', 'Phone Call'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=15, validators=[kenyan_phone_validator])
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    appointment_type = models.CharField(max_length=50, choices=APPOINTMENT_TYPES)
    session_mode = models.CharField(max_length=50, choices=SESSION_MODES, default='online_video')
    counselor = models.ForeignKey(Counselor, on_delete=models.SET_NULL, null=True, blank=True)
    concerns = models.TextField(help_text="Briefly describe what you'd like support with")
    is_new_client = models.BooleanField(default=True, help_text="Is this your first time seeking counseling?")
    hear_about_us = models.CharField(max_length=200, blank=True, help_text="How did you hear about us?")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Admin notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-preferred_date', '-preferred_time']
        
    def __str__(self):
        return f"{self.name} - {self.preferred_date} {self.preferred_time}"

class ContactMessage(models.Model):
    """Model for contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.subject} - {self.name}"

class Resource(models.Model):
    """Model for mental health resources and guides"""
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('guide', 'Guide'),
        ('video', 'Video'),
        ('exercise', 'Exercise'),
        ('external', 'External Link'),
    ]
    
    title = models.CharField(max_length=300)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    description = models.TextField()
    content = RichTextField(blank=True, null=True)
    external_url = models.URLField(blank=True, null=True)
    file_upload = models.FileField(upload_to='resources/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    downloads_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    """Model for client testimonials"""
    client_name = models.CharField(max_length=200)
    client_initials = models.CharField(max_length=10, help_text="e.g., 'M.K.' for privacy")
    location = models.CharField(max_length=100, blank=True)
    testimonial = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    service_received = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.client_initials} - {self.rating} stars"

class FAQ(models.Model):
    """Model for frequently asked questions"""
    question = models.CharField(max_length=500)
    answer = RichTextField()
    category = models.CharField(max_length=100, choices=[
        ('general', 'General'),
        ('services', 'Services'),
        ('appointments', 'Appointments'),
        ('fees', 'Fees & Payment'),
        ('online', 'Online Counseling'),
        ('privacy', 'Privacy & Confidentiality'),
    ])
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'order']
        
    def __str__(self):
        return self.question

class Event(models.Model):
    """Model for community events and workshops"""
    title = models.CharField(max_length=300)
    event_type = models.CharField(max_length=100, choices=[
        ('workshop', 'Workshop'),
        ('support_group', 'Support Circle'),
        ('outreach', 'Community Outreach'),
        ('webinar', 'Webinar'),
    ])
    description = RichTextField()
    featured_image = models.ImageField(upload_to='events/', blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=500)
    is_online = models.BooleanField(default=False)
    online_link = models.URLField(blank=True, null=True)
    max_participants = models.IntegerField(default=0, help_text="0 for unlimited")
    current_participants = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_date']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event_detail', args=[str(self.id)])
    
    @property
    def is_full(self):
        return self.max_participants > 0 and self.current_participants >= self.max_participants
    
    @property
    def spots_left(self):
        if self.max_participants == 0:
            return "Unlimited"
        return self.max_participants - self.current_participants

class NewsletterSubscriber(models.Model):
    """Model for newsletter subscribers"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)
    unsubscribed_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-subscribed_date']
        
    def __str__(self):
        return self.email

class SiteSetting(models.Model):
    """Model for dynamic site settings"""
    site_name = models.CharField(max_length=200, default="Suzstar Counseling")
    tagline = models.CharField(max_length=500, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    primary_color = models.CharField(max_length=20, default="#4A90E2")
    secondary_color = models.CharField(max_length=20, default="#F5A623")
    
    # Contact Information
    phone = models.CharField(max_length=15, validators=[kenyan_phone_validator])
    whatsapp = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    address = models.TextField(blank=True)
    
    # Working Hours
    monday_friday = models.CharField(max_length=100, default="8am - 5pm")
    saturday = models.CharField(max_length=100, default="8am - 12pm")
    sunday = models.CharField(max_length=100, default="Closed / By appointment")
    
    # Social Media
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    
    # SEO
    meta_description = models.TextField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
        
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSetting.objects.exists():
            return
        super().save(*args, **kwargs)