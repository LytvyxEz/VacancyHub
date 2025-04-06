
document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.querySelector('.search-container');
    const searchInput = document.querySelector('.search-input');
    const filterForm = document.querySelector('.filter-section');
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


    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        performSearch();
    });

    filterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        performSearch();
    });

    function performSearch() {
        const params = new URLSearchParams();
        params.append('position', searchInput.value.trim());

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

    function updateCharts() {
        const data = JSON.parse('{{ skill_counts | safe }}');

        if (!data || Object.keys(data).length === 0) {
            document.getElementById("skills-chart").innerHTML = "<p>No data available for this search</p>";
            return;
        }

        const sortedSkills = Object.keys(data).sort((a, b) => data[b] - data[a]);
        const sortedCounts = sortedSkills.map(skill => data[skill]);

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
            title: "",
            xaxis: {
                title: { text: "Skills", standoff: 20 },
                tickangle: -45,
                automargin: true
            },
            yaxis: {
                title: "Mention Count",
                gridcolor: 'rgba(0, 0, 0, 0.05)'
            },
            margin: { t: 0, b: 150, l: 50, r: 20 },
            hovermode: 'closest'
        };

        Plotly.newPlot("skills-chart", chartData, layout, {responsive: true});
    }


    window.addEventListener('resize', function() {
        Plotly.Plots.resize('skills-chart');
    });
});
</script>