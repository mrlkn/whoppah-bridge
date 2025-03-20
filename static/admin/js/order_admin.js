(function($) {
    'use strict';
    
    // Wait for the DOM to be ready
    $(document).ready(function() {
        // Save original order status for comparison
        const originalStatus = $('#id_status').val();
        
        // Add status change tracking
        $('#id_status').on('change', function() {
            const newStatus = $(this).val();
            if (newStatus !== originalStatus) {
                // Add visual indicator that status is changing
                $(this).addClass('status-changed');
                
                // Show notification about status change
                if (!$('#status-change-notice').length) {
                    const notice = $('<div id="status-change-notice" class="alert alert-info"></div>')
                        .text('Status will be updated when you save this order.')
                        .css({
                            'padding': '10px 15px',
                            'margin': '15px 0',
                            'border-left': '5px solid #17a2b8',
                            'background-color': '#e3f7fc'
                        });
                    $(this).parent().after(notice);
                }
            } else {
                // Remove visual indicator if status is set back to original
                $(this).removeClass('status-changed');
                $('#status-change-notice').remove();
            }
        });
        
        // Show confirmation dialog for specific actions
        $('.action-cancel, button#mark-cancelled-btn').on('click', function(e) {
            if (!confirm('Are you sure you want to cancel this order? This cannot be undone.')) {
                e.preventDefault();
                return false;
            }
        });
        
        // Add courier assignment tracking
        const originalCourier = $('#id_assigned_courier').val();
        $('#id_assigned_courier').on('change', function() {
            const newCourier = $(this).val();
            if (newCourier !== originalCourier) {
                if (!$('#courier-change-notice').length) {
                    const notice = $('<div id="courier-change-notice" class="alert alert-info"></div>')
                        .text('Courier assignment will be updated when you save this order.')
                        .css({
                            'padding': '10px 15px',
                            'margin': '15px 0',
                            'border-left': '5px solid #17a2b8',
                            'background-color': '#e3f7fc'
                        });
                    $(this).parent().after(notice);
                }
            } else {
                $('#courier-change-notice').remove();
            }
        });
        
        // Add warning for 2-man delivery orders
        if ($('#id_two_man_delivery').is(':checked')) {
            const warning = $('<div class="two-man-warning alert alert-warning"></div>')
                .text('This order requires two-man delivery. Make sure to assign appropriate resources.')
                .css({
                    'padding': '10px 15px',
                    'margin': '15px 0',
                    'border-left': '5px solid #ffc107',
                    'background-color': '#fff3cd'
                });
            $('#id_two_man_delivery').parent().after(warning);
        }
        
        // Toggle two-man delivery warning when checkbox changes
        $('#id_two_man_delivery').on('change', function() {
            if ($(this).is(':checked')) {
                if (!$('.two-man-warning').length) {
                    const warning = $('<div class="two-man-warning alert alert-warning"></div>')
                        .text('This order requires two-man delivery. Make sure to assign appropriate resources.')
                        .css({
                            'padding': '10px 15px',
                            'margin': '15px 0',
                            'border-left': '5px solid #ffc107',
                            'background-color': '#fff3cd'
                        });
                    $(this).parent().after(warning);
                }
            } else {
                $('.two-man-warning').remove();
            }
        });
        
        // Add order URL field enhancement
        if ($('#id_order_url').length) {
            const orderUrlField = $('#id_order_url');
            const orderUrlVal = orderUrlField.val();
            
            if (orderUrlVal) {
                // Add a "View" button next to the URL field
                const viewButton = $('<a class="button" target="_blank">View Order</a>')
                    .attr('href', orderUrlVal)
                    .css({
                        'margin-left': '10px',
                        'vertical-align': 'middle'
                    });
                orderUrlField.after(viewButton);
            }
        }
        
        // Add product URL field enhancement
        if ($('#id_product_url').length) {
            const productUrlField = $('#id_product_url');
            const productUrlVal = productUrlField.val();
            
            if (productUrlVal) {
                // Add a "View" button next to the URL field
                const viewButton = $('<a class="button" target="_blank">View Product</a>')
                    .attr('href', productUrlVal)
                    .css({
                        'margin-left': '10px',
                        'vertical-align': 'middle'
                    });
                productUrlField.after(viewButton);
            }
        }
        
        // Add quick filter buttons for order status in change list
        if ($('#changelist').length) {
            // We'll add this functionality in the change_list.html template
            // since it's more reliable to work with Django's template system
        }
    });
    
})(django.jQuery);
