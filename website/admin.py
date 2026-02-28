from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import *

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'duration', 'is_active', 'order']
    list_filter = ['service_type', 'is_active']
    search_fields = ['name', 'short_description']
    list_editable = ['is_active', 'order']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'service_type', 'short_description', 'description')
        }),
        ('Details', {
            'fields': ('icon_name', 'price_range', 'duration')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'experience_years', 'is_active', 'order']
    list_filter = ['is_active', 'languages']
    search_fields = ['name', 'title', 'specialties']
    list_editable = ['is_active', 'order']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'title', 'email', 'image')
        }),
        ('Professional Details', {
            'fields': ('bio', 'specialties', 'languages', 'experience_years')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'published_date', 'is_featured', 'is_published', 'views_count']
    list_filter = ['category', 'is_featured', 'is_published', 'published_date']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published']
    date_hierarchy = 'published_date'
    fieldsets = (
        ('Blog Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image', 'tags')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_published', 'published_date')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user.get_full_name() or request.user.username
        super().save_model(request, obj, form, change)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'preferred_date', 'preferred_time', 'appointment_type', 'session_mode', 'counselor_name', 'status']
    list_filter = ['status', 'appointment_type', 'session_mode', 'preferred_date']
    search_fields = ['name', 'email', 'phone']
    list_editable = ['status']
    date_hierarchy = 'preferred_date'
    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'email', 'phone', 'is_new_client')
        }),
        ('Appointment Details', {
            'fields': ('preferred_date', 'preferred_time', 'appointment_type', 'session_mode', 'counselor')
        }),
        ('Additional Information', {
            'fields': ('concerns', 'hear_about_us')
        }),
        ('Admin', {
            'fields': ('status', 'notes')
        }),
    )
    
    def counselor_name(self, obj):
        return obj.counselor.name if obj.counselor else "Not assigned"
    counselor_name.short_description = 'Counselor'
    
    actions = ['mark_as_confirmed', 'mark_as_completed']
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark selected as confirmed"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected as completed"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read', 'is_replied']
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read', 'is_replied']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected as unread"

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'category', 'is_featured', 'downloads_count', 'created_at']
    list_filter = ['resource_type', 'category', 'is_featured']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    fieldsets = (
        ('Resource Information', {
            'fields': ('title', 'resource_type', 'category', 'description')
        }),
        ('Content', {
            'fields': ('content', 'external_url', 'file_upload')
        }),
        ('Settings', {
            'fields': ('is_featured',)
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_initials', 'rating', 'service_received', 'is_featured', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_approved']
    search_fields = ['client_name', 'testimonial']
    list_editable = ['is_featured', 'is_approved']
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_initials', 'location')
        }),
        ('Testimonial', {
            'fields': ('testimonial', 'rating', 'service_received')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_approved')
        }),
    )

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'category', 'order', 'is_active')
        }),
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_date', 'location', 'is_online', 'spots_available', 'is_published']
    list_filter = ['event_type', 'is_online', 'is_published', 'start_date']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_published']
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'event_type', 'description', 'featured_image')
        }),
        ('Date & Location', {
            'fields': ('start_date', 'end_date', 'location', 'is_online', 'online_link')
        }),
        ('Capacity', {
            'fields': ('max_participants', 'current_participants', 'price')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_published')
        }),
    )
    
    def spots_available(self, obj):
        if obj.max_participants == 0:
            return "Unlimited"
        remaining = obj.max_participants - obj.current_participants
        return f"{remaining}/{obj.max_participants}"
    spots_available.short_description = "Spots Available"

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'is_active', 'subscribed_date']
    list_filter = ['is_active', 'subscribed_date']
    search_fields = ['email', 'first_name']
    list_editable = ['is_active']
    date_hierarchy = 'subscribed_date'
    
    actions = ['export_subscribers']
    
    def export_subscribers(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'First Name', 'Subscribed Date'])
        
        for subscriber in queryset:
            writer.writerow([subscriber.email, subscriber.first_name, subscriber.subscribed_date])
        
        return response
    export_subscribers.short_description = "Export selected subscribers"

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Prevent adding multiple instances
        return not SiteSetting.objects.exists()
    
    fieldsets = (
        ('Site Identity', {
            'fields': ('site_name', 'tagline', 'logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('phone', 'whatsapp', 'email', 'address')
        }),
        ('Working Hours', {
            'fields': ('monday_friday', 'saturday', 'sunday')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube')
        }),
        ('SEO & Analytics', {
            'fields': ('meta_description', 'meta_keywords', 'google_analytics_id')
        }),
    )