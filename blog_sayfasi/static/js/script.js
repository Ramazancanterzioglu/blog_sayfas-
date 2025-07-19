// Dark theme toggle
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    
    if (body.getAttribute('data-theme') === 'dark') {
        body.removeAttribute('data-theme');
        themeIcon.className = 'fas fa-moon';
    } else {
        body.setAttribute('data-theme', 'dark');
        themeIcon.className = 'fas fa-sun';
    }
}

// Scroll indicator
function updateScrollIndicator() {
    const winScroll = window.pageYOffset;
    const height = document.body.scrollHeight - window.innerHeight;
    const scrolled = (winScroll / height) * 100;
    document.querySelector('.scroll-indicator').style.width = scrolled + '%';
}

// Animate counters
function animateCounters() {
    const counters = document.querySelectorAll('.header-stat .number');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const current = +counter.innerText;
        const increment = target / 100;
        
        if (current < target) {
            counter.innerText = Math.ceil(current + increment);
            setTimeout(animateCounters, 30);
        } else {
            counter.innerText = target;
        }
    });
}

// Show alerts
function showAlert(type) {
    const messages = {
        course: 'Kapsamlı finansal eğitim programlarımız hakkında detaylı bilgi almak için iletişime geçin!',
        test: 'Finansal bilginizi test etmek için interaktif sorularımız yakında hazır olacak!',
        consult: 'Uzman finansal danışmanlarımızla görüşme planlamak için randevu alın!',
        suggest: 'Dizi/film önerilerinizi Instagram veya Twitter hesaplarımızdan paylaşabilirsiniz!'
    };
    
    alert(messages[type] || 'Yakında daha fazla özellik eklenecek!');
}

// Event listeners
window.addEventListener('scroll', updateScrollIndicator);

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
        }
    });
}, observerOptions);

// Observe cards
document.querySelectorAll('.card').forEach(card => {
    observer.observe(card);
});

// Header stats observer
const headerObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            setTimeout(animateCounters, 500);
            headerObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

const headerStats = document.querySelector('.header-stats');
if (headerStats) {
    headerObserver.observe(headerStats);
}

// Card hover effects
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-15px) scale(1.02)';
        this.style.boxShadow = '0 25px 50px rgba(0,0,0,0.15)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
        this.style.boxShadow = 'var(--shadow)';
    });
});

// Smooth scrolling
document.documentElement.style.scrollBehavior = 'smooth';

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Animate floating icons
    document.querySelectorAll('.floating-icon').forEach((icon, index) => {
        icon.style.animationDelay = Math.random() * 3 + 's';
    });
    
    // Button ripple effect
    document.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                border-radius: 50%;
                background: rgba(255,255,255,0.6);
                transform: scale(0);
                animation: ripple 0.6s linear;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                pointer-events: none;
            `;
            
            this.appendChild(ripple);
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Card 3D effect
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            this.style.transform = `translateY(-15px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotateX(0) rotateY(0) scale(1)';
        });
    });
});

// CSS animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style); 