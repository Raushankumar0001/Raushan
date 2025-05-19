// Check if the section should be expanded on page load
window.onload = function() {
    const additionalDestinations = document.getElementById('additionalDestinations');
    const button = document.querySelector('.view-all-btn');
    
    // Check localStorage to see if the section should be expanded
    if (localStorage.getItem('destinationsExpanded') === 'true') {
        additionalDestinations.style.display = 'flex';
        button.textContent = 'View Less Destinations';
    } else {
        additionalDestinations.style.display = 'none';
        button.textContent = 'View All Destinations';
    }
};

function toggleDestinations() {
    const additionalDestinations = document.getElementById('additionalDestinations');
    const button = document.querySelector('.view-all-btn');

    // Toggle the display of additional destinations
    if (additionalDestinations.style.display === 'none' || additionalDestinations.style.display === '') {
        additionalDestinations.style.display = 'flex';
        button.textContent = 'View Less Destinations';

        // Store the state in localStorage
        localStorage.setItem('destinationsExpanded', 'true');
    } else {
        additionalDestinations.style.display = 'none';
        button.textContent = 'View All Destinations';

        // Store the state in localStorage
        localStorage.setItem('destinationsExpanded', 'false');
    }
}

let currentIndex = 0;
const slides = document.querySelector('.slides');
const totalSlides = document.querySelectorAll('.slides img').length;

function moveSlide(direction) {
    currentIndex += direction;

    if (currentIndex < 0) {
        currentIndex = totalSlides - 1; // Go to the last slide if we're at the first
    } else if (currentIndex >= totalSlides) {
        currentIndex = 0; // Go to the first slide if we're at the last
    }

    const offset = -currentIndex * 100; // Move slides based on the current index
    slides.style.marginLeft = `${offset}%`;
}
 // Open modal
 function openlogin() {
    document.getElementById('loginModal').style.display = 'flex';
    document.body.classList.add('modal-open'); // disable background scroll
  }
  
// Close modal
function closelogin() {
    document.getElementById('loginModal').style.display = 'none';
    document.body.classList.remove('modal-open'); // re-enable scroll
  }

// Fix typo and allow click outside to close
window.onclick = function(event) {
    const modal = document.getElementById('loginModal'); // fixed 'lodinModal'
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


function toggleTab(tab) {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const loginTab = document.getElementById('loginTab');
    const signupTab = document.getElementById('signupTab');

    if (tab === 'login') {
        loginForm.style.display = 'block';
        signupForm.style.display = 'none';
        loginTab.classList.add('active');
        signupTab.classList.remove('active');
    } else {
        loginForm.style.display = 'none';
        signupForm.style.display = 'block';
        loginTab.classList.remove('active');
        signupTab.classList.add('active');
    }
}


