/* ==========================================================================
   Rhyzarca Blog Client Script (Nav, TOC & Sovereign Footers)
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
            '<a href="/search/label/embodied" class="nav-link">生活體驗 (Embodied)</a>' +
            '<a href="/search/label/speculations" class="nav-link">科學思辨 (Speculations)</a>' +
            '</div>';
        header.parentNode.insertBefore(nav, header.nextSibling);
    }

    /* 2. 取得文章主體容器 */
    var postBody = document.querySelector(".post-body, .entry-content");
    if (postBody) {
        /* 3. 自動掃描 H2 生成目錄 (TOC) */
        var headings = postBody.querySelectorAll("h2");
        if (headings.length >= 2 && !document.getElementById("rhyzarca-toc")) {
            var tocContainer = document.createElement("div");
            tocContainer.id = "rhyzarca-toc";
            tocContainer.innerHTML = '<div class="toc-title">📑 本文目錄</div>';

            var tocList = document.createElement("ul");

            headings.forEach(function (heading, index) {
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
    }

    /* 5. 自動在全站頁尾注入版權保護與主權聲明 (Footer) */
    if (!document.getElementById("rhyzarca-footer")) {
        var footer = document.createElement("footer");
        footer.id = "rhyzarca-footer";
        footer.innerHTML = '<div class="footer-container">' +
            '<div class="footer-brand">🏛️ Rhyzarca Sovereign Epistemic Blog</div>' +
            '<div class="footer-copyright">© 2026 <strong>Jerry Chien</strong>. All Rights Reserved.</div>' +
            '<div class="footer-license">' +
            '本站文章思想與分錄依據 <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener noreferrer">CC BY-NC-SA 4.0</a> 條款釋出。' +
            '<br>所有認知軌跡皆具備確定性版本溯源與主權防禦邊界。' +
            '</div>' +
            '<div class="footer-links">' +
            '<a href="https://github.com/jerrychien1031/rhyzarca-blog" target="_blank" rel="noopener noreferrer">GitHub 原始碼</a>' +
            '<span class="footer-sep">·</span>' +
            '<a href="https://blog.rhyzarca.com/atom.xml?redirect=false&start-index=1&max-results=500" target="_blank">Atom RSS 訂閱</a>' +
            '<span class="footer-sep">·</span>' +
            '<a href="https://blog.rhyzarca.com/">返回首頁</a>' +
            '</div>' +
            '</div>';

        var footerContainer = document.querySelector(".footer-outer, #footer, footer, .content-inner");
        if (footerContainer) {
            footerContainer.appendChild(footer);
        } else {
            document.body.appendChild(footer);
        }
    }
});
