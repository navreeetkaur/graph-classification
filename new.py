with open('test.txt', 'r') as fr, open('new_test.txt', 'w') as fw:
	line = fr.readline()
	i = 0
	while line:
		if i<=50:
			fw.write("1 "+line)
		else:
			fw.write("-1 "+line)
		line = fr.readline()
		i+=1