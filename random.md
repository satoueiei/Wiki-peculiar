---
layout: null
---
{% assign random_article = site.articles | sample %}
<meta http-equiv="refresh" content="0; url={{ random_article.url }}">