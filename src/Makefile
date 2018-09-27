
run:
	scrapy crawl -L INFO -t sqlite -o webpage.db spider

clean:
	rm -f webpage.db webpage.db-journal
	rm -fr requests.seen requests.queue
	rm -f spider.state

rerun: clean run

runserver:
	export FLASK_DEBUG=1 FLASK_APP=app.py; flask run
