.PHONY: serve
serve:
	python server.py

.PHONY: deps
deps:
	sudo apt-get install python python-pip python-flask
	sudo pip install mimerender
