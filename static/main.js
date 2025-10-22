function openTab(evt, tabName) {
    // Get all elements with class="tab-content" and hide them
    const tabcontent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        tabcontent[i].classList.remove("active");
    }

    // Get all elements with class="tab-link" and remove the "active" class
    const tablinks = document.getElementsByClassName("tab-link");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

document.addEventListener("DOMContentLoaded", () => {
    // Initialize the first tab
    if (document.querySelector(".tab-link")) {
        document.querySelector(".tab-link").click();
    }

    // Handle form submission to show loader
    const form = document.getElementById("evaluation-form");
    const loader = document.getElementById("loader");
    const resultsWrapper = document.getElementById("results-wrapper");

    if (form) {
        form.addEventListener("submit", () => {
            // Hide results and show loader
            if (resultsWrapper) {
                resultsWrapper.style.display = "none";
            }
            if (loader) {
                loader.style.display = "block";
            }
        });
    }
});