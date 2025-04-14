
document.addEventListener("DOMContentLoaded", function() {
    // Toggle filter section
    const filterToggle = document.getElementById('filterToggle');
    const filterSection = document.getElementById('filterSection');
    
    filterToggle.addEventListener('click', function() {
        filterSection.classList.toggle('active');
        const icon = this.querySelector('i');
        icon.style.transform = filterSection.classList.contains('active') ? 'rotate(180deg)' : 'rotate(0)';
    });

    // Form submissions
    const searchForm = document.getElementById('searchForm');
    const filterForm = document.getElementById('filterForm');
    const searchInput = document.querySelector('.search-input');
    const experienceSelect = document.querySelector('select[name="experience"]');
    const salaryInput = document.querySelector('input[name="salary"]');
    const locationInput = document.querySelector('input[name="location"]');


    const urlParams = new URLSearchParams(window.location.search);
    const position = urlParams.get('position');
    const location = urlParams.get('location');

    if (position) {
        searchInput.value = position;
        if (location) {
            locationInput.value = location;
        }
        updateCharts();
    }

    function performSearch() {
        const params = new URLSearchParams();
        const searchValue = searchInput.value.trim();

        if (!searchValue) {
            searchInput.focus();
            return;
        }

        params.append('position', searchValue);

        if (locationInput.value.trim()) {
            params.append('location', locationInput.value.trim());
        }

        if (experienceSelect.value) {
            params.append('experience', experienceSelect.value);
        }

        if (document.querySelector('input[name="salary"]').value) {
            params.append('salary', document.querySelector('input[name="salary"]').value);
        }

        if (document.querySelector('input[name="max_pages"]').value) {
            params.append('max_pages', document.querySelector('input[name="max_pages"]').value);
        }

        window.location.search = params.toString();
    }

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        performSearch();
    });

    filterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        performSearch();
    });



});
