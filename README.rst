entity_extraction
===================

This is an implementation of faeire entity extraction, a dictionary-baesd entity extraction.

For install:
---------------------

pre-request:

you need to install nltk and its data:

1.run 
::
	sudo pip install -U nltk to install nltk

2.run 
::
	python and type these commands:
::
	>>> import nltk
	>>> nltk.download()

3.run sudo pip install faerie

Usage:
--------------------

Input format is <id><\t><string> for both dictionary and documents

run 
::
	faerie.run(dictionary,documents,ngram(optional),threshold(optional)) 
to run the entity extraction. 

Current output is a json line:
-------------------------------------

{"entities": {entity id: {"value": entity value, "candwins": [{"start": #, "score": #, "end": #}]}}, "document": {"id": document id, "value": document value}}
