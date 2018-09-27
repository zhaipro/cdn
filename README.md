# cdn
抓取静态网站

## 爬取效果
```
$ make run
scrapy crawl -L INFO -t sqlite -o webpage.db spider
2018-09-28 08:02:57 [scrapy.utils.log] INFO: Scrapy 1.5.1 started (bot: webpage)
...
2018-09-28 08:34:29 [scrapy.core.engine] INFO: Spider closed (finished)
$
$ du -B G webpage.db
10G     webpage.db
$
$ sqlite3 webpage.db 'select count(*) from page;'
39536
$
