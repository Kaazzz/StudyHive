document.getElementById("switchMode").addEventListener("click", function() {
    const header = document.getElementById("header");
    const appName = document.getElementById("appName");
    const modeIconLogo = document.getElementById("mode-icon-logo");
    const modeIconHome = document.getElementById("mode-icon-home");
    const modeIconMessage = document.getElementById("mode-icon-message");
    
    const modeIconSwitch = document.getElementById("mode-icon-switch");
    
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
    
    const modeIconGroups = document.getElementById("mode-icon-mygroups");
    const modeIconCalendar = document.getElementById("mode-icon-calendar");
    const modeIconLogout = document.getElementById("mode-icon-logout");

    const sidebar = document.getElementById("sidebar");

    // Toggle the dark class on the body element
    document.body.classList.toggle("dark");

    // Check if dark mode is enabled
    if (document.body.classList.contains('dark')) {
        // Apply black-gradient for dark mode
        header.classList.remove("yellow-gradient");
        header.classList.add("black-gradient");
        appName.style.color = 'white'; // Ensure text color is set to white
        
        // Update logos and icons for dark mode
        modeIconLogo.src = staticUrls.logo;
        modeIconHome.src = staticUrls.lightModeHome;
        modeIconMessage.src = staticUrls.lightModeMessage;
        
        modeIconSwitch.src = staticUrls.lightModeLogo;
        
        searchButton.style.backgroundColor = darkModeButtonColor;
        searchButton.style.color = darkModeTextColor;
        filterSelect.style.backgroundColor = darkModeSelectColor;
        filterSelect.style.color = darkModeTextColor;
        
        modeIconGroups.src = staticUrls.lightModeGroups;
        modeIconCalendar.src = staticUrls.lightModeCalendar;
        modeIconLogout.src = staticUrls.lightModeLogout;

        sidebar.style.backgroundColor = '#1A1A1B'; // Set a slightly darker background color
        sidebar.style.color = '#FFFFFF';

        // Save the preference in localStorage
        localStorage.setItem('theme', 'dark');
    } else {
        // Apply yellow-gradient for light mode
        header.classList.remove("black-gradient");
        header.classList.add("yellow-gradient");
        appName.style.color = '#212121'; // Ensure text color is set to dark
        
        // Update logos and icons for light mode
        modeIconLogo.src = staticUrls.darkLogo;
        modeIconHome.src = staticUrls.darkModeHome;
        modeIconMessage.src = staticUrls.darkModeMessage;
        
        modeIconSwitch.src = staticUrls.darkModeLogo;
        
        searchButton.style.backgroundColor = lightModeButtonColor;
        searchButton.style.color = lightModeTextColor;
        filterSelect.style.backgroundColor = lightModeSelectColor
        filterSelect.style.color = lightModeTextColor; 
        
        modeIconGroups.src = staticUrls.darkModeGroups;
        modeIconCalendar.src = staticUrls.darkModeCalendar;
        modeIconLogout.src = staticUrls.darkModeLogout;

        sidebar.style.backgroundColor = '#FFFFFF';
        sidebar.style.color = '#000000';

        // Save the preference in localStorage
        localStorage.setItem('theme', 'light');
    }
});

// Load saved theme from localStorage
window.addEventListener('load', function() {
    const savedTheme = localStorage.getItem('theme');
    const header = document.getElementById("header");
    const appName = document.getElementById("appName");
    const modeIconLogo = document.getElementById("mode-icon-logo");
    const modeIconHome = document.getElementById("mode-icon-home");
    const modeIconMessage = document.getElementById("mode-icon-message");
    const modeIconSwitch = document.getElementById("mode-icon-switch");

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

    const modeIconGroups = document.getElementById("mode-icon-mygroups");
    const modeIconCalendar = document.getElementById("mode-icon-calendar");
    const modeIconLogout = document.getElementById("mode-icon-logout");

    const sidebar = document.getElementById("sidebar");

    if (savedTheme === 'dark') {
        // Apply dark mode and black-gradient
        document.body.classList.add('dark');
        header.classList.remove("yellow-gradient");
        header.classList.add("black-gradient");
        appName.style.color = 'white'; // Ensure text color is set to white
        
        // Update logos and icons for dark mode
        modeIconLogo.src = staticUrls.logo;
        modeIconHome.src = staticUrls.lightModeHome;
        modeIconMessage.src = staticUrls.lightModeMessage;
        
        modeIconSwitch.src = staticUrls.lightModeLogo;
        
        searchButton.style.backgroundColor = darkModeButtonColor;
        searchButton.style.color = darkModeTextColor;
        filterSelect.style.backgroundColor = darkModeSelectColor;
        filterSelect.style.color = darkModeTextColor;
        
        modeIconGroups.src = staticUrls.lightModeGroups;
        modeIconCalendar.src = staticUrls.lightModeCalendar;
        modeIconLogout.src = staticUrls.lightModeLogout;

        sidebar.style.backgroundColor = '1A1A1B'; // Set a slightly darker background color
        sidebar.style.color = '#FFFFFF';

    } else {
        // Apply light mode and yellow-gradient
        document.body.classList.remove('dark');
        header.classList.remove("black-gradient");
        header.classList.add("yellow-gradient");
        appName.style.color = '#212121'; // Ensure text color is set to dark
        
        // Update logos and icons for light mode
        modeIconLogo.src = staticUrls.darkLogo;
        modeIconHome.src = staticUrls.darkModeHome;
        modeIconMessage.src = staticUrls.darkModeMessage;
        
        modeIconSwitch.src = staticUrls.darkModeLogo;
        
        searchButton.style.backgroundColor = lightModeButtonColor;
        searchButton.style.color = lightModeTextColor;
        filterSelect.style.backgroundColor = lightModeSelectColor
        filterSelect.style.color = lightModeTextColor; 

        modeIconGroups.src = staticUrls.darkModeGroups;
        modeIconCalendar.src = staticUrls.darkModeCalendar;
        modeIconLogout.src = staticUrls.darkModeLogout;

        sidebar.style.backgroundColor = '#FFFFFF';
        sidebar.style.color = '#000000';
    }
});