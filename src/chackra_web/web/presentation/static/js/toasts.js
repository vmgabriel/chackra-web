/**
 * Toast Notifications Manager
 * Inicializa y muestra las notificaciones tipo toast de Bootstrap
 */

class ToastManager {
    constructor(options = {}) {
        this.options = {
            autohide: true,
            delay: 5000,
            ...options
        };

        this.init();
    }

    init() {
        const toastElements = document.querySelectorAll('.toast');

        toastElements.forEach(toastEl => {
            const toast = new bootstrap.Toast(toastEl, this.options);
            toast.show();

            // Limpiar del DOM después de ocultarse
            toastEl.addEventListener('hidden.bs.toast', () => {
                toastEl.remove();
            });
        });
    }

    /**
     * Método estático para crear toasts dinámicamente
     * @param {string} message - Mensaje a mostrar
     * @param {string} type - Tipo de toast (success, danger, warning, info)
     */
    static show(message, type = 'info') {
        const container = document.querySelector('.toast-container') || this.createContainer();
        const toast = this.createToastElement(message, type);

        container.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', () => toast.remove());
    }

    static createContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1100';
        document.body.appendChild(container);
        return container;
    }

    static createToastElement(message, type) {
        const toast = document.createElement('div');
        const bgClass = {
            success: 'bg-success',
            danger: 'bg-danger',
            warning: 'bg-warning',
            info: 'bg-info'
        }[type] || 'bg-primary';

        const iconClass = {
            success: 'bi-check-circle',
            danger: 'bi-exclamation-triangle',
            warning: 'bi-exclamation-circle',
            info: 'bi-info-circle'
        }[type] || 'bi-info-circle';

        toast.className = `toast align-items-center text-white border-0 ${bgClass}`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${iconClass} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                        data-bs-dismiss="toast" aria-label="Cerrar"></button>
            </div>
        `;

        return toast;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new ToastManager();
});

// Exportar para uso global
window.ToastManager = ToastManager;