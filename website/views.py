from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import *
from .forms import *
import json

def home(request):
    """Home page view"""
    site_settings = SiteSetting.objects.first()
    
    # Get featured content
    featured_services = Service.objects.filter(is_active=True)[:3]
    featured_blog = BlogPost.objects.filter(is_featured=True, is_published=True)[:3]
    testimonials = Testimonial.objects.filter(is_approved=True, is_featured=True)[:5]
    upcoming_events = Event.objects.filter(
        is_published=True,
        start_date__gte=timezone.now()
    )[:3]
    counselors = Counselor.objects.filter(is_active=True)[:4]
    
    # Get FAQ for quick answers
    faqs = FAQ.objects.filter(is_active=True)[:4]
    
    context = {
        'site_settings': site_settings,
        'featured_services': featured_services,
        'featured_blog': featured_blog,
        'testimonials': testimonials,
        'upcoming_events': upcoming_events,
        'counselors': counselors,
        'faqs': faqs,
    }
    return render(request, 'home.html', context)

def about(request):
    """About us page"""
    site_settings = SiteSetting.objects.first()
    counselors = Counselor.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_approved=True)[:6]
    
    # Values from your overview
    values = [
        {'name': 'Empathy', 'icon': 'heart', 'description': 'We approach every individual with compassion and understanding.'},
        {'name': 'Confidentiality', 'icon': 'lock', 'description': 'Your privacy and trust are our top priorities.'},
        {'name': 'Respect', 'icon': 'handshake', 'description': 'We honor your unique experiences and perspective.'},
        {'name': 'Inclusivity', 'icon': 'users', 'description': 'All are welcome in a safe, judgment-free space.'},
        {'name': 'Evidence-based practice', 'icon': 'flask', 'description': 'Our methods are backed by clinical research.'},
        {'name': 'Community empowerment', 'icon': 'globe-africa', 'description': 'Building mentally healthy communities together.'},
    ]
    
    context = {
        'site_settings': site_settings,
        'counselors': counselors,
        'testimonials': testimonials,
        'values': values,
    }
    return render(request, 'about.html', context)

def services(request):
    """Services listing page"""
    site_settings = SiteSetting.objects.first()
    
    # Group services by type
    individual_services = Service.objects.filter(
        service_type='individual',
        is_active=True
    )
    group_services = Service.objects.filter(
        service_type='group',
        is_active=True
    )
    workshop_services = Service.objects.filter(
        service_type='workshop',
        is_active=True
    )
    outreach_services = Service.objects.filter(
        service_type='outreach',
        is_active=True
    )
    
    # Approaches from your overview
    approaches = [
        {'name': 'Cognitive-Behavioral Therapy (CBT)', 'description': 'Identify and change negative thought patterns.'},
        {'name': 'Mindfulness & Relaxation', 'description': 'Techniques to reduce stress and increase present-moment awareness.'},
        {'name': 'Strength-based counseling', 'description': 'Focus on your inherent strengths and resilience.'},
        {'name': 'Solution-focused strategies', 'description': 'Practical approaches to achieve your goals.'},
        {'name': 'Narrative therapy', 'description': 'Re-author your life story in empowering ways.'},
        {'name': 'Emotional regulation coaching', 'description': 'Tools to understand and manage emotions effectively.'},
    ]
    
    context = {
        'site_settings': site_settings,
        'individual_services': individual_services,
        'group_services': group_services,
        'workshop_services': workshop_services,
        'outreach_services': outreach_services,
        'approaches': approaches,
    }
    return render(request, 'services.html', context)

def service_detail(request, service_id):
    """Individual service detail page"""
    service = get_object_or_404(Service, id=service_id, is_active=True)
    site_settings = SiteSetting.objects.first()
    related_services = Service.objects.filter(
        service_type=service.service_type,
        is_active=True
    ).exclude(id=service.id)[:3]
    
    context = {
        'site_settings': site_settings,
        'service': service,
        'related_services': related_services,
    }
    return render(request, 'service_detail.html', context)

