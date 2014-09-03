from storage import storage
import Levenshtein as lvst

# f-swoosh algorithm
# (only do the scoring)
class swscore:

	# storage_config can be '{"redis": {"host": hostname, "port": port_num}}''
	def __init__(self, fList1, fList2, scoreFunc=None, matchFuncList=None, storage_config=None):
		self.fList1 = fList1
		self.fList2 = fList2
		assert (len(fList1) == len(fList2)), 'error: [__init__] not compatible'
		if storage_config is None:
			storage_config = {'dict': None}
		self.storage_config = storage_config
		if matchFuncList is None:
			self._matchFuncList = [swscore.levDist for _ in xrange(len(fList1))]
		else:
			assert (len(matchFuncList) == len(fList1)), 'error: [__init__] not compatible'
			self._matchFuncList = []
			for func in matchFuncList:
				if func is None:
					self._matchFuncList.append(swscore.levDist)
				elif (func == 'levenshtein'):
					self._matchFuncList.append(swscore.levDist)
				else:
					self._matchFuncList.append(func)
		if scoreFunc is None:
			self.scoreFunc = self.defaultScore
		else:
			self.scoreFunc = scoreFunc
		self._hashTable = [storage(self.storage_config, i) for i in xrange(len(fList1))]

	# same as __init__: reconstruction
	def clear(self, fList1, fList2, scoreFunc=None, matchFuncList=None, storage_config=None):
		self.fList1 = fList1
		self.fList2 = fList2
		assert (len(fList1) == len(fList2)), 'error: [__init__] not compatible'
		if storage_config is None:
			storage_config = {'dict': None}
		self.storage_config = storage_config
		if matchFuncList is None:
			self._matchFuncList = [swscore.levDist for _ in xrange(len(fList1))]
		else:
			assert (len(matchFuncList) == len(fList1)), 'error: [__init__] not compatible'
			self._matchFuncList = []
			for func in matchFuncList:
				if func is None:
					self._matchFuncList.append(swscore.levDist)
				elif (func == 'levenshtein'):
					self._matchFuncList.append(swscore.levDist)
				else:
					self._matchFuncList.append(func)
		if scoreFunc is None:
			self.scoreFunc = self.defaultScore
		else:
			self.scoreFunc = scoreFunc
		self._hashTable = [storage(self.storage_config, i) for i in xrange(len(fList1))]

	def _extractFeatures(self, rec, flist):
		res = []
		for feat in flist:
			v = []
			for dim in feat:
				v.append(rec[dim])
			res.append(v)
		return res

	def _matchFunc(self, feat, v1, v2):
		# look up in hashtable
		key = (v1, v2)
		if str(key) in self._hashTable[feat].keys():
			return self._hashTable[feat].get_val(str(key))
		else:
			result = self._matchFuncList[feat](v1, v2)
			self._hashTable[feat].set_val(str(key), result)
		return result

	# @staticmethod
	# default score function: average score
	def defaultScore(self, r1, r2):
		score = 0.
		f1 = self._extractFeatures(r1, self.fList1)
		f2 = self._extractFeatures(r2, self.fList2)
		for feat in xrange(len(self.fList1)):
			score += self._matchFunc(feat, f1[feat], f2[feat])
		return score / len(self.fList1)

	# default score function: levenshtein distance
	@staticmethod
	def levSim(vv1, vv2):
		v1 = vv1.strip(' ,.\'" \t\n')
		v2 = vv2.strip(' ,.\'" \t\n')
		lv1 = len(v1)
		lv2 = len(v2)
		dis = 0
		assert (lv1 == lv2), 'error: [levSim] not compatible'
		for i in xrange(lv1):
			l1 = len(v1[i])
			l2 = len(v2[i])
			if (l1 != 0) and (l2 != 0):
				dis += lvst.distance(v1[i].lower(), v2[i].lower())
			else:
				return 0
		if (dis == 0):
			return 1
		return lv1 / dis