document.addEventListener('DOMContentLoaded', function () {
    // Function to open the modal and load the graph
    function openGraphModal(route) {
        var modal = document.getElementById('graphModal');
        modal.style.display = 'block';

        // Load the graph content into the modal
        loadGraphContent(route);
    }

    // Function to close the modal
    function closeGraphModal() {
        var modal = document.getElementById('graphModal');
        modal.style.display = 'none';
    }

    // Function to load the graph content into the modal
    function loadGraphContent(route) {
        // Use AJAX to load the graph content based on the selected route
        var xhttp = new XMLHttpRequest();

        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                // Update the content of 'graphContainer' with the received HTML
                document.getElementById('graphContainer').innerHTML = this.responseText;
            }
        };

        // Make a GET request to the specified route
        xhttp.open('GET', route, true);
        xhttp.send();
    }

    // Event listeners for opening and closing the modal
    document.getElementById('showBarChart').addEventListener('click', function () {
        openGraphModal('/graph');
    });

    document.getElementById('showPieChart').addEventListener('click', function () {
        openGraphModal('/pieChart');
    });

    document.getElementById('showBoxPlot').addEventListener('click', function () {
        openGraphModal('/boxPlot');
    });

    document.getElementById('closeModal').addEventListener('click', function () {
        closeGraphModal();
    });
});
