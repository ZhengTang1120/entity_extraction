# entity_extraction

This is an implementation of faeire entity extraction, a dictionary-baesd entity extraction.

Run "sudo python setup.py install", you can install faerie.c in your python lib

Run "python mheap.py <dictionary file> <documents file>", run the extraction

You can check the dictionary format and document format by looking at sample input.

Current output is a json line:
{"entities": {entity id: {"value": entity value, "candwins": [{"start": #, "score": #, "end": #}]}}, "document": {"id": document id, "value": document value}}
