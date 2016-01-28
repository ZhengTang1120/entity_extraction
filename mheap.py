from nltk.util import ngrams
import faerie
import gc

n = 2 # ngram num 
threshold = 0.8 # threshold

inverted_list = {}
inverted_index = []
entity_tokennum = {}
inverted_list_len = {}
i = 0
maxenl = 0
for line in open('testentity.csv'):
	line = line.split('\t')[1]+'_'+line.split('\t')[2]
	entity = line.replace(' ','_').replace(',','').lower().strip()
	inverted_index.append(entity) # record each entity and its id
	tokens = list(ngrams(entity, n))
	entity_tokennum[entity] = len(tokens) # record each entity's token number
	if maxenl<len(tokens):
		maxenl = len(tokens)
	# build inverted lists for tokens
	tokens = list(set(tokens))
	for token in tokens:
		try:
			inverted_list[token].append(i)
			inverted_list_len[token] += 1
		except KeyError:
			inverted_list[token] = []
			inverted_list[token].append(i)	
			inverted_list_len[token] = 1	
	i = i + 1	

for line in open('ht-sample-locations.csv'):
	#tokenize document, add inverted list(empty) of new tokens in document
	document = line.split('\t')[1].replace(', ','_').replace(' ','_').lower().strip()
	tokens = list(ngrams(document, n))
	heap = []
	los = len(tokens)
	# build the heap
	for i in range(los):
		try:
			heap.append([inverted_list[tokens[i]][0],i])
		except KeyError:
			pass
	if heap != []:
		print (document)
		faerie.getcandidates(heap,entity_tokennum,inverted_list_len,inverted_index,inverted_list,tokens,los,maxenl)
		# print inverted_index[0]
