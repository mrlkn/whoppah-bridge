/**
 * WhoppahBridge Admin Enhancements
 * Custom JavaScript to enhance the admin interface functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar functionality
    const sidebarToggle = document.querySelector('.unfold-sidebar-toggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.body.classList.toggle('unfold-sidebar-collapsed');
            // Store the preference
            localStorage.setItem('unfold_sidebar_collapsed', 
                document.body.classList.contains('unfold-sidebar-collapsed'));
        });
        
        // Check for stored preference on load
        if (localStorage.getItem('unfold_sidebar_collapsed') === 'true') {
            document.body.classList.add('unfold-sidebar-collapsed');
        }
    }
    
    // Add confirmation to delete actions
    const deleteButtons = document.querySelectorAll('.deletelink, input[name="_delete"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Improve filter visibility in admin list views
    const filterButtons = document.querySelectorAll('.filter-button');
    filterButtons.forEach(function(button) {
        button.classList.add('button');
    });
    
    // Add autocomplete="off" to filter fields to prevent browser autocomplete interference
    const filterFields = document.querySelectorAll('.unfold-filters input, .unfold-filters select');
    filterFields.forEach(function(field) {
        field.setAttribute('autocomplete', 'off');
    });
    
    // Add field highlighting for required fields
    const requiredFields = document.querySelectorAll('.required input, .required select, .required textarea');
    requiredFields.forEach(function(field) {
        field.classList.add('required-field');
    });
    
    // Add help text toggle functionality
    const helpTextToggle = document.createElement('button');
    helpTextToggle.type = 'button';
    helpTextToggle.className = 'help-text-toggle button whoppah-button';
    helpTextToggle.textContent = 'Toggle Help Text';
    helpTextToggle.addEventListener('click', function() {
        document.body.classList.toggle('hide-help-text');
        this.textContent = document.body.classList.contains('hide-help-text') 
            ? 'Show Help Text' 
            : 'Hide Help Text';
    });
    
    const submitRow = document.querySelector('.submit-row');
    if (submitRow) {
        submitRow.insertAdjacentElement('beforebegin', helpTextToggle);
    }
});
