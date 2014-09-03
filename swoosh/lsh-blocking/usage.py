from newlsh import barelsh
import numpy as np
import random
import time


def load_docs(doclist):
	docs = []
	print 'doc number: ' + str(len(doclist))
	for doc in doclist:
		try:
			fp = open(doc)
			content = fp.read()
			tokens = content.split()
			docs.append(tokens)
			fp.close()
		except:
			print 'error: [load_docs]'
	return docs


def load_dataset(filename):
	docs = []
	try:
		fp = open(filename)
		docs = [line.strip().split() for line in fp]
		fp.close()
	except:
		print 'error: [load_dataset]'
	return docs


def load_cora(filename):
	docs = []
	answers = []
	try:
		fp = open(filename)
		docs = [line.strip().split('\t')[2:] for line in fp]
		fp.close()
		fp = open(filename)
		answers = [line.strip().split('\t')[1].replace('"', '') for line in fp]
		fp.close()
	except:
		print 'error: [load_cora] from "' + filename + '"'

	for i in range(len(docs)):
		tmp = docs[i]
		docs[i] = ''
		for part in tmp:
			docs[i] += part + ' '
		docs[i] = docs[i].strip()
	return docs, answers


class SignatureBuilder:

	def __init__(self, n=100, max_shingle=3, rand_inf=10000, rand_sup=99999):
		self.n = n # n: dimension number of signature
		self.max_shingle = max_shingle # max_shingle: how many chars(or words) a shingle contains
		self.rand_inf = rand_inf # rand_inf: the lower bound param for generate hash funcs
		self.rand_sup = rand_sup # rand_sup: the upper bound param for generate hash funcs
		assert self.max_shingle > 0, 'error: [SignatureBuilder] max_shingle must be greater than 0'

		self._shingles = {} # maps from words or sequences of words to integers
		self._counter = 0 # the global counter for word indicies in _shingles

		self.shgvec = [] # contains shingle vectors of the dataset
		self.signatures = [] # contains signatures of the dataset
		self.loadflag = 0 # if the dataset has been loaded

		self._param = [[] for i in range(self.n)]
		self._init_param(self.n)

	def clear(self, n=100, max_shingle=3, rand_inf=10000, rand_sup=99999):
		# same as __init__, but for reconstruction
		self.n = n
		self.max_shingle = max_shingle
		self.rand_inf = rand_inf
		self.rand_sup = rand_sup
		assert self.max_shingle > 0, 'error: [clear] max_shingle must be greater than 0'

		self._shingles = {}
		self._counter = 0

		self.shgvec = []
		self.signatures = []
		self.loadflag = 0

		self._param = [[] for i in range(self.n)]
		self._init_param(self.n)

	def _init_param(self, num_hash):
		for i in range(num_hash):
			a = random.randint(self.rand_inf, self.rand_sup)
			self._param[i].append(a)
			b = random.randint(self.rand_inf, self.rand_sup)
			self._param[i].append(b)

	def _get_shingle_vec(self, doc):
		v = {}
		n = self.max_shingle
		for j in range(len(doc) - n + 1):
			s = doc[j:j+n]
			# add new shingles
			if not self._shingles.has_key(s):
				self._shingles[s] = self._counter
				self._counter += 1
			v[self._shingles[s]] = 1
		if (v == {}):
			print 'v == {} : doc to short!!!'
			print doc
		return v

	def _get_query_shingle(self, doc):
		v = {}
		n = self.max_shingle
		for j in range(len(doc) - n + 1):
			s = doc[j:j+n]
			# do not add new shingles
			if self._shingles.has_key(s):
				v[self._shingles[s]] = 1
		if (v == {}):
			print 'v == {}: doc too short, or fully innovative'
			print doc
		return v

	def _get_sig(self, shingle_vec, num_perms):
		mhash = [{} for i in range(num_perms)]
		keys = sorted(shingle_vec.keys())
		for r in keys:
			h = []
			for i in range(num_perms):
				x = (self._param[i][0] * r + self._param[i][1]) % len(self._shingles)
				h.append(x)
			h = np.array(h)
			for i in range(num_perms):
				if (h[i] < mhash[i]):
					mhash[i] = h[i]
		return mhash

	# def _get_sig(self,shingle_vec,num_perms):
	# 	mhash = [{} for i in range(num_perms)]
	# 	keys = sorted(shingle_vec.keys())
	# 	for r in keys:
	# 		#logging.debug('r=%d', r)
	# 		h = np.array([self._xor_hash(mask,r) % len(self._shingles) for mask in self._memomask])
	# 		for i in range(num_perms):
	# 			if (h[i] < mhash[i]):
	# 				mhash[i] = h[i]
	# 	return mhash

	def get_dataset_signature(self):
		assert (self.loadflag == 1), "error: dataset has to be loaded"
		for i in range(len(self.shgvec)):
			shg = self.shgvec[i]
			if (shg == {}):
				sig = [0 for _ in range(self.n)] # zeros for empty
			else:
				sig = self._get_sig(shg, self.n)
			self.signatures.append(sig)

	def get_query_signature(self, doc):
		assert (self.loadflag == 1), "error: query must be after loading"
		shg = self._get_query_shingle(doc)
		if (shg == {}):
			sig = [0 for _ in range(self.n)] # zeros for empty
		else:
			sig = self._get_sig(shg, self.n)
		return sig

	def load_dataset(self, dataset):
		assert (self.loadflag == 0), "error: dataset has to be cleared"
		for doc in dataset:
			shg = self._get_shingle_vec(doc)
			self.shgvec.append(shg)
		self.loadflag = 1


