from evaluator import evaluator


pairs = None
marks = None
clusters = None
setnum = 0


def debugWrite(x):
	fp = open('debug.txt', 'w+')
	for _x in x:
		fp.write(str(_x) + '\n')
	fp.close()


def bfs(x):
	global pairs
	global marks
	global clusters
	global setnum

	if (marks[x] == 1):
		return
	marks[x] = 1
	clusters[setnum].add(x)
	neighbors = set()
	for pair in pairs:
		if (pair[0] == str(x)):
			neighbors.add(int(pair[1]))
		if (pair[1] == str(x)):
			neighbors.add(int(pair[0]))
	for neighbor in neighbors:
		bfs(neighbor)


# 3000 bring
# 1700 return 1nd housing
# 400 return 2nd housing (pending)
# -1000 2nd housing
# -600 2nd housing
# -15 boat
# -30 tussand
# -80 studio
# -10 rap
# -15 cap
# -10 cards
# -45 san diego
# -75 san diego
# -15 san diego
# -20 san diego
# -65 san diego
# -15*30 meal
# -30 travel
# -30 taxi
# -10 basketball


if __name__ == '__main__':

	num = 116 # please change this manually
	lencora = 1295 # total number of records

	fp = open('logs/merge_log.txt')
	pairs = [line.strip().split('-') for line in fp]
	marks = [0 for _ in xrange(lencora)]
	clusters = [set() for _ in xrange(num)]
	fp.close()

	setnum = 0
	i = 0
	while (i < lencora):
		if (marks[i] == 0):
			bfs(i)
			setnum += 1
		i += 1

	s = 0
	res = []
	fp = open('clusters.txt', 'w+')
	for i in xrange(len(clusters)):
		s += len(clusters[i])
		tmp = list(clusters[i])
		res.append(tmp)
		for j in xrange(len(tmp)):
			if (j == len(tmp) - 1):
				fp.write(str(tmp[j]) + '\n')
			else:
				fp.write(str(tmp[j]) + ' ')
	print s
	fp.close()

	fp = open('cora-clusters.txt')
	lines = [line.strip().split() for line in fp]
	ans = []
	for line in lines:
		tmp = []
		for j in xrange(len(line)):
			tmp.append(int(line[j]))
		ans.append(tmp)

	ev = evaluator(1295)
	ev.load_answer_clusters(ans)
	ev.evaluate_clusters(res)