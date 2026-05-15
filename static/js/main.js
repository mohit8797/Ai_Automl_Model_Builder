/**
 * ================================================
 * AutoML Model Builder - Frontend Utilities
 * Modern, responsive, production-ready UX
 * ================================================
 */

// ==========================================
// Toast Notifications System
// ==========================================

class Toast {
    static show(message, type = 'info', duration = 3000) {
        const toast = this.createToastElement(message, type);
        this.addToastToDOM(toast);
        
        if (duration > 0) {
            setTimeout(() => this.removeToast(toast), duration);
        }
    }

    static createToastElement(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <div class="toast-message">${message}</div>
            </div>
        `;
        return toast;
    }

    static addToastToDOM(toast) {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        container.appendChild(toast);
        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);
    }

    static removeToast(toast) {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }

    static success(message) {
        this.show(message, 'success');
    }

    static error(message) {
        this.show(message, 'danger', 4000);
    }

    static warning(message) {
        this.show(message, 'warning');
    }

    static info(message) {
        this.show(message, 'info');
    }
}

// ==========================================
// Loading State Manager
// ==========================================

class LoadingManager {
    static setLoading(buttonSelector, isLoading = true) {
        const button = document.querySelector(buttonSelector);
        if (!button) return;

        if (isLoading) {
            button.disabled = true;
            button.classList.add('loading');
            button.innerHTML = `
                <span class="spinner-small"></span>
                <span>Processing...</span>
            `;
        } else {
            button.disabled = false;
            button.classList.remove('loading');
            button.innerHTML = button.dataset.originalText || 'Submit';
        }
    }

    static captureOriginalText(buttonSelector) {
        const button = document.querySelector(buttonSelector);
        if (button) {
            button.dataset.originalText = button.innerHTML;
        }
    }

    static showFullPageLoader(message = 'Loading...') {
        const loaderHTML = `
            <div id="full-loader" class="full-loader">
                <div class="loader-content">
                    <div class="spinner"></div>
                    <p>${message}</p>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', loaderHTML);
    }

    static hideFullPageLoader() {
        const loader = document.getElementById('full-loader');
        if (loader) {
            loader.classList.add('hide');
            setTimeout(() => loader.remove(), 300);
        }
    }
}

// ==========================================
// Form Validation Utilities
// ==========================================

class FormValidator {
    static validateRequired(input) {
        return input.value.trim().length > 0;
    }

    static validateEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    static validateFileSize(file, maxSizeInMB = 25) {
        const maxSizeInBytes = maxSizeInMB * 1024 * 1024;
        return file.size <= maxSizeInBytes;
    }

    static validateFileType(file, allowedTypes) {
        return allowedTypes.includes(file.type) || allowedTypes.some(type => {
            if (type.includes('*')) {
                const [category] = type.split('/');
                return file.type.startsWith(category);
            }
            return file.type === type;
        });
    }

    static showError(inputElement, message) {
        inputElement.classList.add('error');
        const existingError = inputElement.parentElement.querySelector('.form-error');
        if (existingError) existingError.remove();
        
        const errorElement = document.createElement('div');
        errorElement.className = 'form-error';
        errorElement.textContent = message;
        inputElement.parentElement.appendChild(errorElement);
    }

    static clearError(inputElement) {
        inputElement.classList.remove('error');
        const error = inputElement.parentElement.querySelector('.form-error');
        if (error) error.remove();
    }
}

// ==========================================
// File Upload Handler
// ==========================================

