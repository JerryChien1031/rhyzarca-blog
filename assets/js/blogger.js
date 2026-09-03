/* ==========================================================================
   Rhyzarca Blog Client Script (Auto TOC & UI Enhancements)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
    const postBody = document.querySelector(".post-body, .entry-content");
    if (!postBody) return;

    // 1. 自動掃描 H2 生成目錄
    const headings = postBody.querySelectorAll("h2");
    if (headings.length >= 2) {
        const tocContainer = document.createElement("div");
        tocContainer.id = "rhyzarca-toc";
        tocContainer.innerHTML = '<div class="toc-title">📑 本文目錄</div>';
        
        const tocList = document.createElement("ul");

        headings.forEach((heading, index) => {
            const headingId = "section-" + index;
            heading.id = headingId;

            const li = document.createElement("li");
            const link = document.createElement("a");
            link.href = "#" + headingId;
            link.textContent = heading.textContent;
            li.appendChild(link);
            tocList.appendChild(li);
        });

        tocContainer.appendChild(tocList);

        // 插入在第一個 H2 之前
        headings[0].parentNode.insertBefore(tocContainer, headings[0]);
    }

    // 2. 外部連結自動開新視窗 (target="_blank")
    const links = postBody.querySelectorAll("a");
    links.forEach(link => {
        if (link.hostname !== window.location.hostname && link.hostname !== "") {
            link.setAttribute("target", "_blank");
            link.setAttribute("rel", "noopener noreferrer");
        }
    });
});
