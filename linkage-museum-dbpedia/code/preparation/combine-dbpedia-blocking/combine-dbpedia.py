def read_fragment(fname):
	fp = open(fname)
	lines = [line.strip() for line in fp]
	res = []
	i = 0
	while (i < len(lines)):
		tmp = []
		assert (lines[i][0] == '<'), 'error: [read_fragment] format error'
		kvalue = lines[i].replace('<index>', '').replace('</index>', '')

		j = i + 1
		while (j != len(lines)-1) and (lines[j+1][0] != '<'):
			j += 1
		for k in xrange(i+1, j+1):
			tmp.append(int(lines[k].split(',')[1]))
		res.append(tuple([kvalue, tmp]))
		i = j + 1
	fp.close()
	return res

def read_all():
	first = '123456789abcdef'
	last = '1234567890abcdef&'
	res = []
	for i in xrange(len(first)):
		for j in xrange(len(last)):
			fn = ''
			if (last[j] == '&'):
				fn = first[i]
			else:
				fn = first[i] + last[j]
			try:
				res += read_fragment('data/' + fn)
			except:
				print 'file not exist: ' + fn
	return res

def dump_all(r):
	fp = open('dbpedia-blocked.txt', 'w+')
	for i in xrange(len(r)):
		fp.write(r[i][0] + ', ')
		for j in xrange(len(r[i][1])):
			fp.write(str(r[i][1][j]) + ' ')
		fp.write('\n')
	fp.close()

if __name__ == '__main__':
	res = read_all()
	dump_all(res)