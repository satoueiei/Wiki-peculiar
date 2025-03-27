// 記事データをJekyllから取得するためにJSONを生成
var articles = [{% for article in site.articles %}{"title": "{{ article.title | escape }}", "url": "{{ article.url | escape }}", "content": {{ article.content | strip_html | jsonify }}}{% unless forloop.last %},{% endunless %}{% endfor %}];

// Lunrインデックスを作成
var idx = lunr(function () {
  this.ref('url');
  this.field('title');
  this.field('content');
  articles.forEach(function (doc) {
    this.add(doc);
  }, this);
});

// 検索機能の実装
document.addEventListener('DOMContentLoaded', function() {
  var searchInput = document.getElementById('search');
  var resultsDiv = document.getElementById('results');
  searchInput.addEventListener('input', function() {
    var query = this.value;
    var results = idx.search(query);
    resultsDiv.innerHTML = '';
    results.forEach(function(result) {
      var article = articles.find(a => a.url === result.ref);
      var li = document.createElement('li');
      li.innerHTML = `<a href="${article.url}">${article.title}</a>`;
      resultsDiv.appendChild(li);
    });
  });
});