def blog_list(request):
    """Blog listing page with pagination and filters"""
    site_settings = SiteSetting.objects.first()
    
    # Get all published blog posts
    blog_posts = BlogPost.objects.filter(is_published=True)
    
    # Filter by category if specified
    category = request.GET.get('category')
    if category:
        blog_posts = blog_posts.filter(category=category)
    
    # Filter by tag if specified
    tag = request.GET.get('tag')
    if tag:
        blog_posts = blog_posts.filter(tags__icontains=tag)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        blog_posts = blog_posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(blog_posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories with counts
    categories = BlogPost.objects.filter(is_published=True).values('category').annotate(
        count=Count('category')
    ).order_by('-count')
    
    # Get popular tags
    all_tags = BlogPost.objects.filter(is_published=True).values_list('tags', flat=True)
    tag_list = []
    for tags in all_tags:
        if tags:
            tag_list.extend([tag.strip() for tag in tags.split(',')])
    
    # Count tag frequency
    from collections import Counter
    tag_frequency = Counter(tag_list).most_common(10)
    
    context = {
        'site_settings': site_settings,
        'page_obj': page_obj,
        'categories': categories,
        'tag_frequency': tag_frequency,
        'current_category': category,
        'current_tag': tag,
        'search_query': query,
    }
    return render(request, 'blog_list.html', context)

def blog_detail(request, slug):
    """Individual blog post page"""
    blog_post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    site_settings = SiteSetting.objects.first()
    
    # Increment view count
    blog_post.views_count += 1
    blog_post.save(update_fields=['views_count'])
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        category=blog_post.category,
        is_published=True
    ).exclude(id=blog_post.id)[:3]
    
    context = {
        'site_settings': site_settings,
        'blog_post': blog_post,
        'related_posts': related_posts,
    }
    return render(request, 'blog_detail.html', context)

def blog_category(request, category):
    """Filter blog posts by category"""
    site_settings = SiteSetting.objects.first()
    blog_posts = BlogPost.objects.filter(
        category=category,
        is_published=True
    )
    
    paginator = Paginator(blog_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'site_settings': site_settings,
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, 'blog_category.html', context)

def contact(request):
    """Contact page with form"""
    site_settings = SiteSetting.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            contact_message = form.save()
            
            # Send email notification
            try:
                subject = f"New Contact Message: {contact_message.subject}"
                message = render_to_string('emails/contact_notification.txt', {
                    'name': contact_message.name,
                    'email': contact_message.email,
                    'phone': contact_message.phone,
                    'subject': contact_message.subject,
                    'message': contact_message.message,
                })
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [site_settings.email] if site_settings else [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                
                # Send auto-reply to user
                auto_reply_subject = "Thank you for contacting Suzstar Counseling"
                auto_reply_message = render_to_string('emails/contact_autoreply.txt', {
                    'name': contact_message.name,
                })
                send_mail(
                    auto_reply_subject,
                    auto_reply_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_message.email],
                    fail_silently=False,
                )
            except:
                # Log error but don't break the user experience
                pass
            
            messages.success(request, 'Thank you for your message. We will get back to you soon!')
            return redirect('website:contact')
    else:
        form = ContactForm()
    
    context = {
        'site_settings': site_settings,
        'form': form,
    }
    return render(request, 'contact.html', context)

