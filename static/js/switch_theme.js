document.getElementById('change-theme-btn').addEventListener('click', function() {
    if (localStorage['dark_theme'] == "true") {
        localStorage['dark_theme'] = false
        document.querySelector('body').className = ""
    } else {
        localStorage['dark_theme'] = true;
        document.querySelector('body').className = "dark-theme"
    }
})
if ("dark_theme" in localStorage) { if (localStorage['dark_theme'] == "true") { document.querySelector('body').className = "dark-theme" } else { document.querySelector('body').className = "" } } else { localStorage['dark_theme'] = false }