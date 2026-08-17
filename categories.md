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

<!-- 💡 心得記錄 -->
<div id="insights" style="margin-top: 2.5rem; scroll-margin-top: 2rem;">
  <h2 style="font-size: 1.4rem; font-weight: 700; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; margin-bottom: 1rem;">
    💡 心得記錄 (Insights)
  </h2>
  <ul class="post-list">
    {% assign insight_posts = site.posts | where_exp: "item", "item.categories contains 'insights'" %}
    {% for post in insight_posts %}
      <li class="post-item">
        <div class="post-meta">
          <span>{{ post.date | date: "%Y-%m-%d" }}</span>
        </div>
        <a class="post-link" href="{{ post.url }}">{{ post.title }}</a>
      </li>
    {% else %}
      <li class="post-item" style="color: #64748b; font-size: 0.9rem;">目前此分類尚無文章。</li>
    {% endfor %}
  </ul>
</div>

<!-- 🛠️ 實作日誌 -->
<div id="build-log" style="margin-top: 2.5rem; scroll-margin-top: 2rem;">
  <h2 style="font-size: 1.4rem; font-weight: 700; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; margin-bottom: 1rem;">
    🛠️ 實作日誌 (Build Log)
  </h2>
  <ul class="post-list">
    {% assign build_posts = site.posts | where_exp: "item", "item.categories contains 'build-log'" %}
    {% for post in build_posts %}
      <li class="post-item">
        <div class="post-meta">
          <span>{{ post.date | date: "%Y-%m-%d" }}</span>
        </div>
        <a class="post-link" href="{{ post.url }}">{{ post.title }}</a>
      </li>
    {% else %}
      <li class="post-item" style="color: #64748b; font-size: 0.9rem;">目前此分類尚無文章。</li>
    {% endfor %}
  </ul>
</div>

<!-- 🌲 生活點滴 -->
<div id="life-and-trails" style="margin-top: 2.5rem; scroll-margin-top: 2rem;">
  <h2 style="font-size: 1.4rem; font-weight: 700; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; margin-bottom: 1rem;">
    🌲 生活點滴 (Life & Trails)
  </h2>
  <ul class="post-list">
    {% assign life_posts = site.posts | where_exp: "item", "item.categories contains 'life-and-trails'" %}
    {% for post in life_posts %}
      <li class="post-item">
        <div class="post-meta">
          <span>{{ post.date | date: "%Y-%m-%d" }}</span>
        </div>
        <a class="post-link" href="{{ post.url }}">{{ post.title }}</a>
      </li>
    {% else %}
      <li class="post-item" style="color: #64748b; font-size: 0.9rem;">目前此分類尚無文章。</li>
    {% endfor %}
  </ul>
</div>

<!-- 🌌 科學猜想 -->
<div id="speculations" style="margin-top: 2.5rem; scroll-margin-top: 2rem;">
  <h2 style="font-size: 1.4rem; font-weight: 700; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; margin-bottom: 1rem;">
    🌌 科學猜想 (Speculations)
  </h2>
  <ul class="post-list">
    {% assign spec_posts = site.posts | where_exp: "item", "item.categories contains 'speculations'" %}
    {% for post in spec_posts %}
      <li class="post-item">
        <div class="post-meta">
          <span>{{ post.date | date: "%Y-%m-%d" }}</span>
        </div>
        <a class="post-link" href="{{ post.url }}">{{ post.title }}</a>
      </li>
    {% else %}
      <li class="post-item" style="color: #64748b; font-size: 0.9rem;">目前此分類尚無文章。</li>
    {% endfor %}
  </ul>
</div>

<!-- 📦 其他 -->
<div id="uncategorized" style="margin-top: 2.5rem; scroll-margin-top: 2rem;">
  <h2 style="font-size: 1.4rem; font-weight: 700; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; margin-bottom: 1rem;">
    📦 其他 (Uncategorized)
  </h2>
  <ul class="post-list">
    {% assign other_posts = site.posts | where_exp: "item", "item.categories contains 'uncategorized'" %}
    {% for post in other_posts %}
      <li class="post-item">
        <div class="post-meta">
          <span>{{ post.date | date: "%Y-%m-%d" }}</span>
        </div>
        <a class="post-link" href="{{ post.url }}">{{ post.title }}</a>
      </li>
    {% else %}
      <li class="post-item" style="color: #64748b; font-size: 0.9rem;">目前此分類尚無文章。</li>
    {% endfor %}
  </ul>
</div>
