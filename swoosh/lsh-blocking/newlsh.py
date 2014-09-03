import numpy as np
from storage import storage


class barelsh:

	def __init__(self, input_dim, bwidth, storage_config = None, log=False):
		self.input_dim = input_dim
		self.bwidth = bwidth
		self.log = log

		if storage_config is None:
			storage_config = {'dict': None}
		self.storage_config = storage_config
		
		self._init_hashtables()

		if (log):
			self.fp = open("barelsh_log.txt", "w+")

	def destroy(self):
		if (self.log):
			self.fp.close()
			self.log = False
		self.num_hashtables = 0
		self._hashtables = []
		self._bands = []

	def _init_hashtables(self):
		self._bands = []
		i = 0
		while (i < self.input_dim):
			j = i + self.bwidth - 1
			if (j >= self.input_dim):
				# discard the rest
				break
			self._bands.append((i, j))
			i = j + 1
		self.num_hashtables = len(self._bands)
		self._hashtables = [storage(self.storage_config, i) for i in xrange(self.num_hashtables)]

	def _hash(self, vec, i, j):
		assert (i < len(vec)) and (j < len(vec)), "error: [_hash] index out of range"
		temp = vec[i:j+1]
		return temp

	def index(self, input_point, extra_data=None):
		if (self.log):
			self.fp.write(str(input_point) + '\n')

		if isinstance(input_point, np.ndarray):
			input_point = input_point.tolist()
		if extra_data:
			value = (tuple(input_point), extra_data)
		else:
			value = tuple(input_point)
		for k in range(self.num_hashtables):
			i, j = self._bands[k]
			key = self._hash(input_point, i, j)
			
			if (self.log):
				self.fp.write('bucket: ' + str(k) + ', key: ' + str(key) + ' --- ' + str(extra_data) + '\n')
			
			self._hashtables[k].append_val(str(key), value)

	def _as_np_array(self, json_or_tuple):
		tuples = json_or_tuple

		if isinstance(tuples[0], tuple):
			return np.asarray(tuples[0])
		elif isinstance(tuples, (tuple, list)):
			try:
				return np.asarray(tuples)
			except ValueError as e:
				print("The input needs to be an array-like object", e)
				raise
		else:
			raise TypeError("query data is not supported")

	def query(self, query_point, num_results=None, distance_func=None):
		candidates = set()
		for k in range(self.num_hashtables):
			i, j = self._bands[k]
			key = self._hash(query_point, i, j)
			temp = self._hashtables[k].get_list(str(key))
			candidates.update(temp)

		if not distance_func:
			distance_func = "levenshtein"
		if distance_func == "levenshtein":
			d_func = barelsh.levenshtein_dist
		if distance_func == "hamming":
			d_func = barelsh.hamming_dist

		candidates = [(ix, d_func(query_point, self._as_np_array(ix))) for ix in candidates]
		candidates.sort(key=lambda x: x[1])

		# print 'candidate num: ' + str(len(candidates))
		return candidates[:num_results] if num_results else candidates

	### distance functions

	@staticmethod
	def levenshtein_dist(x, y):
		assert len(x) == len(y), "error: [levenshtein_dist] jaccard operands not compatible"
		count = 0
		for i in range(len(x)):
			if (x[i] != y[i]):
				count += 1
		return count

	@staticmethod
	def hamming_dist(x, y):
		assert len(x) == len(y), "error: [hamming_dist] hamming operands not compatible"
		dist = 0
		for i in range(len(x)):
			dist += abs(x[i] - y[i])
		return dist
