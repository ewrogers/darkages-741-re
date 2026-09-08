// Keep native horizontal scrolling inside a focused diagram. mdBook otherwise
// consumes these keys for chapter navigation at the document level.
document.querySelectorAll(".diagram-scroll").forEach((region) => {
    region.addEventListener("keydown", (event) => {
        if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
            event.stopPropagation();
        }
    });
});
