from swoosh import fswoosh
import Levenshtein as lvst
import json
import re
import time


curtime = 0


class levDist:

	def __init__(self, threshold=0, dim=1):
		self.threshold = threshold
		self.dim = dim

	def compute(self):
		lv1 = len(v1)
		lv2 = len(v2)
		assert (lv1 == lv2), 'error: [levDist] not compatible'
		res = 0
		for i in xrange(lv1):
			res += lvst.distance(v1[i], v2[i])
		if (res <= self.threshold):
			return True
		else:
			return False
		return res


def levDist(v1, v2):
	lv1 = len(v1)
	lv2 = len(v2)
	thr = min(lv1, lv2) / 3
	assert (lv1 == lv2), 'error: [levDist] not compatible'
	res = 0
	for i in xrange(lv1):
		res += lvst.distance(v1[i], v2[i])
	if (res <= thr):
		return True
	else:
		return False
	return res


def pickLonger(v1, v2):
	if (len(v1) > len(v2)):
		return v1
	else:
		return v2


def indexMerge(v1, v2):
	# fp = open('logs/merge_log' + str(curtime) + '.txt', 'a')
	# fp.write(v1 + '-' + v2 + '\n')
	# fp.close()
	return v2


def matchNumeric(v1, v2):
	lv1 = len(v1)
	lv2 = len(v2)
	assert (lv1 == lv2), 'error: [matchNumeric] not compatible'
	pattern = re.compile('\d{1,4}')
	emptyflag = True
	for i in xrange(lv1):
		nl1 = pattern.findall(v1[i])
		nl2 = pattern.findall(v2[i])
		if (len(nl1) == len(nl2)):
			if (len(nl1) == 0): # both empty
				continue
			else: # both non-empty
				emptyflag = False
				for j in xrange(len(nl1)):
					if (nl1[j] != nl2[j]): # must all match
						return False
	if emptyflag: # all empty
		return False
	return True


def indexMatch(v1, v2):
	return False


if __name__ == '__main__':

	# flist = [[0], [1, 2]]
	# r1 = ['JohnDoe', '235-2635', 'jdoe@yahoo']
	# r2 = ['J.Doe', '234-4358', '']
	# r3 = ['JohnD.', '234-4358', 'jdoe@yahoo']
	# rlist = [r1, r2, r3]
	# dim = len(rlist)

	curtime = time.time()

	fp = open('cora.json')
	coraObj = json.load(fp)
	fp.close()
	flist = [[0], [1], [2, 3], [4, 5]]
	matchFuncList = [indexMatch, levDist, levDist, matchNumeric]
	mergeFuncList = [indexMerge, pickLonger, pickLonger, pickLonger, pickLonger, pickLonger]
	rlist = []
	laut = 0
	ltit = 0
	lven = 0
	lyea = 0
	lpag = 0
	for i in xrange(len(coraObj)):
		tmp = coraObj[str(i)]
		item = []
		item.append(str(i))
		item.append(tmp['author'])
		# item.append(tmp['volume'])
		item.append(tmp['title'])
		# item.append(tmp['institution'])
		item.append(tmp['venue'])
		# item.append(tmp['address'])
		# item.append(tmp['publisher'])
		item.append(tmp['year'])
		item.append(tmp['pages'])
		# item.append(tmp['editor'])
		# item.append(tmp['note'])
		# item.append(tmp['month'])
		rlist.append(item)

		laut += len(tmp['author'])
		ltit += len(tmp['title'])
		lven += len(tmp['venue'])
		lyea += len(tmp['year'])
		lpag += len(tmp['pages'])

	laut = (laut + .0) / 1295.
	ltit = (ltit + .0) / 1295.
	lven = (lven + .0) / 1295.
	lyea = (lyea + .0) / 1295.
	lpag = (lpag + .0) / 1295.

	print laut
	print ltit
	print lven
	print lyea
	print lpag

	dim = len(rlist[0])
	fsw = fswoosh(dim, rlist, flist, matchFuncList, mergeFuncList)
	result = fsw.compute()
	# encoded = json.dumps(result)
	# print result
	print len(result)
