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


if __name__ == '__main__':

	num = 89 # please change this manually
	lencora = 1295

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
	fp = open('clusters.txt', 'w+')
	for cluster in clusters:
		s += len(cluster)
		fp.write(str(list(cluster)) + '\n')
	print s
	fp.close()