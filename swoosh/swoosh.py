from storage import storage
import Levenshtein as lvst

# f-swoosh algorithm
class fswoosh:

	def __init__(self, dim, setI0, fList, matchFuncList=None, mergeFuncList=None, storage_config=None):
		self.dim = dim
		self.setI0 = setI0
		self.fList = fList # format of fList: a list of items [features indices list]

		if storage_config is None:
			storage_config = {'dict': None}
		self.storage_config = storage_config
		if matchFuncList is None:
			matchFuncList = [fswoosh.levDist for _ in xrange(len(fList))]
		self._matchFuncList = matchFuncList
		if mergeFuncList is None:
			mergeFuncList = [fswoosh.pickLonger for _ in xrange(dim)]
		self._mergeFuncList = mergeFuncList

		self.Pf = [storage(self.storage_config, i) for i in xrange(len(fList))]
		self.Nf = [[] for i in xrange(len(fList))]
		self.setI = []
		self.curRec = None

	def reconstruct(self, dim, setI0, fList, matchFuncList=None, mergeFuncList=None, storage_config=None):
		self.dim = dim
		self.setI0 = setI0
		self.fList = fList # format of fList: a list of items [features indices list]
		fp = open('logs/merge_log.txt', 'w+') # clear merge log
		fp.close()
		
		if storage_config is None:
			storage_config = {'dict': None}
		self.storage_config = storage_config
		if matchFuncList is None:
			matchFuncList = [fswoosh.levDist for _ in xrange(len(fList))]
		self._matchFuncList = matchFuncList
		if mergeFuncList is None:
			mergeFuncList = [fswoosh.pickLonger for _ in xrange(dim)]
		self._mergeFuncList = mergeFuncList

		self.Pf = [storage(self.storage_config, i) for i in xrange(len(fList))]
		self.Nf = [[] for i in xrange(len(fList))]
		self.setI = []
		self.curRec = None

	def compute(self):
		while (len(self.setI0) > 0) or (self.curRec != None):
			if (self.curRec == None):
				self.curRec = self.setI0.pop()
			buddy = None
			feats = self._extractFeatures(self.curRec)
			# feats format: a list of items [dimensions of featvalue]
			for f in xrange(len(feats)): # keep track of new values
				v = feats[f]
				if (not str(v) in self.Pf[f].keys()) or (self.Pf[f].get_val(str(v)) == None):
					self.Pf[f].set_val(str(v), self.curRec)
			for f in xrange(len(feats)): # any pre-occured
				v = feats[f]
				tmp = self.Pf[f].get_val(str(v))
				if (tmp != self.curRec):
					buddy = tmp
					break
			if (buddy == None): # no pre-occured exist
				for f in xrange(len(feats)):
					v = feats[f]
					if not v in self.Nf[f]:
						for tmpr in self.setI:
							tmpfeats = self._extractFeatures(tmpr)
							# tmpfeats format: a list of tuples (featname, [dimensions of featvalue])
							vv = tmpfeats[f]
							# print 'v: ' + str(v)
							# print 'vv: ' + str(vv)
							if self._matchFunc(f, v, vv):
								buddy = tmpr
								break
						if (buddy != None):
							break
						if v not in self.Nf[f]: # add to set
							self.Nf[f].append(v)
			if (buddy == None):
				if self.curRec not in self.setI: # add to set
					self.setI.append(self.curRec)
				self.curRec = None
			else:
				rr = self._mergeFunc(self.curRec, buddy)
				if buddy in self.setI:
					self.setI.remove(buddy)
				else:
					print 'buddy not in self.setI'
				for f in xrange(len(self.fList)):
					# traverse all keys (feature values) in f's hashtable
					for v in self.Pf[f].keys():
						x = self.Pf[f].get_val(v)
						if (x == self.curRec) or (x == buddy):
							self.Pf[f].set_val(v, rr)
				self.curRec = rr
		return self.setI

	def _extractFeatures(self, rec):
		res = []
		for feat in self.fList:
			# format of feat: [features indices list]
			v = []
			for dim in feat:
				v.append(rec[dim])
			res.append(v)
		return res

	def _matchFunc(self, feat, v1, v2):
		return self._matchFuncList[feat](v1, v2)

	def _mergeFunc(self, r1, r2):
		lv1 = len(r1)
		lv2 = len(r2)
		assert (lv1 == lv2), 'error: [_mergeFunc] not compatible'
		res = []
		for i in xrange(lv1):
			# merge corresponding dimensions with special merge function
			res.append(self._mergeFuncList[i](r1[i], r2[i]))
		fp = open('logs/merge_log.txt', 'a')
		fp.write(str(r1[0]) + '-' + str(r2[0]) + '\n')
		fp.close()
		return res

	@staticmethod
	def levDist(vv1, vv2):
		LEVTHR = 3
		v1 = vv1.strip(',.\'" \t\n')
		v2 = vv2.strip(',.\'" \t\n')
		lv1 = len(v1)
		lv2 = len(v2)
		assert (lv1 == lv2), 'error: [levDist] not compatible'
		emptyflag = True
		for i in xrange(lv1):
			l1 = len(v1[i])
			l2 = len(v2[i])
			thr = max(l1, l2) / LEVTHR
			if (l1 != 0) and (l2 != 0): # both non-empty
				emptyflag = False
				dis = lvst.distance(v1[i].lower(), v2[i].lower())
				if (dis > thr):
					return False
		if emptyflag: # all empty
			return False
		return True

	@staticmethod
	def pickLonger(v1, v2):
		if (len(v1) > len(v2)):
			return v1
		else:
			return v2
