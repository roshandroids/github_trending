document.addEventListener('DOMContentLoaded', function () {
    // Set the selected option based on the query parameter in the URL
    var urlParams = new URLSearchParams(window.location.search);
    var urlDuration = urlParams.get('duration');

    console.log('URL Duration:', urlDuration);

    // Update the select element only if the URL parameter is valid
    if (urlDuration && ['daily', 'weekly', 'monthly'].includes(urlDuration)) {
        console.log('Setting value:', urlDuration);
        document.getElementById('time_span').value = urlDuration;
    } else {
        console.log('Invalid or missing URL duration:', urlDuration);
    }
});

function updateFormAction() {
    var selectedOption = document.getElementById('time_span').value;
    var form = document.getElementById('time_span_form');
    form.action = "/?duration=" + selectedOption;
    form.submit(); // Manually submit the form
}

function filterByLanguage(selectedLanguage) {
    var repositoryCards = document.querySelectorAll('.repository-card');

    repositoryCards.forEach(function(card) {
        var language = card.querySelector('.language span').textContent;

        if (selectedLanguage === '' || selectedLanguage === language) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function resetFilter() {
    var repositoryCards = document.querySelectorAll('.repository-card');
    
    repositoryCards.forEach(function(card) {
        card.style.display = 'block';
    });

    document.getElementById('languageSelect').value = '';
}

function filterByRepoCount(selectedCount) {
    var repositoryCards = document.querySelectorAll('.repository-card');

    repositoryCards.forEach(function(card, index) {
        if (selectedCount === 'all' || index < parseInt(selectedCount, 10)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
