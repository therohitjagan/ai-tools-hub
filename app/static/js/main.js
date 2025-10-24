// Global utility functions

// Show toast notification
function showToast(message, type = 'info') {
    const toast = $(`
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `);
    
    $('.toast-container').append(toast);
    const bsToast = new bootstrap.Toast(toast[0]);
    bsToast.show();
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Add toast container to body if not exists
$(document).ready(function() {
    if ($('.toast-container').length === 0) {
        $('body').append('<div class="toast-container position-fixed top-0 end-0 p-3"></div>');
    }
});

// Smooth scroll
$('a[href^="#"]').on('click', function(e) {
    e.preventDefault();
    const target = $(this.getAttribute('href'));
    if (target.length) {
        $('html, body').stop().animate({
            scrollTop: target.offset().top - 100
        }, 1000);
    }
});

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return false;
    }
    return true;
}

// File size validation
function validateFileSize(file, maxSizeMB = 16) {
    const maxSize = maxSizeMB * 1024 * 1024; // Convert to bytes
    if (file.size > maxSize) {
        showToast(`File size exceeds ${maxSizeMB}MB limit`, 'danger');
        return false;
    }
    return true;
}

// Copy to clipboard helper
function copyToClipboard(text, successMessage = 'Copied to clipboard!') {
    navigator.clipboard.writeText(text).then(() => {
        showToast(successMessage, 'success');
    }).catch(err => {
        showToast('Failed to copy text', 'danger');
        console.error('Copy failed:', err);
    });
}

// Format time
function formatTime(seconds) {
    if (seconds < 1) {
        return `${(seconds * 1000).toFixed(0)}ms`;
    }
    return `${seconds.toFixed(2)}s`;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Loading state helper
function setLoadingState(buttonId, isLoading, loadingText = 'Processing...') {
    const button = $(`#${buttonId}`);
    if (isLoading) {
        button.prop('disabled', true);
        button.data('original-text', button.html());
        button.html(`
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            ${loadingText}
        `);
    } else {
        button.prop('disabled', false);
        button.html(button.data('original-text'));
    }
}

// Handle AJAX errors
function handleAjaxError(xhr, defaultMessage = 'An error occurred') {
    let errorMessage = defaultMessage;
    
    if (xhr.responseJSON && xhr.responseJSON.error) {
        errorMessage = xhr.responseJSON.error;
    } else if (xhr.responseText) {
        try {
            const response = JSON.parse(xhr.responseText);
            errorMessage = response.error || defaultMessage;
        } catch (e) {
            errorMessage = xhr.statusText || defaultMessage;
        }
    }
    
    showToast(errorMessage, 'danger');
    return errorMessage;
}

// Initialize tooltips
$(document).ready(function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Page transition animation
$(document).ready(function() {
    $('body').addClass('fade-in');
});