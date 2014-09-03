from swscore import swscore
from storage import storage
import Levenshtein as lvst
import json
import re
import time
import load
try:
	import jaro
except:
	print 'python package "jaro" required'

########################################
# matching functions and merging functions

# pick the longer one
def pickLonger(v1, v2):
	if (len(v1) > len(v2)):
		return v1
	else:
		return v2

# use levenshtein dist to judge: match or not
def levDist(vv1, vv2):
	LEVTHR = 3 # threshold
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

# judge a list of numeric values: match or not
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

# match a single first name string
def matchFirstname(v1, v2):
	tv1 = v1.lower()
	tv2 = v2.lower()
	if (tv1 == tv2):
		return True
	if (tv1[0] == tv2) or (tv2[0] == tv1):	
		return True
	return False

# match single name
def matchSingleName(v1, v2):
	try:
		m1 = v1.decode('utf-8').strip().replace('.', ' '). replace(',', ' ').split()
		m2 = v2.decode('utf-8').strip().replace('.', ' '). replace(',', ' ').split()
	except:
		return False
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

# use matchSingleName to match a list of names:
# used in cora dataset to match author list
def matchNameList(v1, v2):
	lv1 = len(v1)
	lv2 = len(v2)
	if (lv1 != lv2):
		return False
	res = True
	for i in xrange(lv1):
		res &= matchSingleName(v1[i], v2[i])
	return res

# merge two name list into one
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

# calculate jaccard dist of two strings by shingle them first
def jaccardDist_Shingled(vv1, vv2):
	JACTHR = 0.5 # threshold
	SIZE = 3 # shingle size
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

# 
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

# new functions 08.25

# jaro-winkler similarity
def jwSim(v1, v2):
	try:
		return jaro.jaro_winkler_metric(v1.decode('utf-8').strip().lower(), v2.decode('utf-8').strip().lower())
	except:
		# print v1
		# print v2
		return 0.

# match year in dates: primary version
# used in date matching from museum to dbpedia
def matchYearInDate(v1, v2):
	lv1 = len(v1)
	lv2 = len(v2)
	assert (lv1 == lv2), 'error: [matchNumeric] not compatible'
	pattern = re.compile('\d{4}')
	res = True
	emptyflag = True
	looseflag = 0
	for i in xrange(lv1):
		nl1 = pattern.findall(v1[i])
		nl2 = pattern.findall(v2[i])
		if ((len(nl1) == 0) or (len(nl2) == 0)): # assure non-empty
			continue
		emptyflag = False
		for x in nl1:
			for y in nl2:
				xx = int(x)
				yy = int(y)
				if (xx != yy):
					# if (abs(xx - yy) <= 1):
					# 	if (looseflag != 0):
					# 		return False
					# 	else:
					# 		looseflag = 1
					return False # NOTICE: to add toleration in years, free codes above and annotate this line
	if emptyflag:
		return False
	if (looseflag == 1):
		return 'pending'
	return res

# # matchYearInDate: jaro-winkler version
# def matchYearInDate(v1, v2):
# 	# jaro version
# 	lv1 = len(v1)
# 	lv2 = len(v2)
# 	assert (lv1 == lv2), 'error: [matchNumeric] not compatible'
# 	pattern = re.compile('\d{4}')
# 	res = True
# 	emptyflag = True
#	looseflag = 0
# 	for i in xrange(lv1):
# 		nl1 = pattern.findall(v1[i])
# 		nl2 = pattern.findall(v2[i])
# 		if ((len(nl1) == 0) or (len(nl2) == 0)): # assure non-empty
# 			continue
# 		emptyflag = False
# 		for x in nl1:
# 			for y in nl2:
#				tmp = jwSim(x, y)
#				if (tmp > 0.9):
#					if (tmp != 1.0):
#						if (looseflag != 0):
#							return False
#						else:
#							looseflag = 1
#				else:
#					return False
# 	if emptyflag:
# 		return False
# 	return res

# match a pair of places
# e.g: matchPlaces('Los Angeles, CA', 'los angeles, california, usa') == True
def matchPlaces(v1, v2):
	try:
		m1 = v1.decode('utf-8').strip(' \t\n,."\'').replace('.', ' '). replace(',', ' ').split()
		m2 = v2.decode('utf-8').strip(' \t\n,."\'').replace('.', ' '). replace(',', ' ').split()
	except:
		return False
	if (len(m1) > len(m2)):
		lungo = m1
		corto = m2
	else:
		lungo = m2
		corto = m1
	
	# extract lastname (place name)
	ln1 = lungo[len(lungo)-1].lower()
	ln2 = corto[len(corto)-1].lower()
	ln11 = lungo[0].lower()
	ln22 = corto[0].lower()
	if (ln1 != ln2):
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
	count = 0
	PLACETHR = min(len(corto), (len(lungo)+1)/2) - 1 # threshold

	while (i < len(lungo)) and (j < len(corto)):
		if (matchFirstname(lungo[i], corto[j])):
			i += 1
			j += 1
			count += 1
		else:
			i += 1
		if (j == len(corto)): # corto used up
			flag = True
			break
		elif (i == len(lungo)): # lungo used up before corto
			flag = False
			break
	if (flag and (count >= PLACETHR)):
		return True
	return False

