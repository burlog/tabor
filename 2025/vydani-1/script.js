function fixFirefoxGap() {
    if (navigator.userAgent.toLowerCase().includes("firefox")) {
        document.querySelectorAll("[data-gap]").forEach(el => {
            const gap = el.getAttribute("data-gap");
            if (gap)
                el.style.marginTop = gap;
        });
    }
}
