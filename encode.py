import numpy as np
import subprocess
from collections import OrderedDict
import networkx as nx
from networkx.algorithms import isomorphism

labels_active = './data/ca.txt'
labels_inactive = './data/ci.txt'
inputfile = './data/aido99_all.txt'
# inputfile = './data/small_data.txt'
out_gSPAN = './data/gspan_data.txt'
gSPAN_labels = './data/gspan_v_labels.txt'
graph_num = './data/graph_num.txt'
min_sup = 0.5

labels = OrderedDict()

# define labels for each graph
with open(labels_active, 'r') as fr_a:
	line = fr_a.readline()
	while line:
		line = line.strip().split()
		graph_id = int(line[0])
		labels[graph_id] = 1
		line = fr_a.readline()
fr_a.close()

with open(labels_inactive, 'r') as fr_i:
	line = fr_i.readline()
	while line:
		line = line.strip().split()
		graph_id = int(line[0])
		labels[graph_id] = -1
		line = fr_i.readline()
fr_i.close()

num_a = list(labels.values()).count(1)
num_i = list(labels.values()).count(-1)

print(num_a+num_i)

vertex_labels = OrderedDict()
curr_v_label = -1

total_graphs = 0
unlabelled = 0

##############################
# writing dictionary for mapping node labels to unique numbers
with open(inputfile, 'r') as fr, open(gSPAN_labels, 'a') as f_label:
	line = fr.readline()
	t_num = -1
	while line: 
		line = line.strip()
		if len(line)==0:
			break
		if line[0]=='#':
			total_graphs+=1
			graph_id = int(line[1:])
			# if label for current graph exists
			if graph_id in labels.keys():
				t_num += 1 
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
				unlabelled+=1
				line = fr.readline()
				continue	
		line = fr.readline()

# print(total_graphs)
# print(unlabelled)
# exit()

total_graphs = total_graphs-unlabelled

##############################
# writing datafile for gSpan
with open(inputfile, 'r') as fr, open(out_gSPAN, 'a') as fw, open(graph_num, 'a') as f_num:
	line = fr.readline()
	t_num = -1
	while line: 
		line = line.strip()
		if len(line)==0:
			break
		if line[0]=='#':
			graph_id = int(line[1:])
			# if label for current graph exists
			if graph_id in labels.keys():
				t_num += 1
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
				line = fr.readline()
				continue
		line = fr.readline()
	fw.write("t # -1\n")

###############################################################################################################
########################################## embeddings for LIBSVM ##############################################


############################################################
### run gSpan to generate subgraph_file
# -------------------------- run gSpan from bash --------------------------
# subprocess.run("gSpan -f " + out_gSPAN + " -s " + min_sup + " -o -i", shell=True, check=True)
############################################################


subgraph_file = './data/freq subgraphs/50_gspan_data.txt.fp'
# subgraph_file = out_gSPAN+".fp"
encoding_file = './data/total_encode.txt'
map_graph_id = './data/graph_num.txt'
active_encode_file = './data/a_encode.txt'
inactive_encode_file = './data/i_encode.txt'

total_graphs = t_num + 1

graph_ids = []

##############################
# mapping from ordered graph_id to actual graph_id
with open(map_graph_id, 'r') as fr_id:
	line = fr_id.readline()
	while line:
		line = line.strip().split()
		graph_id = int(line[0])
		graph_ids.append(graph_id)
		line = fr_id.readline()
fr_id.close()


##############################
######## find discriminative subgraphs ###############
# num_active = list(labels.values()).count(1)
# num_inactive = list(labels.values()).count(-1)
num_active = 252
num_inactive = 21619

sup_active = round((num_active/total_graphs),3)
sup_inactive = round((num_inactive/total_graphs),3)

print(sup_active)
print(sup_inactive)
# exit()

