all: init run

init:
	( \
		python3 -m venv venv; \
		. venv/bin/activate; \
		cat requirements.txt | xargs -n 1 pip install; \
	)

run:
	@(python3 run.py)

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
