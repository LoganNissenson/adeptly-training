// Adeptly Training JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Make problem answer options more interactive
    initProblemOptions();
    
    // Initialize range sliders
    initRangeSliders();
});

function initProblemOptions() {
    // Problem answer options - make entire option clickable
    const answerOptions = document.querySelectorAll('.answer-option');
    if (answerOptions.length > 0) {
        answerOptions.forEach(option => {
            option.addEventListener('click', function() {
                // Find the associated radio input
                const radioId = this.getAttribute('for');
                const radio = document.getElementById(radioId);
                if (radio) {
                    radio.checked = true;
                    
                    // Update visual selection
                    answerOptions.forEach(opt => opt.classList.remove('selected'));
                    this.classList.add('selected');
                }
            });
        });
    }
}

function initRangeSliders() {
    // Training time slider
    const timeSlider = document.getElementById('id_time_available');
    const timeDisplay = document.getElementById('timeDisplay');
    
    if (timeSlider && timeDisplay) {
        timeSlider.addEventListener('input', function() {
            timeDisplay.textContent = this.value + ' minutes';
            updateTrainingEstimates(this.value);
        });
    }
}

function updateTrainingEstimates(minutes) {
    const problemEstimate = document.getElementById('estimatedProblems');
    const expEstimate = document.getElementById('potentialExperience');
    
    if (problemEstimate && expEstimate) {
        const minProblems = Math.floor(minutes / 5);
        const maxProblems = Math.ceil(minutes / 3);
        
        problemEstimate.textContent = minProblems + '-' + maxProblems + ' problems';
        
        const minXP = minProblems * 10;
        const maxXP = maxProblems * 20;
        expEstimate.textContent = minXP + '-' + maxXP + ' XP';
    }
}
