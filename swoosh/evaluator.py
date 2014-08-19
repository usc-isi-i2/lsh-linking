# import numpy as np
# import scipy as sp
# import matplotlib as mpl
# import copy


class evaluator:

	def __init__(self, num):
		self.num = num
		self.anstag = [-1 for _ in xrange(num)]
		self.restag = [-1 for _ in xrange(num)]
		self.precision = 0
		self.recall = 0

	def load_answer_clusters(self, c):
		cnum = len(c)
		for curtag in xrange(cnum):
			curc = c[curtag]
			for item in curc:
				self.anstag[item] = curtag

	def load_answer_labeled(self, lb):
		self.anstag = lb

	def _evaluate(self):
		tp = 0 # true positive
		fp = 0 # false positive
		fn = 0 # false negative
		for i in xrange(self.num):
			for j in xrange(i+1, self.num):
				if  (self.anstag[i] == self.anstag[j]):
					if (self.restag[i] == self.restag[j]):
						tp += 1
					else:
						fn += 1
				elif (self.restag[i] == self.restag[j]):
					fp += 1
		self.precision = (tp + .0) / (tp + fp)
		self.recall = (tp + .0) / (tp + fn)
		print 'precision: ' + str(self.precision)
		print 'recall: ' + str(self.recall)

	def evaluate_clusters(self, c):
		cnum = len(c)
		for curtag in xrange(cnum):
			curc = c[curtag]
			for item in curc:
				self.restag[item] = curtag
		self._evaluate()

	def evaluate_labeled(self, lb):
		self.restag = lb
		self._evaluate()

	def get_fmeasure(self, beta):
		fm = (beta * beta + 1) * self.precision * self.recall / (beta * beta * self.precision) + self.recall
		print 'f-' + str(beta) + ' measure: ' + str(fm)