# match place list
def matchPlacesList(v1, v2):
	lv1 = len(v1)
	lv2 = len(v2)
	if (lv1 != lv2):
		return False
	res = True
	emptyflag = True
	for i in xrange(lv1):
		if ((v1[i] == '') or (v2[i] == '')):
			continue
		emptyflag = False
		res &= matchPlaces(v1[i], v2[i])
	if emptyflag:
		return False
	return res

########################################
# tool functions for linkage from museum to dbpedia

# load dbpedia blocking result
# SPECIAL NOTICE: the blocking result STARTS AT 1, please shift if
# sconfig: (optinal) can be '{"redis": {"host": hostname, "port": port_num}}'
def load_buckets(sconfig=None):
	# fp = open('dbpedia-blocked-old.txt')
	# fp = open('dbpedia-blocked-shortkey.txt')
	fp = open('dbpedia-blocked-longkey.txt')
	key_list = [line.strip().split(', ') for line in fp]
	if sconfig is None:
		sconfig = {'dict': None}
	hashtable = storage(sconfig, 0)
	for i in xrange(1, len(key_list)): # STARTS AT 1
		kl = key_list[i]
		k = kl[0]
		l = kl[1].split()
		for x in l:
			hashtable.append_val(k, int(x)-1) # bug fix
	fp.close()
	return hashtable

# load museum blocking result
# for item i in museum, bn[i] is a list contain all bucket key for i
# SPECIAL NOTICE: the blocking result STARTS AT 1, please shift if
def load_bucNum(size):
	# fp = open('museum-blocked-shortkey.txt')
	fp = open('museum-blocked-longkey.txt')
	key_list = [line.strip().split(', ') for line in fp]
	bn = [[] for _ in xrange(size)]
	for i in xrange(1, len(key_list)): # STARTS AT 1
		kl = key_list[i]
		k = kl[0]
		l = kl[1].split()
		for v in l:
			bn[int(v)-1].append(k) # bug fix
	fp.close()
	return bn

# add prerequisite (not in use)
def basicRequirement(r1, r2):
	return True

# # version with out place information
# def matchNameBirthDeathDate(v1, v2):
# 	assert ((len(v1) == 3) and (len(v2) == 3)), 'error: [matchNameBirthDeath] not compatible'
# 	s1 = jwSim(v1[0], v2[0])
# 	s2 = matchYearInDate([v1[1], v1[2]], [v2[1], v2[2]])
# 	JWTHR = 0.9
# 	res = 0
# 	if (s1 > JWTHR):
# 		if s2:
# 			res = s1
# 		else:
# 			res = s1 / 2.0
# 	return res

def matchNameBirthDeathDatePlace(v1, v2):
	assert ((len(v1) == 5) and (len(v2) == 5)), 'error: [matchNameBirthDeath] not compatible'
	s1 = jwSim(v1[0], v2[0])
	s2 = matchYearInDate([v1[1], v1[2]], [v2[1], v2[2]])
	s3 = matchPlacesList([v1[3], v1[4]], [v2[3], v2[4]])
	JWTHR = 0.9 # threshold
	res = 0
	if (s1 > JWTHR):
		if (s2 == 'pending'):
			if s3:
				res = s1
		elif (s2 == True):
			res = s1
		else:
			res = s1 / 2.0
	return res

# linkage from museum to dbpedia
# return the target id in dbpedia
def bucket_linkage(rec, buckets, buclist, srcset, targetset):
	assert (len(buclist) > 0), 'error: [bucket_linkage] no bucket'
	# combime all buckets where rec found (buclist)
	pool = []
	for x in buclist:
		try:
			tmp = buckets.get_val(x)
			pool += tmp
		except:
			# print 'key not found: ' + x
			pass
	if (len(pool) == 0):
		return None

	# feature lists
	flist1 = [[1, 2, 4, 3, 5]] # museum
	flist2 = [[3, 1, 2, 4, 5]] # dbpedia

	# matchFuncList = [matchNameBirthDeathDate]
	matchFuncList = [matchNameBirthDeathDatePlace]
	
	scoreFunc = None
	maxscore = -1
	target = None
	fsw = swscore(flist1, flist2, scoreFunc, matchFuncList)
	for candidate in pool:
		if (basicRequirement(12, 34)): # not in use yet
			tmp = fsw.scoreFunc(srcset[rec], targetset[candidate])
			if (tmp > maxscore):
				maxscore = tmp
				target = candidate
	# NOTICE: target can be None
	if (maxscore < 0.55): # no good score, abandon the top result
		return None
	return target



