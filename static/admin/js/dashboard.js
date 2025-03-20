/**
 * WhoppahBridge Admin Dashboard
 * Custom JavaScript for the admin dashboard functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts and graphs
    initOrdersChart();
});

// Function to initialize the orders chart
function initOrdersChart() {
    const ctx = document.getElementById('orders-chart');
    if (!ctx) return;
    
    const canvas = ctx.getContext('2d');
    
    // Get data from Django template
    let labels = [];
    let counts = [];
    
    // If we have daily order data from the server
    if (window.dashboardData && window.dashboardData.dailyOrderData) {
        window.dashboardData.dailyOrderData.forEach(item => {
            labels.push(item.label);
            counts.push(item.count);
        });
    } else {
        // Fallback sample data
        labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        counts = [12, 19, 15, 27, 22, 19, 26];
    }
    
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Orders',
                    data: counts,
                    borderColor: '#005D33',
                    backgroundColor: 'rgba(0, 93, 51, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            }
        }
    });
}

// Optional: Event handlers for quick action buttons
document.addEventListener('click', function(e) {
    // Add any additional click handlers for dynamic elements as needed
    
    // For example, if you add dynamic filters or toggles in the future
    if (e.target.closest('.filter-toggle')) {
        const filter = e.target.closest('.filter-toggle');
        console.log(`Filter toggled: ${filter.dataset.filter}`);
        // Implement filter functionality
    }
});

// Handle errors when chart.js is loading data
window.addEventListener('error', function(e) {
    if (e.target && (e.target.src || e.target.href)) {
        console.error(`Error loading resource: ${e.target.src || e.target.href}`);
    }
});
