/* ==========================================================================
   Rhyzarca Blog Client Script (Auto TOC & UI Enhancements)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
    /* 1. 自動在頁首 Header 下方注入分類導覽列 */
    var header = document.querySelector(".header-outer, #header, .header, header, .Header");
    if (header && !document.getElementById("rhyzarca-nav")) {
        var nav = document.createElement("nav");
        nav.id = "rhyzarca-nav";
        nav.innerHTML = '<div class="nav-container">' +
            '<a href="/" class="nav-link">首頁</a>' +
            '<a href="/search/label/insights" class="nav-link">心得記錄 (Insights)</a>' +
            '<a href="/search/label/architecture" class="nav-link">系統日誌 (Architecture)</a>' +
            '<a href="/search/label/embodied" class="nav-link">肉身感知 (Embodied)</a>' +
            '<a href="/search/label/speculations" class="nav-link">科學思辨 (Speculations)</a>' +
            '</div>';
        header.parentNode.insertBefore(nav, header.nextSibling);
    }

    /* 2. 取得文章主體容器 */
    var postBody = document.querySelector(".post-body, .entry-content");
    if (!postBody) {
        return;
    }

    /* 3. 自動掃描 H2 生成目錄 (若已有目錄則不重複執行) */
    var headings = postBody.querySelectorAll("h2");
    if (headings.length >= 2 && !document.getElementById("rhyzarca-toc")) {
        var tocContainer = document.createElement("div");
        tocContainer.id = "rhyzarca-toc";
        tocContainer.innerHTML = '<div class="toc-title">📑 本文目錄</div>';

        var tocList = document.createElement("ul");

        headings.forEach(function (heading, index) {
            /* 若 H2 原本已有 ID 則保留，否則自動生成 */
            var headingId = heading.id ? heading.id : ("section-" + index);
            heading.id = headingId;

            var li = document.createElement("li");
            var link = document.createElement("a");
            link.href = "#" + headingId;
            link.textContent = heading.textContent;
            li.appendChild(link);
            tocList.appendChild(li);
        });

        tocContainer.appendChild(tocList);

        /* 插入在第一個 H2 標題之前 */
        headings[0].parentNode.insertBefore(tocContainer, headings[0]);
    }

    /* 4. 外部連結自動開新視窗 (target="_blank") */
    var links = postBody.querySelectorAll("a");
    links.forEach(function (link) {
        if (link.hostname && link.hostname !== window.location.hostname) {
            link.setAttribute("target", "_blank");
            link.setAttribute("rel", "noopener noreferrer");
        }
    });
});
