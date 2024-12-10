// Redirect to the search results page when clicking search or pressing Enter
document.getElementById('searchButton').addEventListener('click', function () {
    redirectToSearchResults();
});

document.getElementById('searchInput').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent default form submission
        redirectToSearchResults();
    }
});

// Redirect Function
function redirectToSearchResults() {
    const query = document.getElementById('searchInput').value;
    const filter = document.getElementById('filterSelect').value;

    // Redirect to the results page with query and filter as parameters
    const url = `/search_groups/?query=${encodeURIComponent(query)}&filter=${encodeURIComponent(filter)}`;
    window.location.href = url;
}