// Add this script to both dashboard_admin.html and dashboard_cashier.html inside {% block extra_js %}
<script>
    // Greeting based on time of day
    function updateGreeting() {
        const hour = new Date().getHours();
        const greetingText = document.getElementById('greetingText');
        
        if (hour >= 3 && hour < 11) {
            greetingText.textContent = 'Selamat pagi';
        } else if (hour >= 11 && hour < 15) {
            greetingText.textContent = 'Selamat siang';
        } else if (hour >= 15 && hour < 18) {
            greetingText.textContent = 'Selamat sore';
        } else {
            greetingText.textContent = 'Selamat malam';
        }
    }

    // Update greeting every minute
    document.addEventListener('DOMContentLoaded', function() {
        updateGreeting();
        setInterval(updateGreeting, 60000);
    });
</script>
