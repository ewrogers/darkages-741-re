// Progressive navigation only: mdBook still owns themes, search, and chapters.
(() => {
    "use strict";
    const scriptURL = document.currentScript.src;
    const rootURL = new URL("../", scriptURL);
    const main = document.querySelector("main");
    if (!main || new URL(location.href).pathname.endsWith("/print.html")) return;

    const title = main.querySelector("h1");
    if (!title) return;
    if (!main.id) main.id = "grimoire-main";
    main.tabIndex = -1;
    const skip = document.createElement("a");
    skip.className = "skip-to-content";
    skip.href = "#" + main.id;
    skip.textContent = "Skip to content";
    document.body.prepend(skip);

    const sidebar = document.querySelector(".sidebar-scrollbox");
    if (sidebar) {
        const brand = document.createElement("a");
        brand.className = "book-brand";
        brand.href = new URL("index.html", rootURL).href;
        brand.setAttribute("aria-label", "The Dark Ages Grimoire, book home");
        const mark = document.createElement("img");
        mark.src = new URL("assets/ornaments/bookplate.svg", rootURL).href;
        mark.alt = "";
        mark.width = mark.height = 48;
        const text = document.createElement("span");
        const name = document.createElement("strong");
        name.textContent = "Dark Ages";
        const subtitle = document.createElement("small");
        subtitle.textContent = "THE GRIMOIRE · CLIENT 741";
        text.append(name, subtitle);
        brand.append(mark, text);
        sidebar.prepend(brand);
    }

    const labels = {
        light: "Parchment",
        navy: "Lamplight",
        rust: "Parchment (Rust)",
        coal: "Lamplight (Coal)",
        ayu: "Lamplight (Ayu)",
    };
    for (const [theme, label] of Object.entries(labels)) {
        const button = document.getElementById("mdbook-theme-" + theme);
        if (button) button.textContent = label;
    }

    if (!main.querySelector(".book-frontispiece")) {
        const kicker = document.createElement("div");
        kicker.className = "chapter-kicker";
        kicker.textContent = "CLIENT 741 · REFERENCE & EVIDENCE";
        title.before(kicker);
    }

    const headings = [...main.querySelectorAll("h2[id], h3[id]")];
    if (headings.length > 1) {
        const outline = document.createElement("details");
        outline.className = "page-outline";
        const summary = document.createElement("summary");
        summary.textContent = "On this page";
        const nav = document.createElement("nav");
        nav.setAttribute("aria-label", "On this page");
        const list = document.createElement("ol");
        const links = headings.map((heading) => {
            const item = document.createElement("li");
            if (heading.tagName === "H3") item.className = "subsection";
            const link = document.createElement("a");
            link.href = "#" + encodeURIComponent(heading.id);
            link.textContent = heading.textContent;
            item.append(link);
            list.append(item);
            return link;
        });
        const top = document.createElement("a");
        top.className = "outline-top";
        top.href = "#" + encodeURIComponent(title.id);
        top.textContent = "Back to top";
        nav.append(list, top);
        outline.append(summary, nav);
        const introduction = title.nextElementSibling;
        if (introduction && introduction.tagName === "P") introduction.after(outline);
        else title.after(outline);
        document.body.classList.add("has-page-outline");

        const wide = window.matchMedia("(min-width: 1500px)");
        const fitOutline = () => {
            outline.open = wide.matches;
            summary.tabIndex = wide.matches ? -1 : 0;
        };
        fitOutline();
        wide.addEventListener("change", fitOutline);
        let scheduled = false;
        const locate = () => {
            scheduled = false;
            let current = 0;
            headings.forEach((heading, index) => {
                if (heading.getBoundingClientRect().top <= 150) current = index;
            });
            links.forEach((link, index) => {
                if (index === current) link.setAttribute("aria-current", "location");
                else link.removeAttribute("aria-current");
            });
        };
        window.addEventListener("scroll", () => {
            if (!scheduled) {
                scheduled = true;
                window.requestAnimationFrame(locate);
            }
        }, {passive: true});
        locate();
    }

    // Only overflowing regions join the tab order. Left/Right keep their native
    // scrolling behavior instead of reaching mdBook's chapter shortcuts.
    const regions = [...main.querySelectorAll("pre, .table-wrapper")];
    const measure = () => regions.forEach((region) => {
        const overflow = region.scrollWidth > region.clientWidth + 1;
        if (overflow) {
            region.tabIndex = 0;
            region.setAttribute("role", "region");
            region.setAttribute("aria-label", (region.tagName === "PRE" ? "Code example" : "Table") + "; scroll horizontally with arrow keys");
        } else {
            region.removeAttribute("tabindex");
            region.removeAttribute("role");
            region.removeAttribute("aria-label");
        }
    });
    regions.forEach((region) => region.addEventListener("keydown", (event) => {
        if (event.key === "ArrowLeft" || event.key === "ArrowRight") event.stopPropagation();
    }));
    if (typeof ResizeObserver !== "undefined") {
        const observer = new ResizeObserver(measure);
        regions.forEach((region) => observer.observe(region));
    }
    window.addEventListener("resize", measure, {passive: true});
    if (document.fonts) document.fonts.ready.then(measure);
    measure();
})();
