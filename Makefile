run:
	export PWD=/home/khais/src/github/dragon-rpg/src; python src/main.py

commit:
	git status
	git diff

style:
	black src -q
#	pylint -f colorized src/main.py -s yes --exit-zero
	flake8 --max-complexity=5 --exit-zero --show-source
	bandit src/main.py -q
