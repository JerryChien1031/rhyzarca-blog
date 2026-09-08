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
            '<a href="/p/about.html" class="nav-link">關於我</a>' +
            '<a href="/search/label/insights" class="nav-link">心得記錄 (Insights)</a>' +
            '<a href="/search/label/architecture" class="nav-link">系統日誌 (Architecture)</a>' +
            '<a href="/search/label/embodied" class="nav-link">生活體驗 (Embodied)</a>' +
            '<a href="/search/label/speculations" class="nav-link">科學思辨 (Speculations)</a>' +
            '</div>';
        header.parentNode.insertBefore(nav, header.nextSibling);
    }

    // Only owner links in the Profile gadget / author byline, not reader comments.
    document.querySelectorAll('.widget.Profile a[href], .post-author a[href]').forEach(function (link) {
        var url = new URL(link.href, window.location.href);
        if (url.hostname === 'www.blogger.com' && url.pathname === '/profile/03091466585665229711') {
            link.href = '/p/about.html';
            link.classList.remove('g-profile');
            if (link.classList.contains('profile-link')) link.textContent = '關於 Jerry Chien';
        }
    });

    /* 2. 取得文章主體容器 */
    var postBody = document.querySelector(".post-body, .entry-content");
    if (postBody) {
        if (window.location.pathname === "/p/about.html") postBody.classList.add("about-profile");
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

/* ==========================================================================
   AEO / GEO: 動態注入 TechArticle 結構化資料 (Schema.org JSON-LD)
   ========================================================================== */
function injectStructuredData() {
    var path = window.location.pathname;
    var isStaticPage = /^\/p\/[^/]+\.html$/.test(path);
    var isSinglePost = /^\/\d{4}\/\d{2}\/[^/]+\.html$/.test(path);
    var aboutUrl = 'https://blog.rhyzarca.com/p/about.html';
    var person = {
        '@type': 'Person', '@id': aboutUrl + '#jerry-chien',
        name: 'Jerry Chien', jobTitle: 'Cognitive System Architect', url: aboutUrl
    };
    // The live theme emits a standalone BlogPosting even on non-article pages.
    // Normalize only this site's Jerry Chien article nodes, preserving other schema.
    document.querySelectorAll('script[type="application/ld+json"]').forEach(function (node) {
        if (node.id === 'rhyzarca-structured-data') return;
        try {
            function clean(value) {
                if (Array.isArray(value)) return value.map(clean).filter(Boolean);
                if (!value || typeof value !== 'object') return value;
                var types = [].concat(value['@type'] || []);
                if (types.some(function (t) { return ['BlogPosting', 'TechArticle', 'Article'].includes(t); }) &&
                    value.author && value.author.name === 'Jerry Chien') {
                    if (!isSinglePost) return null;
                    value.author = Object.assign({}, value.author, person);
                }
                if (value['@graph']) value['@graph'] = clean(value['@graph']);
                return value;
            }
            var cleaned = clean(JSON.parse(node.textContent));
            if (cleaned) node.textContent = JSON.stringify(cleaned);
            else node.remove();
        } catch (error) { /* Leave unrelated or invalid theme data untouched. */ }
    });
    if (document.getElementById('rhyzarca-structured-data')) return;
    if (isStaticPage && path === '/p/about.html') {
        person.sameAs = ['https://github.com/JerryChien1031',
            'https://www.blogger.com/profile/03091466585665229711'];
        var profile = document.createElement('script');
        profile.id = 'rhyzarca-structured-data';
        profile.type = 'application/ld+json';
        profile.textContent = JSON.stringify({
            '@context': 'https://schema.org', '@type': 'ProfilePage',
            url: aboutUrl, mainEntity: person
        });
        document.head.appendChild(profile);
        return;
    }
    if (!isSinglePost) return;

    var postTitle = document.querySelector(".post-title, h1.entry-title");
    var postBody = document.querySelector(".post-body, .entry-content");
    var postDate = document.querySelector(".published, .date-header");

    if (!postTitle || !postBody) return;

    var schemaData = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": postTitle.innerText.trim(),
        "inLanguage": "zh-TW",
        "author": person,
        "publisher": {
            "@type": "Organization",
            "name": "Rhyzarca",
            "url": "https://blog.rhyzarca.com",
            "logo": {
                "@type": "ImageObject",
                "url": "https://blog.rhyzarca.com/favicon.ico"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": window.location.href
        },
        "description": document.querySelector('meta[name="description"]') 
            ? document.querySelector('meta[name="description"]').getAttribute("content") 
            : postBody.innerText.substring(0, 160).trim()
    };

    var script = document.createElement("script");
    script.id = "rhyzarca-structured-data";
    script.type = "application/ld+json";
    script.text = JSON.stringify(schemaData);
    document.head.appendChild(script);
}
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectStructuredData);
} else {
    injectStructuredData();
}
