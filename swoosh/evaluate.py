from evaluator import evaluator


class evaluate:

	def __init__(self, num, lencora, resultfile, answerfile):
		self.num = num
		self.lencora = lencora
		fp = open('logs/merge_log.txt')
		self.pairs = [line.strip().split('-') for line in fp]
		self.marks = [0 for _ in xrange(lencora)]
		self.clusters = [set() for _ in xrange(num)]
		self.setnum = 0
		self.resultfile = resultfile
		self.answerfile = answerfile
		fp.close()

	def _bfs(self, x):
		if (self.marks[x] == 1):
			return
		self.marks[x] = 1
		self.clusters[self.setnum].add(x)
		neighbors = set()
		for pair in self.pairs:
			if (pair[0] == str(x)):
				neighbors.add(int(pair[1]))
			if (pair[1] == str(x)):
				neighbors.add(int(pair[0]))
		for neighbor in neighbors:
			self._bfs(neighbor)

	def do(self):
		i = 0
		while (i < self.lencora):
			if (self.marks[i] == 0):
				self._bfs(i)
				self.setnum += 1
			i += 1
		s = 0
		res = []
		fp = open(self.resultfile, 'w+')
		for i in xrange(len(self.clusters)):
			s += len(self.clusters[i])
			tmp = list(self.clusters[i])
			res.append(tmp)
			for j in xrange(len(tmp)):
				if (j == len(tmp) - 1):
					fp.write(str(tmp[j]) + '\n')
				else:
					fp.write(str(tmp[j]) + ' ')
		fp.close()
		fp = open(self.answerfile)
		lines = [line.strip().split() for line in fp]
		ans = []
		for line in lines:
			tmp = []
			for j in xrange(len(line)):
				tmp.append(int(line[j]))
			ans.append(tmp)
		ev = evaluator(self.lencora)
		ev.load_answer_clusters(ans)
		ev.evaluate_clusters(res)
