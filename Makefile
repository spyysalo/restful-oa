.PHONY: serve
serve:
	python app.py

.PHONY: deps
deps:
	sudo apt-get install python python-pip python-flask
	sudo pip install mimerender
