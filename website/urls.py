from django.urls import path
from django.contrib.auth import views as auth_views  # Add this import
from . import views

app_name = 'website'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/category/<str:category>/', views.blog_category, name='blog_category'),
    
    # Contact & Appointments
    path('contact/', views.contact, name='contact'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('appointment-success/<int:appointment_id>/', views.appointment_success, name='appointment_success'),
    
    # Resources
    path('resources/', views.resources, name='resources'),
    path('resources/<int:resource_id>/', views.resource_detail, name='resource_detail'),
    path('resources/download/<int:resource_id>/', views.download_resource, name='download_resource'),
    
    # Events
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/register/', views.event_register, name='event_register'),
    
    # FAQ
    path('faq/', views.faq, name='faq'),
    
    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('newsletter/unsubscribe/<str:email>/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    
    # Counselor
    path('counselors/', views.counselors, name='counselors'),
    path('counselors/<int:counselor_id>/', views.counselor_detail, name='counselor_detail'),
    
    # Testimonials
    path('testimonials/', views.testimonials, name='testimonials'),
    
    # Search
    path('search/', views.search, name='search'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-test/', views.simple_dashboard, name='dashboard_test'),
    
    # Authentication URLs (move these to main urls.py instead)
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]