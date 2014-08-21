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

def matchTitlePublisher(v1, v2):
	assert (len(v1) == 2) and (len(v2) == 2), 'error: [matchTitlePublisher] not compatible'
	return levDist([v1[0]], [v2[0]]) & levDist([v1[1]], [v2[1]])

def matchTitlePages(v1, v2):
	assert (len(v1) == 2) and (len(v2) == 2), 'error: [matchTitlePages] not compatible'
	return levDist([v1[0]], [v2[0]]) & matchNumeric([v1[1]], [v2[1]])

def matchAuthorVenueYearMonth(v1, v2):
	assert (len(v1) == 4) and (len(v2) == 4), 'error: [matchTitlePages] not compatible'
	res = matchNameList(v1[0], v2[0]) & levDist([v1[1]], [v2[1]]) & matchNumeric([v1[2]], [v2[2]])
	if (v1[3] != '') and (v2[3] != ''):
		res &= matchNumeric([v1[3]], [v2[3]])
	return res

def matchTitlePublisherYearMonth(v1, v2):
	assert (len(v1) == 4) and (len(v2) == 4), 'error: [matchTitlePublisherYearMonth] not compatible'
	res = levDist([v1[0]], [v2[0]]) & levDist([v1[1]], [v2[1]]) & matchNumeric([v1[2]], [v2[2]])
	if (v1[3] != '') and (v2[3] != ''): # month is optional, can be empty
		res &= matchNumeric([v1[3]], [v2[3]])
	return res

def matchPublisherYearMonthPages(v1, v2):
	assert (len(v1) == 4) and (len(v2) == 4), 'error: [matchPublisherYearMonthPages] not compatible'
	res = levDist([v1[0]], [v2[0]]) & matchNumeric([v1[1]], [v2[1]]) & matchNumeric([v1[3]], [v2[3]]) & matchNumeric([v1[2]], [v2[2]])
	return res


def jaccardDist_Shingled(vv1, vv2):
	JACTHR = 0.5
	SIZE = 3
	res = True
	v1 = vv1.strip(',.\'" \t\n')
	v2 = vv2.strip(',.\'" \t\n')
	lv1 = len(v1)
	lv2 = len(v2)
	assert (lv1 == lv2), 'error: [jaccardDist_Shingled] not compatible'
	
	s1 = set()
	s2 = set()
	for i in xrange(lv1):
		if (len(v1[i]) <= SIZE) or (len(v2[i]) <= SIZE):
			if (v1[i] != v2[i]):
				return False
			else:
				continue
		for j in xrange(len(v1[i])-SIZE+1):
			tmp1 = v1[i][j:j+SIZE]
			s1.add(tmp1)
		for j in xrange(len(v2[i])-SIZE+1):
			tmp2 = v2[i][j:j+SIZE]
			s2.add(tmp2)
		i12 = s1 & s2
		u12 = s1 | s2
		jac = (len(i12) + .0) / len(u12)
		res &= (jac > JACTHR)
		s1.clear()
		s2.clear()
	return res

def pickByContribution(v1, v2):
	s1 = set()
	s2 = set()
	SIZE = 3

	vv1 = v1.strip(',.\'" \t\n')
	vv2 = v2.strip(',.\'" \t\n')
	if (len(vv1) <= SIZE) or (len(vv2) <= SIZE):
		return pickLonger(vv1, vv2)

	for j in xrange(len(vv1)-SIZE+1):
		tmp1 = vv1[j:j+SIZE]
		s1.add(tmp1)
	for j in xrange(len(vv2)-SIZE+1):
		tmp2 = vv2[j:j+SIZE]
		s1.add(tmp2)
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

	# print matchSingleName('f. totti', 'francesco totti')
	fp = open('cora-namelist.json')
	coraObj = json.load(fp)
	fp.close()

	# design feature combinations
	# flist = [[0], [3, 1], [3, 5], [3, 7, 8, 12], [7, 8, 12, 9]]
	# flist = [[0], [3, 1], [3, 5], [3, 7, 8, 12]]
	# flist = [[0], [3, 1], [3, 5], [3, 7], [3, 8]]
	flist = [[0], [3, 1], [3, 5], [3, 7], [3, 8], [3, 9]]
	# flist = [[0], [3, 1], [3, 5], [3, 7], [3, 8], [3, 9], [1, 5, 8, 12]]
	# flist = [[0], [3, 1], [3, 5], [3, 7], [3, 8], [7, 8, 12, 9]]

	# design appropriate match funcs
	# matchFuncList = [indexMatch, matchTitleAuthor, levDist, matchTitlePublisherYearMonth, matchPublisherYearMonthPages]
	# matchFuncList = [indexMatch, matchTitleAuthor, levDist, matchTitlePublisherYearMonth]
	# matchFuncList = [indexMatch, matchTitleAuthor, levDist, matchTitlePublisher, matchTitleYear]
	matchFuncList = [indexMatch, matchTitleAuthor, levDist, matchTitlePublisher, matchTitleYear, matchTitlePages]
	# matchFuncList = [indexMatch, matchTitleAuthor, levDist, matchTitlePublisher, matchTitleYear, matchTitlePages, matchAuthorVenueYearMonth]
	# matchFuncList = [indexMatch, matchTitleAuthor, levDist, matchTitlePublisher, matchTitleYear, matchPublisherYearMonthPages]
	
	# design appropriate merge funcs
	mergeFuncList = [indexMerge, mergeNameList, pickLonger, pickLonger, pickLonger, pickLonger, pickLonger, pickLonger, pickLonger, pickLonger, pickLonger, pickLonger, pickLonger]
	
	fp = open('logs/merge_log.txt', 'w+')
	fp.close()

	rlist = []
	s = [0 for _ in xrange(13)]
	for i in xrange(len(coraObj)):
		tmp = coraObj[str(i)]
		item = []
		item.append(str(i)) #0
		item.append(tmp['author'])  #1
		item.append(tmp['volume']) #2
		item.append(tmp['title']) #3
		item.append(tmp['institution']) #4
		item.append(tmp['venue']) #5
		item.append(tmp['address']) #6
		item.append(tmp['publisher']) #7
		item.append(tmp['year']) #8
		item.append(tmp['pages']) #9
		item.append(tmp['editor']) #10
		item.append(tmp['note']) #11
		item.append(tmp['month']) #12
		rlist.append(item)

		for j in xrange(1, 13):
			if (item[j] != ''):
				s[j] += 1

	print 'id, auth, vol, ttl, ins, ven, addr, pub, year, pag, edi, nt, mon'
	print s

	dim = len(rlist[0])
	# f-swoosh: record dimension, record list, feature list, match func list, merge func list
	fsw = fswoosh(dim, rlist, flist, matchFuncList, mergeFuncList)
	result = fsw.compute()

	# evaluation: num after merging, num of records, result file, correct answer file
	eva = evaluate(len(result), len(coraObj), 'clusters.txt', 'cora-clusters.txt')
	eva.do()
