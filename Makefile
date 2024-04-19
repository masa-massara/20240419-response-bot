PYTHON	= python
PYDOC	= pydoc
MODULE	= terminal_bot
TARGET	= $(MODULE).py
TARGETS	= \
	'./dialogue_system/dialogue_management/reference.py' \
	'./dialogue_system/dialogue_management/dialogue_manager.py' \
	'./dialogue_system/dialogue_management/internal_state.py' \
	'./dialogue_system/dialogue_management/responder.py' \
	'./dialogue_system/agent.py' \
	'./dialogue_system/response_generation/response_generator.py' \
	'./dialogue_system/utterance_analysis/utterance_analyzer.py' \
	'./application/terminal_bot.py'
ARCHIVE	= $(shell basename `pwd`)
WORKDIR	= ./application/
PYLINTRST	= pylintresult.txt
FLAKE8RST	= flake8result.txt
REQUIREMENTS	= requirements.txt

all:
	@:

edit:
	@if [ -e "/Applications/Visual Studio Code.app" ] ; then echo 'open -a "Visual Studio Code" .' ; open -a "Visual Studio Code" . ; fi

wipe: clean
	@if [ -e ../$(ARCHIVE).zip ] ; then echo "rm -f ../$(ARCHIVE).zip" ; rm -f ../$(ARCHIVE).zip ; fi
	@if [ -e ../$(ARCHIVE).tar ] ; then echo "rm -f ../$(ARCHIVE).tar" ; rm -f ../$(ARCHIVE).tar ; fi

clean:
	@find . -type f -name ".DS_Store" -print -exec rm -f {} ";" -exec echo rm -f {} ";"
	@find . -type f -name "*.pyc" -exec rm -f {} ";" -exec echo rm -f {} ";"
	@find . -type d -name "__pycache__" -exec rm -rf {} ";" -exec echo rm -rf {} ";"
	@if [ -e $(PYLINTRST) ] ; then echo "rm -f $(PYLINTRST)" ; rm -f $(PYLINTRST) ; fi
	@if [ -e $(FLAKE8RST) ] ; then echo "rm -f $(FLAKE8RST)" ; rm -f $(FLAKE8RST) ; fi

test:
	@cd $(WORKDIR) ; $(PYTHON) ./$(TARGET)

doc:
	@cd $(WORKDIR) ; $(PYDOC) ./$(TARGET)

zip: clean
	@if [ -e ../$(ARCHIVE).zip ] ; then echo "rm -f ../$(ARCHIVE).zip" ; rm -f ../$(ARCHIVE).zip ; fi
	cd ../ ; zip -r ./$(ARCHIVE).zip ./$(ARCHIVE)/ --exclude='*/.git/*' --exclude='*/.svn/*' --exclude='*/.python-version' --exclude='*/.tool-versions'

tar: clean
	@if [ -e ../$(ARCHIVE).tar ] ; then echo "rm -f ../$(ARCHIVE).tar" ; rm -f ../$(ARCHIVE).tar ; fi
	cd ../ ; tar -cvf ./$(ARCHIVE).tar --exclude='*/.git/*' --exclude='*/.svn/*' --exclude='*/.python-version' --exclude='*/.tool-versions' ./$(ARCHIVE)/

pydoc:
	(sleep 5 ; open http://localhost:9999/index.html) & cd $(WORKDIR) ; $(PYDOC) -p 9999

lint:
	pylint --exit-zero --max-line-length 200 --reports y $(TARGETS) > $(PYLINTRST)
	flake8 --exit-zero --max-line-length 200 --statistics $(TARGETS) > $(FLAKE8RST)
	@less $(PYLINTRST)
	@less $(FLAKE8RST)

pip:
	pip install -U pip

requirements:
	pip install --no-cache-dir -r ./$(REQUIREMENTS)

prepare: pip requirements

update: prepare
