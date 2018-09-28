# cdn
抓取静态网站

## 爬取效果
```
$ make run
scrapy crawl spider -L INFO -o db.sqlite
2018-09-28 08:02:57 [scrapy.utils.log] INFO: Scrapy 1.5.1 started (bot: crawler)
...
2018-09-28 08:34:29 [scrapy.core.engine] INFO: Spider closed (finished)
$
$ du -B G db.sqlite
10G     db.sqlite
$
$ sqlite3 db.sqlite 'select count(*) from page;'
39536
$
$ make runserver
export FLASK_DEBUG=1 FLASK_APP=app.py; flask run
...
127.0.0.1 - - [28/Sep/2018 08:35:26] "GET / HTTP/1.1" 200 -
...
```
