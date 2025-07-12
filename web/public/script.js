document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('email-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loadingSpinner = submitBtn.querySelector('.loading-spinner');
    const successMessage = document.getElementById('success-message');
    const errorMessage = document.getElementById('error-message');
    const emailInput = document.getElementById('email');

    // Hide messages initially
    function hideMessages() {
        successMessage.style.display = 'none';
        errorMessage.style.display = 'none';
    }

    // Show loading state
    function showLoading() {
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        loadingSpinner.style.display = 'block';
    }

    // Hide loading state
    function hideLoading() {
        submitBtn.disabled = false;
        btnText.style.display = 'block';
        loadingSpinner.style.display = 'none';
    }

    // Show success message
    function showSuccess() {
        hideMessages();
        successMessage.style.display = 'block';
        form.style.display = 'none';
        
        // Scroll to success message
        successMessage.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    }

    // Show error message
    function showError(message = 'Something went wrong. Please try again.') {
        hideMessages();
        errorMessage.querySelector('p').textContent = message;
        errorMessage.style.display = 'block';
        
        // Auto-hide error after 5 seconds
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000);
    }

    // Validate email format
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const email = emailInput.value.trim();
        
        // Client-side validation
        if (!email) {
            showError('Please enter your email address.');
            return;
        }
        
        if (!isValidEmail(email)) {
            showError('Please enter a valid email address.');
            return;
        }

        // Show loading state
        showLoading();
        hideMessages();

        try {
            console.log('Submitting email:', email);
            
            // Submit to backend
            const response = await fetch('/api/submit-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({ email: email })
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);

            if (!response.ok) {
                // Handle non-200 responses
                let errorMessage = 'Failed to subscribe. Please try again.';
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.error || errorMessage;
                    console.error('Server error:', errorData);
                } catch (jsonError) {
                    console.error('Failed to parse error response:', jsonError);
                    const textResponse = await response.text();
                    console.error('Error response text:', textResponse);
                }
                showError(errorMessage);
                return;
            }

            const data = await response.json();
            console.log('Success response:', data);

            // Success
            showSuccess();
            
            // Track successful submission (optional analytics)
            if (typeof gtag !== 'undefined') {
                gtag('event', 'email_signup', {
                    'event_category': 'engagement',
                    'event_label': 'strategic_intelligence'
                });
            }
        } catch (error) {
            console.error('Submission error:', error);
            
            // More specific error messages
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                showError('Unable to connect to server. Please check your internet connection.');
            } else if (error.name === 'SyntaxError') {
                showError('Server returned invalid response. Please try again.');
            } else {
                showError('Network error. Please check your connection and try again.');
            }
        } finally {
            hideLoading();
        }
    });

    // Real-time email validation feedback
    emailInput.addEventListener('input', function() {
        const email = this.value.trim();
        
        if (email && !isValidEmail(email)) {
            this.style.borderColor = '#e74c3c';
        } else {
            this.style.borderColor = '#e1e8ed';
        }
    });

    // Clear validation on focus
    emailInput.addEventListener('focus', function() {
        this.style.borderColor = '#667eea';
        hideMessages();
    });

    // Add smooth scroll to form when page loads
    window.addEventListener('load', function() {
        // Small delay to ensure everything is rendered
        setTimeout(() => {
            document.querySelector('.form-section').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }, 500);
    });
});