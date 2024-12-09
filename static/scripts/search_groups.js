// search_group.js

// Search when clicking the search button
document.getElementById('searchButton').addEventListener('click', function () {
    performSearch();
});

// Search when pressing the "Enter" key in the input field
document.getElementById('searchInput').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default form submission if applicable
        performSearch();
    }
});

// Function to perform the search (common for both button click and Enter key)
function performSearch() {
    const query = document.getElementById('searchInput').value;
    const filter = document.getElementById('filterSelect').value;

    // Make the AJAX request for searching groups
    fetch(`/search_groups/?query=${query}&filter=${filter}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const resultsContainer = document.getElementById('resultsContainer');
        resultsContainer.innerHTML = ''; // Clear previous results

        // Check if results are found
        if (data.results.length > 0) {
            data.results.forEach(group => {
                let buttonText = 'Join';
                let buttonClass = 'join-button';

                if (group.is_creator || group.is_member) {
                    buttonText = 'Enter';
                    buttonClass = 'enter-button';
                } else if (group.is_private) {
                    buttonText = 'Request';
                    buttonClass = 'request-button';
                }

                // Result Container
                resultsContainer.innerHTML += `
                    <div class="group-card">
                        <h3>${group.group_name}</h3>
                        <p>Subject: ${group.subject}</p>
                        <p>Members: ${group.members_count}</p>
                        <button class="group-action-button ${buttonClass}" data-group-id="${group.unique_id}" onclick="handleGroupAction('${group.unique_id}', '${buttonClass}')">${buttonText}</button>
                        <p><a href="/group/${group.unique_id}/">View Group</a></p>
                    </div>
                `;
            });
        } else {
            resultsContainer.innerHTML = '<p>No results found.</p>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('resultsContainer').innerHTML = '<p>Error loading results.</p>';
    });
}

// Handle group actions
function handleGroupAction(groupId, actionType) {
    // Your existing handleGroupAction logic here
    if (actionType === 'join-button') {
        // Handle joining the group via AJAX
        fetch('/join/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ group_code: groupId }) // Sending the unique_id as the group code
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message); // Show the success/error message
            if (data.redirect_url) {
                window.location.href = data.redirect_url; // Redirect to the dashboard
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error joining the group.');
        });
    } else if (actionType === 'enter-button') {
        // Redirect to the group detail page
        window.location.href = `/group/${groupId}/`; 
    } else if (actionType === 'request-button') {
        // Handle request to join a private group
        console.log(`Requesting to join private group with ID: ${groupId}`);
        // Optionally, implement request logic here
        // Handle request to join a private group via AJAX
        fetch('/request-join/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ group_id: groupId }) // Sending the unique_id as group_id
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message); // Show the success/error message
        })
        .catch(error => {
            console.error('Error:', error);
            // alert('There was an error sending the join request.');
            alert('Join request already sent.');
        });
    }
}

// Get CSRF Token (for AJAX requests)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
