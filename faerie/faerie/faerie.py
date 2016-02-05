from nltk.util import ngrams
import singleheap
import json
import sys

def run(dictfile,inputfile,n=2,threshold=0.8):

	inverted_list = {}
	inverted_index = []
	entity_tokennum = {}
	inverted_list_len = {}
	entity_realid = {}
	entity_real = {}
	i = 0
	maxenl = 0
	for line in open(dictfile):
		entity_realid[i] = line.split("\t")[0]
		line = line.split('\t')[1]+'_'+line.split('\t')[2]
		entity_real[i] = line.strip()
		entity = line.replace(' ','_').replace(',','').lower().strip()
		inverted_index.append(entity) # record each entity and its id
		tokens = list(ngrams(entity, n))
		entity_tokennum[entity] = len(tokens) # record each entity's token number
		if maxenl<len(tokens):
			maxenl = len(tokens)
		# build inverted lists for tokens
		tokens = list(set(tokens))
		for token in tokens:
			token = str(token)
			try:
				inverted_list[token].append(i)
				inverted_list_len[token] += 1
			except KeyError:
				inverted_list[token] = []
				inverted_list[token].append(i)	
				inverted_list_len[token] = 1	
		i = i + 1

	for line in open(inputfile):
		#tokenize document, add inverted list(empty) of new tokens in document
		document = line.split('\t')[1].replace(', ','_').replace(' ','_').lower().strip()
		jsonline = {}
		jsonline["document"] = {}
		jsonline["document"]["id"] = line.split('\t')[0]
		jsonline["document"]["value"] = line.split('\t')[1].strip()
		jsonline["entities"] = {}
		tokens = list(ngrams(document, n))
		heap = []
		keys = []
		los = len(tokens)
		# build the heap
		for i, token in enumerate(tokens):
			key = str(token)
			keys.append(key)
			try:
				heap.append([inverted_list[key][0],i])
			except KeyError:
				pass
		if heap != []:
			returnValuesFromC = singleheap.getcandidates(heap,entity_tokennum,inverted_list_len,inverted_index,inverted_list,keys,los,maxenl)
			for value in returnValuesFromC:
				temp = {}
				temp["start"] = value[1]
				temp["end"] = value[2]
				temp["score"] = value[3]
				try:
					jsonline["entities"][entity_realid[value[0]]]["candwins"].append(temp)
				except KeyError:
					jsonline["entities"][entity_realid[value[0]]] = {}
					jsonline["entities"][entity_realid[value[0]]]["value"] = entity_real[value[0]]
					jsonline["entities"][entity_realid[value[0]]]["candwins"] = [temp]
		print json.dumps(jsonline)