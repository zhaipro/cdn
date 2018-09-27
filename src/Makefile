
run:
	scrapy crawl spider -L INFO -o db.sqlite

clean:
	rm -f db.sqlite db.sqlite-journal
	rm -fr requests.seen requests.queue
	rm -f spider.state

rerun: clean run

runserver:
	export FLASK_DEBUG=1 FLASK_APP=app.py; flask run