discriminative_subgraph_ids = []
_iter=0
with open(subgraph_file, 'r') as fr:
	line = fr.readline()
	while line:
		line = line.strip().split()
		if len(line)!=0:
			if line[0]=='t':
				subgraph_id = int(line[2])
				_iter+=1
				num_total = int(line[4])
				num_curr_active = 0
				num_curr_inactive = 0
			elif line[0]=='x':
				for i in range(1,len(line)):
					ord_graph_id = int(line[i])
					act_graph_id = graph_ids[ord_graph_id]
					curr_lab = labels[act_graph_id]
					if curr_lab==1:
						num_curr_active+=1
					if curr_lab==-1:
						num_curr_inactive+=1
		else:
			curr_sup_active = round(num_curr_active/float(num_total),3)
			curr_sup_inactive = round(num_curr_inactive/float(num_total),3)
			if (curr_sup_active>=sup_active and curr_sup_inactive<sup_inactive) or (curr_sup_active<sup_active and curr_sup_inactive>=sup_inactive) :
				# print(_iter, curr_sup_active, curr_sup_inactive)
				discriminative_subgraph_ids.append(subgraph_id)

		line = fr.readline()
fr.close()

total_subgraphs = len(discriminative_subgraph_ids)
print(total_subgraphs)
discriminative_subgraph_ids = OrderedDict(zip(discriminative_subgraph_ids, np.arange(total_subgraphs)))


##############################
# read subgraphs and form binary feature vector for each graph

# for line in reversed(list(open(subgraph_file))):
# 	line = line.strip().split()
# 	if len(line)!=0 and line[0]=='t':
# 		total_subgraphs = int(line[2]) + 1
# 		break

zeros = np.zeros(total_subgraphs, dtype=np.int8)
d_keys = np.arange(total_subgraphs)
feature_arr = OrderedDict()
for i in range(total_graphs):
	d = OrderedDict(zip(d_keys, zeros))
	feature_arr[i] = d

sup = OrderedDict()

with open(subgraph_file, 'r') as fr:
	line = fr.readline()
	subgraph_id = -1
	while line:
		line = line.strip().split()
		if len(line)!=0:
			if line[0]=='t':
				# print("--->>> " + line[2])
				# subgraph_id += 1 
				subgraph_id = int(line[2])
				if subgraph_id in discriminative_subgraph_ids.keys():
					sup[subgraph_id] = int(line[4])
			elif line[0]=='x' and subgraph_id in discriminative_subgraph_ids.keys():
				# for each graph for which current subgraph is frequent
				print(f'SUBGRAPH_ID: {subgraph_id} ----  #subgraphs: {len(line)-1}')
				# print(f'------------------------------>>>>>>>> {line[21421]} {line[21422]} {line[21423]}')
				for i in range(1,len(line)):
					# for every number
					ord_graph_id = int(line[i])
					act_graph_id = graph_ids[ord_graph_id]
					curr_graph_feature_arr = feature_arr[ord_graph_id]
					curr_graph_feature_arr[discriminative_subgraph_ids[subgraph_id]] = 1
					# print(f'Done: Subgraph ID={subgraph_id} --- Ordered Graph ID={line[i]} ---- Actual Graph ID={act_graph_id}')
					# if (i%5000)==0:
						# print(f'Ordered Graph ID={line[i]} ---- Bin_Vec={curr_graph_feature_arr}')

		line = fr.readline()
fr.close()

# print(sup)


##############################
# write the file for libsvm
with open(encoding_file, 'a') as fw, open(active_encode_file, 'a') as fw_a, open(inactive_encode_file, 'a') as fw_i:
	for i in range(total_graphs):
		# write label of the ith graph
		actual_graph_id = graph_ids[i]
		label = str(labels[actual_graph_id])
		embedding = str(feature_arr[i]).replace(" ", "")
		embedding = embedding.replace(",", " ")
		embedding = embedding.replace("}", "")
		embedding = embedding.replace("{", "")
		if int(label)==1:
			fw_a.write(str(i)+ " " +embedding+ "\n")
		if int(label)==-1:
			fw_i.write(str(i)+ " " +embedding+ "\n")
		fw.write(label + " " + embedding + "\n")

fw.close()


####################################################################################################
########## apply CORK to further discriminate features ##########
# -------------------------- run Sanyam's .cpp code --------------------------
#####################################################################################################


##############################
# make list of CORK discriminative subgraphs

