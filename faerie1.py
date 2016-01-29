from nltk.util import ngrams
import heapq
import math

# shift the candidate window using binary search
def BinaryShift(i,j,Te,Tl,Pe):
	lower = i
	upper = j
	while lower <= upper:
		mid = int(math.ceil((upper+lower)/2))
		if (Pe[j] + (mid - i)) - Pe[mid] + 1 > Te:
			lower = mid + 1
		else:
			upper = mid - 1
	i = lower
	j = i + Tl - 1
	if j>=len(Pe):
		return -1
	if Pe[j] - Pe[i] > up:
		return BinaryShift(i,j,Te,Tl,Pe)
	else:
		return i


n = 2 # ngram num 
threshold = 0.8 # threshold

inverted_list = {}
inverted_index = []
entity_tokennum = {}
inverted_list_len = {}
i = 0
for line in open('testentity.csv'):
	line = line.split('\t')[1]+'_'+line.split('\t')[2]
	entity = line.replace(' ','_').replace(',','').lower().strip()
	inverted_index.append(entity) # record each entity and its id
	tokens = list(ngrams(entity, n))
	entity_tokennum[entity] = len(tokens) # record each entity's token number
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
for line in open('test.csv'):
	#tokenize document, add inverted list(empty) of new tokens in document
	document = line.split('\t')[1].replace(', ','_').replace(' ','_').lower().strip()
	tokens = list(ngrams(document, n))
	heap = []
	los = len(tokens)
	# build the heap
	for i in xrange(los):
		try:
			heap.append([inverted_list[tokens[i]][0],i])
		except KeyError:
			pass
	if heap != []:
		result = []
		heapq.heapify(heap);
		e = heap[0][0] #current entity, the top entity in heap
		loe = entity_tokennum[inverted_index[e]]
		Pe = [] #opsition list
		low = int(math.ceil(loe * threshold)) #lower boundary for current entity
		up = int(math.floor(loe / threshold)) #upper boundary for current entity
		V = [[0 for col in xrange(low,up+1)] for row in xrange(los)] #occurence matrix for entity
		current_index = [0 for col in xrange(0,los)]
		while 1:
			ei = heap[0][0] #top of the heap entity
			pi = heap[0][1] #the top entity's position in document
			if(ei == 237392 or pi == -1):
				print document,result
				break
			if(ei == e):
				Pe.append(pi)
				for l in xrange(0,up-low+1):
					if pi-(l+low)+1 <= 0:
						k = 0
					else:
						k = pi-(l+low)+1 
					for i in xrange(k,pi+1):
						V[i][l] += 1
			else:
				Pe.sort()
				# if len(Pe) == low:
				# 	slen = Pe[low-1] - Pe[0] + 1
				# 	if(low<=slen and slen<=up):
				# 		T = int(math.ceil((loe+los)*(threshold/(1+threshold))))
				# 		if (V[Pe[0]][slen-low] >= T):
				# 			result.append((inverted_index[e],document[Pe[0]:Pe[low-1]+2]))
				if len(Pe) >= low:
					i = 0
					while (i<=len(Pe)-low):
						j = i + low -1
						if(Pe[j]-Pe[i]<=up):
							#Binary Span
							lower = j;
							upper = i+up-1;
							if upper>=len(Pe):
								upper = len(Pe)-1
							while(lower<=upper):
								mid = int(math.ceil((upper+lower)/2))
								if(Pe[mid]-Pe[i]+1>up):
 									upper = mid - 1;
								else:
									lower = mid + 1;
							if (upper>=len(Pe)-1):
								upper = len(Pe)-1
								slen = Pe[upper] - Pe[i] + 1
								if(low<=slen and slen<=up):
									T = int(math.ceil((loe+los)*(threshold/(1+threshold))))
									if (V[Pe[i]][slen-low] >= T):
										result.append((inverted_index[e],(Pe[i],Pe[upper]+2),document[Pe[i]:Pe[upper]+2]))
								break
							slen = Pe[upper] - Pe[i] + 1
							if(low<=slen and slen<=up):
								T = int(math.ceil((loe+los)*(threshold/(1+threshold))))
								if (V[Pe[i]][slen-low] >= T):
									result.append((inverted_index[e],document[Pe[i]:Pe[upper]+2]))
							i+=1
						else:
							i = BinaryShift(i,j,up,low,Pe)
							if i == -1:
								break
				e = ei
				Pe = [pi]
				loe = entity_tokennum[inverted_index[e]]
				low = int(math.ceil(loe * threshold))
				up = int(math.floor(loe / threshold))
				V = [[0 for col in xrange(low,up+1)] for row in xrange(los)]
			if (current_index[pi]+1)<inverted_list_len[tokens[pi]]:
				current_index[pi] += 1
				heapq.heapreplace(heap,[inverted_list[tokens[pi]][current_index[pi]],pi])
			else:
				heapq.heapreplace(heap,[237392,-1])


