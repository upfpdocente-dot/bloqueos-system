// static/js/scripts.js

// Funcionalidad adicional para mejorar la experiencia de usuario

document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema de Bloqueos cargado correctamente');
    
    // Establecer la fecha actual como valor por defecto en el campo fecha
    const fechaField = document.getElementById('fecha');
    if (fechaField) {
        const now = new Date();
        const year = now.getFullYear();
        const month = (now.getMonth() + 1).toString().padStart(2, '0');
        const day = now.getDate().toString().padStart(2, '0');
        fechaField.value = `${year}-${month}-${day}`;
    }
    
    // Agregar tooltips a los botones
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-ocultar las alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Validación personalizada para el formulario
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            
            inputs.forEach(function(input) {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('is-invalid');
                    
                    // Crear mensaje de error si no existe
                    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'invalid-feedback';
                        errorDiv.textContent = 'Este campo es obligatorio';
                        input.parentNode.appendChild(errorDiv);
                    }
                } else {
                    input.classList.remove('is-invalid');
                    input.classList.add('is-valid');
                }
            });
            
            if (!isValid) {
                event.preventDefault();
                event.stopPropagation();
                
                // Mostrar alerta de error
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-danger alert-dismissible fade show';
                alertDiv.innerHTML = `
                    <strong>Error:</strong> Por favor completa todos los campos obligatorios.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                `;
                form.prepend(alertDiv);
                
                // Auto-ocultar la alerta después de 5 segundos
                setTimeout(function() {
                    const bsAlert = new bootstrap.Alert(alertDiv);
                    bsAlert.close();
                }, 5000);
            }
        });
    });
    
    // Efectos de animación para las tarjetas
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Mejorar la experiencia en móviles
    if (window.innerWidth < 768) {
        // Ajustar el padding en móviles
        document.querySelectorAll('.card-body').forEach(function(body) {
            body.classList.add('p-3');
        });
    }
    
    // Efecto de carga inicial
    document.body.style.opacity = '0';
    setTimeout(function() {
        document.body.style.transition = 'opacity 0.5s ease-in';
        document.body.style.opacity = '1';
    }, 100);
});

// Funciones de utilidad
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.appendChild(notification);
    
    // Auto-ocultar después de 5 segundos
    setTimeout(function() {
        const bsAlert = new bootstrap.Alert(notification);
        bsAlert.close();
    }, 5000);
}