cork_feature_file = './data/cork_features.txt'

with open(cork_feature_file,'r') as fr:
	line =fr.readline()
	line = line.strip().split(" ")
fr.close()

reversed_discriminative_subgraph_ids = OrderedDict(map(reversed, discriminative_subgraph_ids.items()))
final_discriminative_subgraphs = []

with x in line:
	cork_subgraph_id = int(x)
	gspan_subgraph_id = reversed_discriminative_subgraph_ids[cork_subgraph_id]
	final_discriminative_subgraphs.append(gspan_subgraph_id)

total_cork_subgraphs = len(final_discriminative_subgraphs)
print(total_cork_subgraphs)
cork_subgraph_ids = OrderedDict(zip(final_discriminative_subgraphs, np.arange(total_cork_subgraphs)))


##############################
# read cork dicriminative subgraphs from gSpan subgraph file
list_cork_subgraph_objects = []
final_discriminative_subgraphs_read_order = []

with open(subgraph_file, 'r') as fr:
	line = fr.readline()
	while line: 
		line = line.strip()
		if len(line)!=0:
			if line[0]=='t':
				subgraph_id = int(line[2])
				# if subgraph is discriminative, store the graph
				if subgraph_id in cork_subgraph_ids.keys():
					final_discriminative_subgraphs_read_order.append(subgraph_id)
					G = nx.Graph()
					line = fr.readline().split(" ")
					while line[0]!='x':
						if line[0]=='v':
							G.add_node(int(line[1]), label=int(line[2]))
						elif line[0]=='e':
							G.add_edge(int(line[1]), int(line[2]), label=int(line[3]))
						line = fr.readline().split(" ")
					list_cork_subgraph_objects.append(G)
		line = fr.readline()
fr.close()


##############################
# Ordering the subgraphs 
#(order of subgraphs read should be same as decalared by cork)
order_subgraph_features_1 = OrderedDict(zip(final_discriminative_subgraphs, final_discriminative_subgraphs_read_order))
order_subgraph_features_2 = OrderedDict(zip(final_discriminative_subgraphs_read_order, list_cork_subgraph_objects))

ordered_list_cork_subgraph_objects = []

for freq_id in order_subgraph_features_1.keys():
	sg = order_subgraph_features_2[order_subgraph_features_1[freq_id]]
	ordered_list_cork_subgraph_objects.append(sg)


##############################
# check for these graphs in the test file
test_file = './data/test.txt'
encode_test = './data/encode_test.txt'

cork_zeros = np.zeros(len(ordered_list_cork_subgraph_objects), dtype=np.int8)
cork_d_keys = np.arange(len(ordered_list_cork_subgraph_objects))

# parse test file (aido format)
with open(test_file, 'r') as fr, open(encode_test, 'a') as fw:
	line = fr.readline()
	while line: 
		line = line.strip()
		if len(line)==0:
			break
		if line[0]=='#':
			G=nx.Graph()
			# read vertices
			num_vertices = int(fr.readline().strip())
			for i in range(num_vertices):
				v_alpha_label = fr.readline().rstrip()
				v_num_label = vertex_labels[v_alpha_label]
				G.add_node(int(i), label=v_num_label)
			num_edges = int(fr.readline().strip())
			for i in range(num_edges):
				edge = fr.readline()
				edge_nums = edge.split(" ")
				G.add_edge(int(edge_nums[0]),int(edge_nums[1]),label=int(edge_nums[2]))
			# check for all subgraphs in G
			binary_vector = OrderedDict(zip(cork_d_keys, cork_zeros))
			for key, G_freq in enumerate(ordered_list_cork_subgraph_objects):
				GM = isomorphism.GraphMatcher(G,G_freq)
				is_isomorph = GM.subgraph_is_isomorphic()
				if is_isomorph:
					binary_vector[key] = 1
				else:
					binary_vector[key] = 0

			embedding = str(binary_vector).replace(" ", "")
			embedding = embedding.replace(",", " ")
			embedding = embedding.replace("}", "")
			embedding = embedding.replace("{", "")
			fw.write(embedding + "\n")

		line = fr.readline()
fr.close()
fw.close()