if __name__ =='__main__':

	# parameters
	dim = 32 # dimension of signature vectors to be hashed
	threshold = 16 # the threshold in levenshtein distance
	assert (threshold >= 0), 'error: invalid threshold value'
	print 'threshold: ' + str(threshold)
	lsh_bandwidth = 4 # bandwidth used in lsh
	shingle_size = 3 # shingle size

	t1 = time.time()

	lsh = barelsh(dim, lsh_bandwidth) # param, input dim, band width
	sb = SignatureBuilder(dim, shingle_size) #param: sig dimension, shingle size
	
	print 'traning...'
	cora, cora_answer = load_cora('cora.txt')
	sb.load_dataset(cora) # loading
	sb.get_dataset_signature() # computing
	id_count = 0
	for sig in sb.signatures:
		# fp.write(str(id_count) + ': ' + str(sig) + '\n')
		lsh.index(sig, tuple([id_count, cora_answer[id_count]])) # insert: [param] point, extra_data(optional)
		id_count += 1

	t2 = time.time()

	print 'testing...'
	cora_test, cora_test_answer = load_cora('cora.txt')
	assert (len(cora_test) > 0), 'error: empty dataset'
	test_id_count = 0
	
	result_set = []
	fp = open('lsh-blocked.txt', 'w+')
	dic = set()
	
	for ctestitem in cora_test:
		# computing
		testsig = sb.get_query_signature(ctestitem)
		result = lsh.query(testsig, None, 'levenshtein') # query: [param] query_point, num_results, distance_func
		tmp = [cora_test_answer[test_id_count], []]
		for r in result:
			if (r[1] <= threshold):
				tmp[1].append(r[0][1]) # is a tuple (id, label)
			# tmp[1].append(r[0][1]) # is a tuple (id, label) # if you want no threshold, use this line instead of the two above
		result_set.append(tmp)

		# write blocking result
		aaa = sorted(tmp[1], key=lambda x : x[0])
		straaa = str(aaa)
		if not straaa in dic:
			dic.add(straaa)
			for x in aaa:
				fp.write(str(x[0]) + ' ')
			fp.write('\n')
		
		test_id_count += 1

	fp.close()

	t3 = time.time()
	print 'time1: ' + str(t2-t1) + ' s'
	print 'time2: ' + str(t3-t2) + ' s'

	lsh.destroy()