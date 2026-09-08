(function () {
    "use strict";

    const MAX_RESULTS = 50;

    function hexValue(value) {
        const digits = String(value).trim().replace(/^0x/i, "");
        if (!/^[0-9a-f]+$/i.test(digits)) return null;
        const normalized = digits.replace(/^0+/, "") || "0";
        if (normalized.length > 8) return null;
        return parseInt(normalized, 16);
    }

    function compareText(left, right) {
        return left < right ? -1 : left > right ? 1 : 0;
    }

    function searchFunctions(functions, query, limit = MAX_RESULTS) {
        const text = String(query).trim().toLowerCase();
        const resultLimit = Number.isFinite(limit)
            ? Math.max(1, Math.min(MAX_RESULTS, Math.floor(limit)))
            : MAX_RESULTS;
        if (!text) return { results: [], total: 0, limit: resultLimit, invalidRva: false };

        const rvaQuery = /^rva\s*:/.test(text);
        const address = hexValue(rvaQuery ? text.replace(/^rva\s*:\s*/, "") : text);
        if (rvaQuery && address === null) {
            return { results: [], total: 0, limit: resultLimit, invalidRva: true };
        }

        const matches = [];
        for (const entry of functions) {
            const name = entry.name.toLowerCase();
            let rank = -1;
            if (rvaQuery) {
                if (hexValue(entry.rva) === address) rank = 0;
            } else if (name === text) {
                rank = 0;
            } else if (address !== null && hexValue(entry.address) === address) {
                rank = 1;
            } else if (name.startsWith(text)) {
                rank = 2;
            } else if (name.includes(text)) {
                rank = 3;
            }
            if (rank !== -1) matches.push({ entry, name, rank });
        }

        matches.sort((left, right) =>
            left.rank - right.rank ||
            compareText(left.name, right.name) ||
            hexValue(left.entry.address) - hexValue(right.entry.address) ||
            compareText(left.entry.url, right.entry.url)
        );
        return {
            results: matches.slice(0, resultLimit).map(match => match.entry),
            total: matches.length,
            limit: resultLimit,
            invalidRva: false,
        };
    }

    function readIndex(element) {
        const data = JSON.parse(element.textContent);
        if (!Array.isArray(data.functions)) throw new Error("Missing function records");
        for (const entry of data.functions) {
            if (!entry || typeof entry.name !== "string" || !entry.name ||
                typeof entry.group !== "string" || typeof entry.conflict !== "boolean" ||
                !/^0x[0-9A-F]{8}$/.test(entry.address) ||
                !/^0x[0-9A-F]{8}$/.test(entry.rva) ||
                typeof entry.url !== "string" || !entry.url ||
                /\s/.test(entry.url) ||
                /^[a-z][a-z0-9+.-]*:|^[\\/]/i.test(entry.url)) {
                throw new Error("Invalid function record");
            }
        }
        return data.functions;
    }

    function addMainSearchLink(document, scriptURL) {
        const wrapper = document.getElementById("mdbook-search-wrapper");
        const searchbar = document.getElementById("mdbook-searchbar");
        if (!wrapper || !searchbar || !scriptURL ||
            document.getElementById("function-lookup-search-link")) return;

        const hint = document.createElement("p");
        hint.className = "function-lookup-search-hint";
        hint.append(document.createTextNode("For function names or addresses, use "));
        const link = document.createElement("a");
        link.id = "function-lookup-search-link";
        link.textContent = "Function lookup";
        hint.append(link, document.createTextNode("."));
        wrapper.prepend(hint);

        function updateLink() {
            // mdBook 0.5 keeps this additional script under theme/, including
            // when the whole book is published beneath a repository prefix.
            const url = new URL("../appendix/functions.html", scriptURL);
            const query = searchbar.value.trim();
            if (query) url.searchParams.set("symbol", query);
            link.href = url.href;
        }
        searchbar.addEventListener("input", updateLink);
        link.addEventListener("click", updateLink);
        updateLink();
    }

    function initializeLookup(document, window) {
        const section = document.getElementById("function-lookup");
        if (!section) return;
        const input = document.getElementById("function-query");
        const status = document.getElementById("function-lookup-status");
        const results = document.getElementById("function-results");
        const embedded = document.getElementById("function-index");
        if (!input || !status || !results) return;

        let functions;
        try {
            if (!embedded) throw new Error("Missing function index");
            functions = readIndex(embedded);
        } catch (_) {
            input.disabled = true;
            status.textContent = "Function lookup is unavailable. Use the function groups below.";
            return;
        }

        function render(updateURL) {
            const query = input.value.trim();
            results.replaceChildren();
            if (updateURL) {
                const url = new URL(window.location.href);
                if (query) url.searchParams.set("symbol", query);
                else url.searchParams.delete("symbol");
                // Keep unrelated parameters and legacy heading fragments intact.
                try { window.history.replaceState(null, "", url.href); } catch (_) { /* Local file URLs may disallow history changes. */ }
            }
            if (!query) {
                status.textContent = functions.length.toLocaleString() +
                    " functions available. Enter a name, a static hexadecimal address, or rva: followed by a hexadecimal RVA.";
                return;
            }

            const found = searchFunctions(functions, query);
            if (found.invalidRva) {
                status.textContent = "Enter a hexadecimal RVA after rva:.";
                return;
            }
            if (!found.total) {
                status.textContent = "No functions match “" + query +
                    "”. Try part of a name; use rva: for a module-relative address.";
                return;
            }
            status.textContent = found.total > found.limit
                ? "Showing " + found.limit + " of " + found.total.toLocaleString() + " matches. Refine the query to see more specific results."
                : found.total.toLocaleString() + (found.total === 1 ? " matching function." : " matching functions.");

            const scroll = document.createElement("div");
            scroll.className = "function-results-scroll";
            scroll.tabIndex = 0;
            scroll.setAttribute("role", "region");
            scroll.setAttribute("aria-label", "Function search results; scroll horizontally on narrow screens");
            scroll.addEventListener("keydown", event => {
                if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
                    event.stopPropagation();
                }
            });
            const table = document.createElement("table");
            const header = table.createTHead().insertRow();
            for (const label of ["Function", "Static VA", "RVA", "Group"]) {
                const cell = document.createElement("th");
                cell.scope = "col";
                cell.textContent = label;
                header.append(cell);
            }
            const body = table.createTBody();
            for (const entry of found.results) {
                const row = body.insertRow();
                const name = row.insertCell();
                const link = document.createElement("a");
                link.className = "function-result-name";
                link.textContent = entry.name;
                link.href = entry.url;
                name.append(link);
                if (entry.conflict) {
                    const conflict = document.createElement("span");
                    conflict.className = "function-result-conflict";
                    conflict.textContent = "Unresolved name/address conflict";
                    name.append(conflict);
                }
                for (const value of [entry.address, entry.rva]) {
                    const cell = row.insertCell();
                    cell.className = "function-result-address";
                    cell.textContent = value;
                }
                row.insertCell().textContent = entry.group;
            }
            scroll.append(table);
            const hint = document.createElement("p");
            hint.className = "function-results-scroll-hint";
            hint.textContent = "Scroll horizontally to see all result columns.";
            results.append(hint, scroll);
        }

        function restoreQuery() {
            input.value = new URL(window.location.href).searchParams.get("symbol") || "";
            render(false);
        }
        input.disabled = false;
        input.addEventListener("input", () => render(true));
        input.addEventListener("keydown", event => {
            if (event.key === "Escape") {
                event.preventDefault();
                input.value = "";
                render(true);
            }
        });
        window.addEventListener("popstate", restoreQuery);
        restoreQuery();
    }

    if (typeof module !== "undefined" && module.exports) {
        module.exports = { searchFunctions, hexValue };
    }
    if (typeof document !== "undefined") {
        const scriptURL = document.currentScript && document.currentScript.src;
        const initialize = () => {
            addMainSearchLink(document, scriptURL);
            initializeLookup(document, window);
        };
        if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialize, { once: true });
        else initialize();
    }
}());
