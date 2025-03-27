---
layout: default
---
# 架空のWikipedia記事一覧

<ul>
{% for article in site.articles %}
  <li><a href="{{ site.baseurl }}{{ article.url }}">{{ article.title }}</a></li>
{% endfor %}
</ul>
<input type="text" id="search" placeholder="記事を検索...">
<ul id="results"></ul>

<script src="/assets/js/lunr.min.js"></script>
<script src="/assets/js/search.js"></script>
<a href="/random">ランダム記事へ</a>