// Main JavaScript for Suzstar Counseling Website

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS (Animate on Scroll) if available
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: true,
            offset: 100
        });
    }
    
    // Navbar scroll effect
    handleNavbarScroll();
    
    // Smooth scroll for anchor links
    setupSmoothScroll();
    
    // Form validation
    setupFormValidation();
    
    // FAQ accordion
    setupFAQ();
    
    // Back to top button
    setupBackToTop();
    
    // Newsletter form handling
    setupNewsletterForm();
    
    // Appointment date picker restrictions
    setupDatePicker();
});

// Navbar scroll effect
function handleNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('shadow-sm');
            navbar.style.padding = '0.5rem 0';
        } else {
            navbar.classList.remove('shadow-sm');
            navbar.style.padding = '1rem 0';
        }
    });
}

// Smooth scroll for anchor links
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Form validation
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Phone number formatting for Kenyan numbers
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                if (value.startsWith('0')) {
                    value = '254' + value.slice(1);
                }
                if (value.length > 12) {
                    value = value.slice(0, 12);
                }
                e.target.value = '+' + value;
            }
        });
    });
}

// FAQ accordion
function setupFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        const icon = question?.querySelector('i');
        
        question?.addEventListener('click', function() {
            const isOpen = answer?.style.display === 'block';
            
            // Close all other FAQs
            faqItems.forEach(otherItem => {
                const otherAnswer = otherItem.querySelector('.faq-answer');
                const otherIcon = otherItem.querySelector('.faq-question i');
                if (otherAnswer && otherItem !== item) {
                    otherAnswer.style.display = 'none';
                    if (otherIcon) {
                        otherIcon.className = 'fas fa-chevron-down';
                    }
                }
            });
            
            // Toggle current FAQ
            if (answer) {
                answer.style.display = isOpen ? 'none' : 'block';
                if (icon) {
                    icon.className = isOpen ? 'fas fa-chevron-down' : 'fas fa-chevron-up';
                }
            }
        });
    });
}

// Back to top button
function setupBackToTop() {
    const button = document.createElement('button');
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    button.className = 'btn btn-primary back-to-top';
    button.style.cssText = `
        position: fixed;
        bottom: 100px;
        right: 30px;
        display: none;
        z-index: 99;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        padding: 0;
    `;
    
    document.body.appendChild(button);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            button.style.display = 'block';
        } else {
            button.style.display = 'none';
        }
    });
    
    button.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Newsletter form handling
function setupNewsletterForm() {
    const newsletterForm = document.querySelector('.newsletter-form');
    
    newsletterForm?.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const response = await fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        });
        
        if (response.ok) {
            showNotification('Thank you for subscribing!', 'success');
            this.reset();
        } else {
            showNotification('An error occurred. Please try again.', 'error');
        }
    });
}

// Appointment date picker restrictions
function setupDatePicker() {
    const dateInput = document.querySelector('input[type="date"]');
    
    if (dateInput) {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        dateInput.min = today;
        
        // Set maximum date to 3 months from now
        const maxDate = new Date();
        maxDate.setMonth(maxDate.getMonth() + 3);
        dateInput.max = maxDate.toISOString().split('T')[0];
        
        // Disable weekends if needed
        dateInput.addEventListener('input', function(e) {
            const date = new Date(e.target.value);
            const day = date.getDay();
            
            // Disable Sundays (day 0)
            if (day === 0) {
                alert('Appointments are not available on Sundays. Please select another day.');
                e.target.value = '';
            }
        });
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Loading spinner
function showSpinner() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    spinner.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 99999;
    `;
    document.body.appendChild(spinner);
    return spinner;
}

function hideSpinner(spinner) {
    if (spinner) {
        spinner.remove();
    }
}

// Search functionality
function setupSearch() {
    const searchInput = document.querySelector('#search-input');
    const searchResults = document.querySelector('#search-results');
    
    let timeout;
    searchInput?.addEventListener('input', function(e) {
        clearTimeout(timeout);
        const query = e.target.value;
        
        if (query.length < 3) {
            searchResults.innerHTML = '';
            return;
        }
        
        timeout = setTimeout(async () => {
            const response = await fetch(`/search/?q=${encodeURIComponent(query)}`);
            const html = await response.text();
            searchResults.innerHTML = html;
        }, 500);
    });
}

// Initialize tooltips
function setupTooltips() {
    const tooltips = document.querySelectorAll('[data-toggle="tooltip"]');
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    }
}

// Initialize popovers
function setupPopovers() {
    const popovers = document.querySelectorAll('[data-toggle="popover"]');
    if (typeof bootstrap !== 'undefined' && bootstrap.Popover) {
        popovers.forEach(popover => {
            new bootstrap.Popover(popover);
        });
    }
}

// Handle dynamic content loading
function setupDynamicLoading() {
    const loadMoreBtns = document.querySelectorAll('.load-more');
    
    loadMoreBtns.forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            
            const url = this.getAttribute('data-url');
            const spinner = showSpinner();
            
            try {
                const response = await fetch(url);
                const html = await response.text();
                
                const container = document.querySelector(this.getAttribute('data-container'));
                container.insertAdjacentHTML('beforeend', html);
                this.remove();
            } catch (error) {
                showNotification('Error loading content', 'error');
            } finally {
                hideSpinner(spinner);
            }
        });
    });
}

// Initialize all components
function init() {
    setupTooltips();
    setupPopovers();
    setupSearch();
    setupDynamicLoading();
}

// Run initialization
init();