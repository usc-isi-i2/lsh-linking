from swoosh import fswoosh
import Levenshtein as lvst
import json
import re
import time
from evaluate import evaluate


def pickLonger(v1, v2):
	if (len(v1) > len(v2)):
		return v1
	else:
		return v2


def levDist(v1, v2):
	LEVTHR = 3
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
		else: # numbers of numeric values not match
			return False
	if emptyflag: # all empty
		return False
	return True


def matchFirstname(v1, v2):
	tv1 = v1.lower()
	tv2 = v2.lower()
	if (tv1 == tv2):
		return True
	if (tv1[0] == tv2) or (tv2[0] == tv1):	
		return True
	return False

def matchSingleName(v1, v2):
	m1 = v1.replace('.', ' '). replace(',', ' ').split()
	m2 = v2.replace('.', ' '). replace(',', ' ').split()
	if (len(m1) > len(m2)):
		lungo = m1
		corto = m2
	else:
		lungo = m2
		corto = m1
	ln1 = lungo[len(lungo)-1].lower()
	ln2 = corto[len(corto)-1].lower()
	ln11 = lungo[0].lower()
	ln22 = corto[0].lower()
	if (ln1 != ln2): # lastname must match
		if (ln1 == ln22) and (len(ln1) > 2):
			lungo.pop()
			corto.remove(corto[0])
		elif (ln2 == ln11) and (len(ln2) > 2):
			corto.pop()
			lungo.remove(lungo[0])
		else:
			return False
	else:
		lungo.pop()
		corto.pop()
	flag = True
	i = j = 0
	while (i < len(lungo)) and (j < len(corto)):
		if (matchFirstname(lungo[i], corto[j])):
			i += 1
			j += 1
		else:
			i += 1
		if (j == len(corto)): # corto used up
			flag = True
			break
		elif (i == len(lungo)): # lungo used up before corto
			flag = False
			break
	return flag

def matchNameList(v1, v2):
	lv1 = len(v1)
	lv2 = len(v2)
	if (lv1 != lv2):
		return False
	res = True
	for i in xrange(lv1):
		res &= matchSingleName(v1[i], v2[i])
	return res

def mergeNameList(v1, v2):
	lv1 = len(v1)
	lv2 = len(v2)
	if (lv1 > lv2):
		lungo = v1
		corto = v2
	else:
		lungo = v2
		corto = v1
	res = []
	for i in xrange(len(corto)):
		res.append(pickLonger(v1[i], v2[i]))
	for j in xrange(i+1, len(lungo)):
		res.append(lungo[j])
	return res


def matchTitleYear(v1, v2):
	assert (len(v1) == 2) and (len(v2) == 2), 'error: [matchTitleYear] not compatible'
	return levDist([v1[0]], [v2[0]]) & matchNumeric([v1[1]], [v2[1]])

def matchTitleAuthor(v1, v2):
	assert (len(v1) == 2) and (len(v2) == 2), 'error: [matchTitleAuthor] not compatible'
	return levDist([v1[0]], [v2[0]]) & matchNameList(v1[1], v2[1])


def jaccardDist_Tokenized(v1, v2):
	JACTHR = 0.5
	res = True
	lv1 = len(v1)
	lv2 = len(v2)
	assert (lv1 == lv2), 'error: [jaccardDist_Tokenized] not compatible'

	for i in xrange(lv1):
		s1 = set()
		s2 = set()
		t1 = v1[i].split(' \t')
		t2 = v2[i].split(' \t')
		for t in t1:
			t = t.strip(',.\'"')
			s1.add(t)
		for t in t2:
			t = t.strip(',.\'"')
			s2.add(t)
		i12 = s1 & s2
		u12 = s1 | s2
		jac = (len(i12) + .0) / len(u12)
		res &= (jac > JACTHR)
	return result

def pickByContribution(v1, v2):
	s1 = set()
	s2 = set()

	t1 = v1.split(' \t')
	t2 = v2.split(' \t')
	for t in t1:
		t = t.strip(',.\'"')
		s1.add(t)
	for t in t2:
		t = t.strip(',.\'"')
		s2.add(t)
	s = s1 | s2
	m1 = (len(s1) + .0) / len(s)
	m2 = (len(s2) + .0) / len(s)
	if (m1 > m2):
		return v1
	else:
		return v2


def indexMatch(v1, v2):
	return False

def indexMerge(v1, v2):
	return v2


if __name__ == '__main__':

	matchSingleName('f. totti', 'francesco totti')

	fp = open('cora-namelist.json')
	coraObj = json.load(fp)
	fp.close()

	flist = [[0], [2, 1], [2, 3], [2, 4]]
	matchFuncList = [indexMatch, matchTitleAuthor, levDist, matchTitleYear]
	mergeFuncList = [indexMerge, mergeNameList, pickLonger, pickLonger, pickLonger]
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
		# item.append(tmp['pages'])
		# item.append(tmp['editor'])
		# item.append(tmp['note'])
		# item.append(tmp['month'])
		rlist.append(item)

	dim = len(rlist[0])
	fsw = fswoosh(dim, rlist, flist, matchFuncList, mergeFuncList)
	result = fsw.compute()

	eva = evaluate(len(result), 1295, 'clusters.txt', 'cora-clusters.txt')
	eva.do()