class FileUploadHandler {
    static initDragDrop(dropZoneSelector, inputSelector) {
        const dropZone = document.querySelector(dropZoneSelector);
        const input = document.querySelector(inputSelector);

        if (!dropZone || !input) return;

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, e => e.preventDefault());
        });

        dropZone.addEventListener('dragover', () => {
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            dropZone.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length) {
                input.files = files;
                this.handleFileSelect(input);
            }
        });

        input.addEventListener('change', () => {
            this.handleFileSelect(input);
        });
    }

    static handleFileSelect(input) {
        const file = input.files[0];
        if (!file) return;

        const fileName = document.querySelector('[data-file-name]');
        if (fileName) {
            fileName.textContent = `Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
        }
    }
}

// ==========================================
// Smooth Scroll Navigation
// ==========================================

class SmoothScroll {
    static init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                const href = anchor.getAttribute('href');
                if (href === '#') return;
                
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }
}

// ==========================================
// Multi-Step Form Handler
// ==========================================

class MultiStepForm {
    constructor(formSelector) {
        this.form = document.querySelector(formSelector);
        this.currentStep = 1;
        this.steps = [];
        this.init();
    }

    init() {
        this.steps = this.form.querySelectorAll('[data-step]');
        this.setupStepButtons();
        this.showStep(1);
    }

    setupStepButtons() {
        const nextButtons = this.form.querySelectorAll('[data-next-step]');
        const prevButtons = this.form.querySelectorAll('[data-prev-step]');

        nextButtons.forEach(btn => {
            btn.addEventListener('click', () => this.nextStep());
        });

        prevButtons.forEach(btn => {
            btn.addEventListener('click', () => this.previousStep());
        });
    }

    showStep(stepNumber) {
        if (stepNumber < 1 || stepNumber > this.steps.length) return;

        this.steps.forEach(step => {
            step.classList.remove('active');
        });

        const currentStepElement = this.form.querySelector(`[data-step="${stepNumber}"]`);
        if (currentStepElement) {
            currentStepElement.classList.add('active');
        }

        this.updateStepIndicators(stepNumber);
        this.updateProgressBar(stepNumber);
        this.currentStep = stepNumber;
    }

    updateStepIndicators(stepNumber) {
        const indicators = this.form.querySelectorAll('[data-step-indicator]');
        indicators.forEach((indicator, index) => {
            const stepNum = index + 1;
            indicator.classList.remove('active', 'completed');
            
            if (stepNum < stepNumber) {
                indicator.classList.add('completed');
            } else if (stepNum === stepNumber) {
                indicator.classList.add('active');
            }
        });
    }

    updateProgressBar(stepNumber) {
        const progressBar = this.form.querySelector('[data-progress-bar]');
        if (progressBar) {
            const progress = (stepNumber / this.steps.length) * 100;
            progressBar.style.width = progress + '%';
        }
    }

    nextStep() {
        if (this.validateCurrentStep()) {
            this.showStep(this.currentStep + 1);
        }
    }

    previousStep() {
        this.showStep(this.currentStep - 1);
    }

    validateCurrentStep() {
        const stepElement = this.form.querySelector(`[data-step="${this.currentStep}"]`);
        if (!stepElement) return true;

        const inputs = stepElement.querySelectorAll('[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!FormValidator.validateRequired(input)) {
                FormValidator.showError(input, 'This field is required');
                isValid = false;
            } else {
                FormValidator.clearError(input);
            }
        });

        return isValid;
    }

    getCurrentStep() {
        return this.currentStep;
    }

    getTotalSteps() {
        return this.steps.length;
    }
}

// ==========================================
// API Request Helper
// ==========================================

class APIClient {
    static async request(url, options = {}) {
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const finalOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, finalOptions);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || `HTTP ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    static get(url) {
        return this.request(url, { method: 'GET' });
    }

    static post(url, body) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(body),
        });
    }

    static put(url, body) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(body),
        });
    }

    static delete(url) {
        return this.request(url, { method: 'DELETE' });
    }

    static async uploadFile(url, file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Upload failed');
            }

            return data;
        } catch (error) {
            console.error('Upload Error:', error);
            throw error;
        }
    }
}

// ==========================================
// Utility Functions
// ==========================================

class Utils {
    static formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }

    static formatNumber(num) {
        return num.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        });
    }

    static formatDate(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        });
    }

    static copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            Toast.success('Copied to clipboard!');
        }).catch(() => {
            Toast.error('Failed to copy');
        });
    }

    static generateRandomString(length = 8) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    static debounce(func, wait) {
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

    static throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// ==========================================
// DOM Ready Handler
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize smooth scroll
    SmoothScroll.init();

    // Add toast container CSS
    const style = document.createElement('style');
    style.textContent = `
        .toast-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .toast {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 0.75rem;
            padding: 1rem 1.5rem;
            color: #f5f7fa;
            min-width: 300px;
            max-width: 400px;
            animation: slideOut 0.3s ease-out;
            opacity: 0;
            transform: translateX(100%);
        }

        .toast.show {
            opacity: 1;
            transform: translateX(0);
        }

        @keyframes slideOut {
            to {
                opacity: 0;
                transform: translateX(100%);
            }
        }

        .toast-success {
            border-color: #10b981;
            background: rgba(16, 185, 129, 0.1);
        }

        .toast-danger {
            border-color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
        }

        .toast-warning {
            border-color: #f59e0b;
            background: rgba(245, 158, 11, 0.1);
        }

        .toast-info {
            border-color: #3b82f6;
            background: rgba(59, 130, 246, 0.1);
        }

        .full-loader {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 14, 39, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            opacity: 1;
            transition: opacity 0.3s ease-out;
        }

        .full-loader.hide {
            opacity: 0;
        }

        .loader-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1rem;
        }

        [data-step] {
            display: none;
        }

        [data-step].active {
            display: block;
            animation: fadeIn 0.3s ease-out;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        Toast,
        LoadingManager,
        FormValidator,
        FileUploadHandler,
        SmoothScroll,
        MultiStepForm,
        APIClient,
        Utils,
    };
}
