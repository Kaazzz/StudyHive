document.addEventListener("DOMContentLoaded", function() {
    const switchMode = document.getElementById("switchMode");
    const modeIcon = document.getElementById("mode-icon-switch");
    const homeIcon = document.getElementById("mode-icon-home");
    const messageIcon = document.getElementById("mode-icon-message");
    const notifIcon = document.getElementById("mode-icon-notif");
    const logoIcon = document.getElementById("mode-icon-logo");
    const header = document.getElementById("header");

    const searchButton = document.getElementById("searchButton");
    const filterSelect = document.getElementById("filterSelect");

    const tooltipText = document.getElementById("tooltip-text");

    const lightModeButtonColor = '#010600';
    const lightModeSelectColor = '#010600';
    const lightModeTextColor = '#FFFFFF';

    const darkModeButtonColor = '#f2d638';
    const darkModeSelectColor = '#f2d638';
    const darkModeTextColor = '#000000';

    const gray = '#1f2937';
    const white = '#ffffff';

    const appName = document.getElementById("appName");

    // Check if dark mode is enabled by default
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.classList.add("dark");
        header.classList.remove("yellow-gradient");
        header.classList.add("black-gradient");
        modeIcon.src = staticUrls.lightModeLogo;
        homeIcon.src = staticUrls.lightModeHome;
        messageIcon.src = staticUrls.lightModeMessage;
        notifIcon.src = staticUrls.lightModeNotif;
        logoIcon.src = staticUrls.logo;

        // Set the color for dark mode elements
        searchButton.style.backgroundColor = darkModeButtonColor;
        filterSelect.style.backgroundColor = darkModeSelectColor;
    }

    // Toggle dark mode
    switchMode.addEventListener("click", () => {
        document.body.classList.toggle("dark");

        if (document.body.classList.contains("dark")) {
            header.classList.remove("yellow-gradient");
            header.classList.add("black-gradient");
            filterSelect.classList.remove("black-gradient");
            filterSelect.classList.add("yellow-gradient");
            searchButton.classList.remove("black-gradient");
            searchButton.classList.add("yellow-gradient");

            modeIcon.src = staticUrls.lightModeLogo;
            homeIcon.src = staticUrls.lightModeHome;
            messageIcon.src = staticUrls.lightModeMessage;
            notifIcon.src = staticUrls.lightModeNotif; 
            logoIcon.src = staticUrls.logo;

            // Change to dark mode colors
            searchButton.style.backgroundColor = darkModeButtonColor;
            searchButton.style.color = darkModeTextColor;
            filterSelect.style.backgroundColor = darkModeSelectColor;
            filterSelect.style.color = darkModeTextColor;

            appName.style.color = white;

        } else {
            header.classList.remove("black-gradient");
            header.classList.add("yellow-gradient");
            filterSelect.classList.remove("yellow-gradient");
            filterSelect.classList.add("black-gradient");
            searchButton.classList.remove("yellow-gradient");
            searchButton.classList.add("black-gradient");

            modeIcon.src = staticUrls.darkModeLogo;
            homeIcon.src = staticUrls.darkModeHome;
            messageIcon.src = staticUrls.darkModeMessage;
            notifIcon.src = staticUrls.darkModeNotif; 
            logoIcon.src = staticUrls.darkLogo;

            // Reset to light mode colors
            searchButton.style.backgroundColor = lightModeButtonColor;
            searchButton.style.color = lightModeTextColor;
            filterSelect.style.backgroundColor = lightModeSelectColor
            filterSelect.style.color = lightModeTextColor; 

            appName.style.color = gray;
        }
    });
});