def book_appointment(request):
    """Appointment booking page"""
    site_settings = SiteSetting.objects.first()
    counselors = Counselor.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            
            # Send confirmation email
            try:
                subject = "Appointment Request Received - Suzstar Counseling"
                message = render_to_string('emails/appointment_confirmation.txt', {
                    'name': appointment.name,
                    'date': appointment.preferred_date,
                    'time': appointment.preferred_time,
                    'appointment_type': appointment.get_appointment_type_display(),
                })
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [appointment.email],
                    fail_silently=False,
                )
                
                # Notify admin
                admin_subject = f"New Appointment Booking: {appointment.name}"
                admin_message = render_to_string('emails/admin_appointment_notification.txt', {
                    'appointment': appointment,
                })
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [site_settings.email] if site_settings else [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except:
                pass
            
            messages.success(request, 'Your appointment request has been submitted successfully!')
            return redirect('website:appointment_success', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    
    context = {
        'site_settings': site_settings,
        'form': form,
        'counselors': counselors,
    }
    return render(request, 'book_appointment.html', context)

def appointment_success(request, appointment_id):
    """Appointment booking success page"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    site_settings = SiteSetting.objects.first()
    
    context = {
        'site_settings': site_settings,
        'appointment': appointment,
    }
    return render(request, 'appointment_success.html', context)

def resources(request):
    """Resources listing page"""
    site_settings = SiteSetting.objects.first()
    
    # Get all resources
    resources_list = Resource.objects.all()
    
    # Filter by type
    resource_type = request.GET.get('type')
    if resource_type:
        resources_list = resources_list.filter(resource_type=resource_type)
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        resources_list = resources_list.filter(category=category)
    
    # Search
    query = request.GET.get('q')
    if query:
        resources_list = resources_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    
    paginator = Paginator(resources_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique categories
    categories = Resource.objects.values_list('category', flat=True).distinct()
    
    context = {
        'site_settings': site_settings,
        'page_obj': page_obj,
        'categories': categories,
        'current_type': resource_type,
        'current_category': category,
        'search_query': query,
    }
    return render(request, 'resources.html', context)

def resource_detail(request, resource_id):
    """Individual resource detail page"""
    resource = get_object_or_404(Resource, id=resource_id)
    site_settings = SiteSetting.objects.first()
    
    context = {
        'site_settings': site_settings,
        'resource': resource,
    }
    return render(request, 'resource_detail.html', context)

def download_resource(request, resource_id):
    """Handle resource downloads"""
    resource = get_object_or_404(Resource, id=resource_id)
    
    if resource.file_upload:
        # Increment download count
        resource.downloads_count += 1
        resource.save(update_fields=['downloads_count'])
        
        # Serve the file
        response = HttpResponse(resource.file_upload, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{resource.file_upload.name}"'
        return response
    
    messages.error(request, 'This resource is not available for download.')
    return redirect('website:resource_detail', resource_id=resource.id)

def events(request):
    """Events listing page"""
    site_settings = SiteSetting.objects.first()
    
    # Get upcoming events
    upcoming_events = Event.objects.filter(
        is_published=True,
        start_date__gte=timezone.now()
    )
    
    # Get past events
    past_events = Event.objects.filter(
        is_published=True,
        start_date__lt=timezone.now()
    )[:6]
    
    # Filter by type
    event_type = request.GET.get('type')
    if event_type:
        upcoming_events = upcoming_events.filter(event_type=event_type)
    
    context = {
        'site_settings': site_settings,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'current_type': event_type,
    }
    return render(request, 'events.html', context)

def event_detail(request, event_id):
    """Individual event detail page"""
    event = get_object_or_404(Event, id=event_id, is_published=True)
    site_settings = SiteSetting.objects.first()
    
    context = {
        'site_settings': site_settings,
        'event': event,
    }
    return render(request, 'event_detail.html', context)

def event_register(request, event_id):
    """Handle event registration"""
    event = get_object_or_404(Event, id=event_id, is_published=True)
    
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            # Check if event is full
            if event.is_full:
                messages.error(request, 'Sorry, this event is already full.')
                return redirect('website:event_detail', event_id=event.id)
            
            # Create registration
            registration = form.save(commit=False)
            registration.event = event
            registration.save()
            
            # Update participant count
            event.current_participants += 1
            event.save(update_fields=['current_participants'])
            
            # Send confirmation email
            try:
                subject = f"Registration Confirmation: {event.title}"
                message = render_to_string('emails/event_registration.txt', {
                    'name': registration.name,
                    'event': event,
                })
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [registration.email],
                    fail_silently=False,
                )
            except:
                pass
            
            messages.success(request, 'You have successfully registered for this event!')
            return redirect('website:event_detail', event_id=event.id)
    else:
        form = EventRegistrationForm()
    
    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'event_register.html', context)

def faq(request):
    """Frequently Asked Questions page"""
    site_settings = SiteSetting.objects.first()
    
    # Group FAQs by category
    categories = FAQ.objects.filter(is_active=True).values_list('category', flat=True).distinct()
    
    faqs_by_category = {}
    for category in categories:
        faqs_by_category[category] = FAQ.objects.filter(
            category=category,
            is_active=True
        )
    
    context = {
        'site_settings': site_settings,
        'faqs_by_category': faqs_by_category,
    }
    return render(request, 'faq.html', context)

def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data.get('first_name', '')
            
            # Check if already subscribed
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name, 'is_active': True}
            )
            
            if not created and not subscriber.is_active:
                subscriber.is_active = True
                subscriber.first_name = first_name or subscriber.first_name
                subscriber.save()
            
            # Send welcome email
            try:
                subject = "Welcome to Suzstar Counseling Newsletter"
                message = render_to_string('emails/newsletter_welcome.txt', {
                    'first_name': first_name or 'there',
                })
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            except:
                pass
            
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    return redirect(request.META.get('HTTP_REFERER', 'website:home'))

def newsletter_unsubscribe(request, email):
    """Handle newsletter unsubscription"""
    try:
        subscriber = NewsletterSubscriber.objects.get(email=email)
        subscriber.is_active = False
        subscriber.unsubscribed_date = timezone.now()
        subscriber.save()
        messages.success(request, 'You have been unsubscribed from our newsletter.')
    except NewsletterSubscriber.DoesNotExist:
        messages.error(request, 'Email not found in our subscription list.')
    
    return redirect('website:home')

def counselors(request):
    """Counselors listing page"""
    site_settings = SiteSetting.objects.first()
    counselors_list = Counselor.objects.filter(is_active=True)
    
    context = {
        'site_settings': site_settings,
        'counselors': counselors_list,
    }
    return render(request, 'counselors.html', context)

def counselor_detail(request, counselor_id):
    """Individual counselor detail page"""
    counselor = get_object_or_404(Counselor, id=counselor_id, is_active=True)
    site_settings = SiteSetting.objects.first()
    
    context = {
        'site_settings': site_settings,
        'counselor': counselor,
    }
    return render(request, 'counselor_detail.html', context)

def testimonials(request):
    """Testimonials listing page"""
    site_settings = SiteSetting.objects.first()
    testimonials_list = Testimonial.objects.filter(is_approved=True)
    
    paginator = Paginator(testimonials_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'site_settings': site_settings,
        'page_obj': page_obj,
    }
    return render(request, 'testimonials.html', context)

def search(request):
    """Global search functionality"""
    site_settings = SiteSetting.objects.first()
    query = request.GET.get('q', '')
    
    results = {
        'services': [],
        'blog': [],
        'resources': [],
        'events': [],
        'faqs': [],
    }
    
    if query and len(query) >= 3:
        # Search services
        results['services'] = Service.objects.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query),
            is_active=True
        )[:5]
        
        # Search blog
        results['blog'] = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query),
            is_published=True
        )[:5]
        
        # Search resources
        results['resources'] = Resource.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )[:5]
        
        # Search events
        results['events'] = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query),
            is_published=True,
            start_date__gte=timezone.now()
        )[:5]
        
        # Search FAQ
        results['faqs'] = FAQ.objects.filter(
            Q(question__icontains=query) |
            Q(answer__icontains=query),
            is_active=True
        )[:5]
    
    context = {
        'site_settings': site_settings,
        'query': query,
        'results': results,
    }
    return render(request, 'search.html', context)

# ADMIN DASHBOARD VIEWS (for custom admin pages if needed)
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import *

@login_required(login_url='/admin/login/')
@staff_member_required
def dashboard(request):
    """Main dashboard view - accessible only to staff members"""
    
    # Get statistics for dashboard
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    confirmed_appointments = Appointment.objects.filter(status='confirmed').count()
    completed_appointments = Appointment.objects.filter(status='completed').count()
    
    # Get recent appointments
    recent_appointments = Appointment.objects.all().order_by('-created_at')[:10]
    
    # Get blog stats
    total_blog_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(is_published=True).count()
    
    # Get contact messages
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    
    # Get subscribers
    total_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()
    
    # Get events
    upcoming_events = Event.objects.filter(
        start_date__gte=timezone.now(),
        is_published=True
    ).count()
    
    # Chart data (last 7 days)
    last_7_days = []
    appointments_data = []
    
    for i in range(6, -1, -1):
        date = timezone.now().date() - timedelta(days=i)
        last_7_days.append(date.strftime('%a'))
        count = Appointment.objects.filter(
            preferred_date=date
        ).count()
        appointments_data.append(count)
    
    # Service distribution
    service_types = Appointment.objects.values('appointment_type').annotate(
        count=Count('appointment_type')
    )
    
    context = {
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'completed_appointments': completed_appointments,
        'recent_appointments': recent_appointments,
        'total_blog_posts': total_blog_posts,
        'published_posts': published_posts,
        'unread_messages': unread_messages,
        'total_subscribers': total_subscribers,
        'upcoming_events': upcoming_events,
        'last_7_days': last_7_days,
        'appointments_data': appointments_data,
        'service_types': service_types,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

# Alternative: Simple dashboard without authentication (for testing)
def simple_dashboard(request):
    """Simple dashboard view for testing - NO AUTHENTICATION REQUIRED"""
    return render(request, 'dashboard/dashboard.html')