if __name__ == '__main__':
	t0 = time.time()

	mus_data = load.load_museum('museum.csv') # 10000
	dbp_data = load.load_dbpedia('dbpedia-place-649050.csv') # 649050

	t1 = time.time()

	# # clear files
	# first = '123456789abcdef'
	# last = '1234567890abcdef'
	# for i in xrange(len(first)):
	# 	for j in xrange(len(last)):
	# 		fn = first[i] + last[j]
	# 		try:
	# 			fp = open('buckets/' + fn + '.txt', 'w+')
	# 			fp.close()
	# 		except:
	# 			print 'file not exist: ' + fn

	# load from dbpedia blocking results
	# buckets = load_buckets({'redis':{'host':'localhost', 'port':6379}})
	buckets = load_buckets()

	# # write into files
	# for k in buckets.keys():
	# 	fn = k[0:2]
	# 	fp = open('buckets/' + fn + '.txt', 'a')
	# 	l = buckets.get_val(k)
	# 	for x in l:
	# 		fp.write(k + '-' + str(x) + '\n')
	# 	fp.close()

	# load museum blocking results
	bucNum = load_bucNum(len(mus_data))

	t2 = time.time()

	fp1 = open('linking-result.txt', 'w+')
	fp2 = open('log.txt', 'w+')
	sss = [0, 0] # for statistics
	gt = load.load_groundtruth_a('gt.csv')
	resdict = []
	
	for i in xrange(len(mus_data)):
		# if (mus_data[i][1].strip().lower()[0] != 'a'): # only 'a' starting ones
		# 	continue
		res = bucket_linkage(i, buckets, bucNum[i], mus_data, dbp_data)
		fp1.write(str(i) + '--' + str(res) + '\n')
		fp2.write(str(mus_data[i]) + '\n')
		if not (res is None):
			fp2.write(str(dbp_data[res]) + '\n')
		fp2.write('------------------------------------------------\n')
		sss[0] += 1
		sss[1] += 1
		if (sss[0] == 100):
			sss[0] = 0
			print sss[1]
		# pattern = re.compile('\d+')
		# try:
		# 	pid = pattern.findall(mus_data[i][0].strip())[0]
		# except:
		# 	# print str(i) + '---' + mus_data[i][0] # eliminate cartermuseum
		# 	continue
		# url = None
		# if not res is None:
		# 	url = dbp_data[res][0].strip()
		# resdict.append((pid, url))
	print sss[1] # total item number

	t3 = time.time()

	# # evaluation
	# tp = 0
	# fp = 0
	# fn = 0
	# wrdict = {}
	# for tup in resdict:
	# 	if (not tup[1] is None):
	# 		if (not tup[0] in gt.keys()):
	# 			print tup[0] + '---' + tup[1] + '---None'
	# 			fp += 1
	# 		elif (tup[1].lower() != gt[tup[0]].lower()):
	# 			print tup[0] + '---' + tup[1] + '---' + gt[tup[0]]
	# 			fp += 1
	# 		else:
	# 			wrdict[tup[0]] = -1
	# 			# print tup[0] + '---' + gt[tup[0]] + '---' + str(wrdict[tup[0]])
	# 			tp += 1
	# 	else:
	# 		if (tup[0] in gt.keys()):
	# 			if (not tup[0] in wrdict.keys()):
	# 				wrdict[tup[0]] = 0
	# 			if (wrdict[tup[0]] != -1):
	# 				wrdict[tup[0]] += 1
	# 			# print tup[0] + '---' + gt[tup[0]] + '---' + str(wrdict[tup[0]])
	# for wr in wrdict:
	# 	if (wrdict[wr] != -1):
	# 		fn += wrdict[wr]
	# 		print wr + '---' + gt[wr]
	# print 'tp: ' + str(tp)
	# print 'fp: ' + str(fp)
	# print 'fn: ' + str(fn)
	# print 'precision: ' + str((tp + .0) / (tp + fp))
	# print 'recall: ' + str((tp + .0) / (tp + fn))
	# print 'f1score: ' + str()

	t4 = time.time()

	print 't1-t0: ' + str(t1-t0)
	print 't2-t1: ' + str(t2-t1)
	print 't3-t2: ' + str(t3-t2)
	print 't4-t3: ' + str(t4-t3)

	fp2.close()
	fp1.close()
