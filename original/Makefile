work:
	ls
	./workflow.sh

clean:
	make regraph
	rm -rf __pycache__ *.jack493 *.pyc
	ls

analyze:
	make encourage
	make regraph
	python3 analyze.py

regraph:
	rm -f *.png

encourage:
	cat words_of_encouragement | cowsay | lolcat

bert:
	python3 initwrite.py exemplar/99M99/99M99.txt
	mv pickled_data.jack493 bert.jack493

data:
	python3 initwrite.py JACK493data/*/*.txt

reset:
	cat restart_words | cowsay | lolcat
	make clean
	make bert
	make data

rerun:
	make reset
	make analyze