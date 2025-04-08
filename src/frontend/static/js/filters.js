
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
    const salaryInput = document.querySelector('input[name="salary_min"]');
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

        if (salaryInput.value) {
            params.append('salary_min', salaryInput.value);
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

    function updateCharts() {
        // This would be replaced with actual data from your backend
        const sampleData = {
            "Python": 45,
            "JavaScript": 38,
            "SQL": 32,
            "Java": 28,
            "AWS": 25,
            "React": 22,
            "Docker": 18,
            "Kubernetes": 15,
            "Machine Learning": 12,
            "Data Analysis": 10
        };

        if (!sampleData || Object.keys(sampleData).length === 0) {
            document.getElementById("skills-chart").innerHTML = "<p>No data available for this search</p>";
            return;
        }

        const sortedSkills = Object.keys(sampleData).sort((a, b) => sampleData[b] - sampleData[a]);
        const sortedCounts = sortedSkills.map(skill => sampleData[skill]);

        const chartData = [{
            x: sortedSkills,
            y: sortedCounts,
            type: "bar",
            marker: {
                color: "rgba(67, 97, 238, 0.7)",
                line: {
                    color: 'rgba(67, 97, 238, 1)',
                    width: 1.5
                }
            }
        }];

        const layout = {
            title: "Top Required Skills",
            xaxis: {
                title: { text: "Skills", standoff: 20 },
                tickangle: -45,
                automargin: true
            },
            yaxis: {
                title: "Mention Count",
                gridcolor: 'rgba(0, 0, 0, 0.05)'
            },
            margin: { t: 40, b: 150, l: 50, r: 20 },
            hovermode: 'closest'
        };

        Plotly.newPlot("skills-chart", chartData, layout, {responsive: true});
    }

    window.addEventListener('resize', function() {
        if (document.getElementById("skills-chart")) {
            Plotly.Plots.resize('skills-chart');
        }
    });
});
