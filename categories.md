---
layout: default
title: "分類總覽"
permalink: /categories/
---

<link rel="stylesheet" href="/assets/css/custom.css">

<h1 style="font-size: 2rem; font-weight: 800; margin-bottom: 1.5rem;">文章分類總覽</h1>

<div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 2rem;">
  <a href="#insights" class="post-category-tag" style="text-decoration: none; padding: 6px 12px; font-size: 0.9rem;">💡 心得記錄</a>
  <a href="#build-log" class="post-category-tag" style="text-decoration: none; padding: 6px 12px; font-size: 0.9rem;">🛠️ 實作日誌</a>
  <a href="#life-and-trails" class="post-category-tag" style="text-decoration: none; padding: 6px 12px; font-size: 0.9rem;">🌲 生活點滴</a>
  <a href="#speculations" class="post-category-tag" style="text-decoration: none; padding: 6px 12px; font-size: 0.9rem;">🌌 科學猜想</a>
  <a href="#uncategorized" class="post-category-tag" style="text-decoration: none; padding: 6px 12px; font-size: 0.9rem;">📦 其他</a>
</div>

{% assign categories = "insights,build-log,life-and-trails,speculations,uncategorized" | split: "," %}

{% for cat in categories %}
  <div id="{{ cat }}" style="margin-top: 3rem; scroll-margin-top: 2rem;">
    <h2 style="font-size: 1.4rem; font-weight: 700; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; margin-bottom: 1rem;">
      {% case cat %}
        {% when "insights" %}💡 心得記錄 (Insights)
        {% when "build-log" %}🛠️ 實作日誌 (Build Log)
        {% when "life-and-trails" %}🌲 生活點滴 (Life & Trails)
        {% when "speculations" %}🌌 科學猜想 (Speculations)
        {% else %}📦 其他 (Uncategorized)
      {% endcase %}
    </h2>

    <ul class="post-list">
      {% assign posts_in_cat = site.categories[cat] %}
      {% for post in posts_in_cat %}
        <li class="post-item">
          <div class="post-meta">
            <span>{{ post.date | date: "%Y-%m-%d" }}</span>
          </div>
          <a class="post-link" href="{{ post.url }}">{{ post.title }}</a>
        </li>
      {% else %}
        <p style="color: #64748b; font-size: 0.9rem;">目前此分類尚無文章。</p>
      {% endfor %}
    </ul>
  </div>
{% endfor %}
