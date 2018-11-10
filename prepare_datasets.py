import os
import sys
import numpy as np
import pandas as pd

inputfile = './data/aido99_all.txt'
# inputfile = './data/small_data.txt'
out_PAFI = './data/pafi_data.txt'
out_gSPAN = './data/gspan_data.txt'
gSPAN_labels = './data/gspan_v_labels.txt'
# out_GASTON= './data/gaston_data.txt'
graph_num = './data/graph_num.txt'

# with open(inputfile, 'r') as fr, open(out_PAFI, 'a') as fw:
# 	line = fr.readline()
# 	while line: 
# 		line = line.strip()
# 		if line[0]=='#':
# 			to_write = 't ' + str(line) + '\n'
# 			fw.write(to_write)

# 			# read vertices
# 			num_vertices = int(fr.readline().strip())
# 			for i in range(num_vertices):
# 				v_label = fr.readline()
# 				to_write = 'v ' + str(i) + ' ' + v_label
# 				fw.write(to_write)
# 			num_edges = int(fr.readline().strip())
# 			for i in range(num_edges):
# 				edge = fr.readline()
# 				to_write = 'u ' + edge
# 				fw.write(to_write)
# 		else:
# 			print(line + ' oooooooops !!!!')
# 			break	
# 		line = fr.readline()


vertex_labels = {}
curr_v_label = -1
with open(inputfile, 'r') as fr, open(gSPAN_labels, 'a') as f_label:
	line = fr.readline()
	t_num = -1
	while line: 
		t_num += 1 
		line = line.strip()
		if line[0]=='#':
			# read vertices
			num_vertices = int(fr.readline().strip())
			for i in range(num_vertices):
				v_label = fr.readline().rstrip()
				if v_label not in vertex_labels.keys():
					curr_v_label += 1
					vertex_labels[v_label] = curr_v_label
					f_label.write(str(curr_v_label) + ' ' + v_label+'\n')
			num_edges = int(fr.readline().strip())
			for i in range(num_edges):
				edge = fr.readline()
		else:
			print(line + ' oooooooops !!!!')
			break	
		line = fr.readline()


with open(inputfile, 'r') as fr, open(out_gSPAN, 'a') as fw, open(graph_num, 'a') as f_num:
	line = fr.readline()
	t_num = -1
	while line: 
		t_num += 1 
		line = line.strip()
		if line[0]=='#':
			to_write = 't # ' + str(t_num) + '\n'
			fw.write(to_write)
			f_num.write(line[1:] + '\n')

			# read vertices
			num_vertices = int(fr.readline().strip())
			for i in range(num_vertices):
				v_label = fr.readline().rstrip()
				to_write = 'v ' + str(i) + ' ' + str(vertex_labels[v_label]) + '\n'
				fw.write(to_write)
			# read edges
			num_edges = int(fr.readline().strip())
			for i in range(num_edges):
				edge = fr.readline()
				edge_nums = edge.split(" ")
				to_write = 'e ' + edge_nums[0] + " " + edge_nums[1] + " " +  str(int(edge_nums[2])-1) + "\n"
				fw.write(to_write)
				
		else:
			print(line + ' oooooooops !!!!')
			break	
		line = fr.readline()



				