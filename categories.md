---
layout: default
title: "文章分類總覽"
permalink: /categories/
---
<link rel="stylesheet" href="{{ '/assets/css/custom.css' | relative_url }}">
<h1>文章分類總覽</h1>
<p>依文章主要目的尋找內容；有完整交集的文章可出現在多個入口。完成程度不由分類名稱保證，請以正文說明為準。</p>
<nav aria-label="文章分類" style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:2rem;">
{% for category in site.data.blog_categories %}
  <a class="post-category-tag" href="#{{ category.id }}">{{ category.name }}</a>
{% endfor %}
</nav>
{% for category in site.data.blog_categories %}
{% for alias in category.aliases %}<span id="{{ alias }}" aria-hidden="true"></span>{% endfor %}
<section id="{{ category.id }}" style="margin-top:2.5rem;scroll-margin-top:2rem;">
  <h2>{{ category.name }} ({{ category.english }})</h2>
  <p>{{ category.summary }}</p>
  <ul class="post-list">
    {% assign category_posts = site.categories[category.id] %}
    {% for post in category_posts %}
      <li class="post-item"><div class="post-meta">{{ post.date | date: "%Y-%m-%d" }}</div><a class="post-link" href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
    {% else %}
      <li class="post-item">目前此分類尚無文章。</li>
    {% endfor %}
  </ul>
</section>
{% endfor %}
