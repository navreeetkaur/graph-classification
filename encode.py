import sys
import numpy as np
import subprocess
from collections import OrderedDict
import networkx as nx
import networkx.algorithms.isomorphism as iso
import time

# inputfile = './data/train_aids.txt'
# labels_active = './data/ca.txt'
# labels_inactive = './data/ci.txt'
# test_file = './data/test_aids.txt'
inputfile = sys.argv[1]
labels_active = sys.argv[2]
labels_inactive = sys.argv[3]
test_file = sys.argv[4]

encode_test = 'test.txt'
encoding_file = 'train.txt'
out_gSPAN_a = './data/a_gspan_data.txt'
out_gSPAN_i = './data/i_gspan_data.txt'
gSPAN_labels = './data/gspan_v_labels.txt'
graph_num = './data/graph_num.txt'
graph_num_a = './data/graph_num_a.txt'
graph_num_i = './data/graph_num_i.txt'
min_sup_a = 0.6
min_sup_i = 0.8

labels = OrderedDict()
# nx.Graph objects of all graphs in training set
all_graphs = []

step0 = time.time()

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

vertex_labels = {}
curr_v_label = -1

total_graphs = 0
unlabelled = 0

##############################
# writing dictionary for mapping node labels to unique numbers
with open(inputfile, 'r') as fr, open(gSPAN_labels, 'w') as f_label:
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

total_graphs = total_graphs-unlabelled
print(total_graphs)


graph_ids = []
graph_ids_i = OrderedDict()
graph_ids_a = OrderedDict()

step1 = time.time()

##############################
# writing datafile for gSpan
with open(inputfile, 'r') as fr, open(out_gSPAN_a, 'w') as fw_a, open(out_gSPAN_i, 'w') as fw_i:#, open(graph_num_a, 'w') as f_num_a, open(graph_num_i, 'w') as f_num_i, open(graph_num, 'w') as f_num :
	line = fr.readline()
	t_num_a = -1
	t_num_i = -1
	t_num = -1
	while line: 
		line = line.strip()
		if len(line)==0:
			break
		if line[0]=='#':
			graph_id = int(line[1:])
			# if label for current graph exists
			if graph_id in labels.keys():
				t_num +=1
				if labels[graph_id]==1:
					t_num_a +=1
					to_write = 't # ' + str(t_num_a) + '\n'
					fw_a.write(to_write)
					graph_ids_a[int(t_num)] = t_num_a
					# f_num_a.write(str(t_num)+" "+line[1:] + '\n')
				else:
					t_num_i +=1
					to_write = 't # ' + str(t_num_i) + '\n'
					fw_i.write(to_write)
					graph_ids_i[int(t_num)] = t_num_i
					# f_num_i.write(str(t_num)+" "+line[1:] + '\n')
				# f_num.write(line[1:] + '\n')
				graph_ids.append(graph_id)
				G = nx.Graph()
				# read vertices
				num_vertices = int(fr.readline().strip())
				for i in range(num_vertices):
					v_label = fr.readline().rstrip()
					to_write = 'v ' + str(i) + ' ' + str(vertex_labels[v_label]) + '\n'
					if labels[graph_id]==1:
						fw_a.write(to_write)
					else:
						fw_i.write(to_write)
					G.add_node(i, label=vertex_labels[v_label])
				# read edges
				num_edges = int(fr.readline().strip())
				for i in range(num_edges):
					edge = fr.readline()
					edge_nums = edge.split(" ")
					G.add_edge(int(edge_nums[0]), int(edge_nums[1]), label=int(edge_nums[2])-1)
					to_write = 'e ' + edge_nums[0] + " " + edge_nums[1] + " " +  str(int(edge_nums[2])-1) + "\n"
					if labels[graph_id]==1:
						fw_a.write(to_write)
					else:
						fw_i.write(to_write)
				all_graphs.append(G)
			else:
				line = fr.readline()
				continue
		line = fr.readline()
	# fw_a.write("t # -1\n")
	# fw_i.write("t # -1\n")


## check 
# g_id = 654077
# g_id = 699751
# idx = graph_ids.index(g_id)
# if idx in graph_ids_a:
# 	print("a", graph_ids_a[idx])
# if idx in graph_ids_i:
# 	print("i", graph_ids_i[idx])
# exit()

step2 = time.time()
print(f'Done writing files for gSpan: {step2-step1}')

# ###############################################################################################################
# ########################################## embeddings for LIBSVM ##############################################

# ############################################################
# ### run gSpan to generate subgraph_file
# # # -------------------------- run gSpan from bash --------------------------
subprocess.run("./gSpan6/gSpan -f "+out_gSPAN_i+" -s "+str(min_sup_i)+" -o -i", shell=True, check=True)
subprocess.run("./gSpan6/gSpan -f "+out_gSPAN_a+" -s "+str(min_sup_a)+" -o -i", shell=True, check=True)
############################################################

step3 = time.time()
print(f'Mined frequent items: {step3-step2}')

# subgraph_file = './data/gspan_data.txt.fp'
subgraph_file_i = out_gSPAN_i+".fp"
subgraph_file_a = out_gSPAN_a+".fp"
map_graph_id = './data/graph_num.txt'
map_graph_id_i = './data/graph_num_i.txt'
map_graph_id_a = './data/graph_num_a.txt'
active_encode_file = './data/a_encode.txt'
inactive_encode_file = './data/i_encode.txt'

total_graphs = t_num_i + t_num_a + 2
num_active = t_num_a + 1
num_inactive = t_num_i + 1

## check
# print(total_graphs)
# print(num_active)
# print(num_inactive)
# exit()

##############################
######## find discriminative subgraphs ###############
sup_active = round((num_active/total_graphs),3)
sup_inactive = round((num_inactive/total_graphs),3)

print(sup_active)
print(sup_inactive)

discriminative_subgraph_ids = []
_iter=0
inactive_subgraphs = []
active_subgraphs = []
G_i = []
G_a = []

# read active subgraphs as objects
## check
# index =0
with open(subgraph_file_a, 'r') as fr:
	line = fr.readline()
	while line: 
		line = line.strip().split()
		if len(line)!=0:
			if line[0]=='t':
				G = nx.Graph()
				## check
				# if index==5:
				# 	curr_sup = print(int(line[4]))
				G_as = []
				line = fr.readline().split(" ")
				while line[0]!='x':
					if line[0]=='v':
						G.add_node(int(line[1]), label=int(line[2]))
					elif line[0]=='e':
						G.add_edge(int(line[1]), int(line[2]), label=int(line[3]))
					line = fr.readline().split(" ")
				if line[0]=='x':
					for i in line[1:len(line)-1]:
						G_as.append(int(i))
				## check
				# index+=1
				# if index==5:
				# 	print(len(G_as))
				# 	exit()
				G_a.append(G_as)
				active_subgraphs.append(G)
				
		line = fr.readline()
fr.close()

# read inactive subgraphs as objects
with open(subgraph_file_i, 'r') as fr:
	line = fr.readline()
	while line: 
		line = line.strip().split()
		if len(line)!=0:
			if line[0]=='t':
				G = nx.Graph()
				G_is = []
				line = fr.readline().split(" ")
				while line[0]!='x':
					if line[0]=='v':
						G.add_node(int(line[1]), label=int(line[2]))
					elif line[0]=='e':
						G.add_edge(int(line[1]), int(line[2]), label=int(line[3]))
					line = fr.readline().split(" ")
				if line[0]=='x':
					for i in line[1:len(line)-1]:
						G_is.append(int(i))
				G_i.append(G_is)
				inactive_subgraphs.append(G)
		line = fr.readline()
fr.close()


## check
# G = inactive_subgraphs[43]
# print(G.nodes())
# print(G.edges())
# print(G[0][1]['label'])
# exit()
## check
# print(len(active_subgraphs))
# print(len(G_a))
# print(len(inactive_subgraphs))
# print(len(G_i))
# exit()

discriminative_a = []
discriminative_i = []

for i in range(len(active_subgraphs)):
	is_isomorph = False
	for j in range(len(inactive_subgraphs)):
		is_isomorph = nx.is_isomorphic(active_subgraphs[i], inactive_subgraphs[j], node_match=iso.categorical_node_match('label', ''),  edge_match=iso.categorical_node_match('label', ''))
		if is_isomorph:
			break
	if not is_isomorph:
		discriminative_a.append(i)

# for i in range(len(inactive_subgraphs)):
# 	is_isomorph = False
# 	for j in range(len(active_subgraphs)):
# 		is_isomorph = nx.is_isomorphic(inactive_subgraphs[i], active_subgraphs[j], node_match=iso.categorical_node_match('label', ''),  edge_match=iso.categorical_node_match('label', ''))
# 		if is_isomorph:
# 			break
# 	if not is_isomorph:
# 		discriminative_i.append(i)

# ## check 
# print(discriminative_i)
# print(discriminative_a)
# discriminative_i = list(set(discriminative_i))
# discriminative_a = list(set(discriminative_a))
# print()
# print(discriminative_i)
# print(discriminative_a)
# exit()

# discriminative_i = list(set(discriminative_i))
discriminative_i = list(np.arange(len(inactive_subgraphs)), dtype=np.int8)
discriminative_a = list(set(discriminative_a))
print(len(discriminative_i))
print(len(discriminative_a))

# Graph objects
discriminative_subgraphs = []
# indexes
Graphs = []
i_a = []

for i in range(len(discriminative_i)):
	discriminative_subgraphs.append(inactive_subgraphs[discriminative_i[i]])
	Graphs.append(G_i[discriminative_i[i]])
	i_a.append(-1)

for i in range(len(discriminative_a)):
	discriminative_subgraphs.append(active_subgraphs[discriminative_a[i]])
	Graphs.append(G_a[discriminative_a[i]])
	i_a.append(1)

step4 = time.time()
print(f'Found discriminative subgraphs: {step4-step3}')

## check
# print(len(discriminative_subgraphs)) 
# print(len(Graphs))
# print(len(Graphs[7]))
# exit()

# print()
# print(discriminative_subgraphs[5].nodes())
# print(discriminative_subgraphs[5].edges())
# # print(discriminative_subgraphs[5][0]['label'])
# # print(discriminative_subgraphs[5][1]['label'])
# # print(discriminative_subgraphs[5][2]['label'])
# # print(discriminative_subgraphs[5][3]['label'])
# print(discriminative_subgraphs[5][0][1]['label'])
# print(discriminative_subgraphs[5][1][2]['label'])
# print(discriminative_subgraphs[5][2][3]['label'])
# print()
# exit()

##############################
# read subgraphs and form binary feature vector for each graph
total_subgraphs = len(discriminative_subgraphs)

zeros = np.zeros(total_subgraphs, dtype=np.int8)
d_keys = np.arange(total_subgraphs)
feature_arr = {}

for i in range(total_graphs):
	d = dict(zip(d_keys, zeros))
	feature_arr[i] = d

print(total_graphs)
items_graph_ids_i = list(graph_ids_i.items())
items_graph_ids_a = list(graph_ids_a.items())

for i in range(total_subgraphs):
	label = i_a[i]
	if label==-1:
		for freq_graph in Graphs[i]:
			ord_graph_id = items_graph_ids_i[freq_graph][0]
			curr_graph_feature_arr = feature_arr[ord_graph_id]
			curr_graph_feature_arr[i] = 1
	else:
		for freq_graph in Graphs[i]:
			ord_graph_id = items_graph_ids_a[freq_graph][0]
			curr_graph_feature_arr = feature_arr[ord_graph_id]
			curr_graph_feature_arr[i] = 1

items_labels = list(labels.items())
# check for inactive freq subgraphs in active graphs
for i in range(len(all_graphs)):
	G = all_graphs[i]
	if items_labels[i][1]==1:
		for j in range(len(i_a)):
			if i_a[j]==-1:
				SG = discriminative_subgraphs[j]
				GM = iso.GraphMatcher(G, SG,node_match=iso.categorical_node_match('label', ''),  edge_match=iso.categorical_node_match('label', ''))
				is_isomorph = GM.subgraph_is_isomorphic()
				if is_isomorph:
					curr_graph_feature_arr = feature_arr[i]
					curr_graph_feature_arr[j] = 1
	if items_labels[i][1]==-1:
		for j in range(len(i_a)):
			if i_a[j]==1:
				SG = discriminative_subgraphs[j]
				GM = iso.GraphMatcher(G, SG,node_match=iso.categorical_node_match('label', ''),  edge_match=iso.categorical_node_match('label', ''))
				is_isomorph = GM.subgraph_is_isomorphic()
				if is_isomorph:
					curr_graph_feature_arr = feature_arr[i]
					curr_graph_feature_arr[j] = 1

step5 = time.time()
print(f'Made binary features for Train: {step5 -step4}')
##############################
# write the file for CORK
with open(encoding_file, 'w') as fw, open(active_encode_file, 'w') as fw_a, open(inactive_encode_file, 'w') as fw_i:
	for i in range(total_graphs):
		# write label of the ith graph
		actual_graph_id = graph_ids[i]
		label = str(labels[actual_graph_id])
		embedding = str(feature_arr[i]).replace(" ", "")
		embedding = embedding.replace(",", " ")
		embedding = embedding.replace("}", "")
		embedding = embedding.replace("{", "")
		bin_vec = str(list(feature_arr[i].values()))
		bin_vec = bin_vec.replace(" ", "")
		bin_vec = bin_vec.replace("[", "")
		bin_vec = bin_vec.replace("]", "")
		if int(label)==1:
			fw_a.write(str(i)+ "," +bin_vec+ "\n")
		if int(label)==-1:
			embedding = embedding.replace(":", ",")
			fw_i.write(str(i)+ "," +bin_vec+ "\n") 
		new_embedding = str(feature_arr[i]).replace(" ", "")
		new_embedding = new_embedding.replace(",", " ")
		new_embedding = new_embedding.replace("}", "")
		new_embedding = new_embedding.replace("{", "")
		# uncomment to write file for LIBSVM
		fw.write(label + " " + new_embedding + "\n")
fw.close()

step6 = time.time()
print(f'Made binary features for Train: {step6-step5}')
# exit()
# ####################################################################################################
# ########## apply CORK to further discriminate features ##########
# # -------------------------- run Sanyam's .cpp code --------------------------
# # subprocess.run("", shell=True, check=True)
# #####################################################################################################


##############################
# make list of CORK discriminative subgraphs
# cork_feature_file = './data/cork_features.txt'

# with open(cork_feature_file,'r') as fr:
# 	line =fr.readline()
# 	line = line.strip().split(" ")
# fr.close()

# # # maps order to DELTA subgraphs
# # reversed_discriminative_subgraph_ids = OrderedDict(map(reversed, discriminative_subgraph_ids.items()))
# final_discriminative_subgraphs = []

# # print(reversed_discriminative_subgraph_ids)
# for x in line:
# 	cork_subgraph_id = int(x)
# 	# print(cork_subgraph_id)
# 	# gspan_subgraph_id = reversed_discriminative_subgraph_ids[cork_subgraph_id]
# 	final_discriminative_subgraphs.append(cork_subgraph_id)

# # IDs in 'final_discriminative_subgraphs' correspond to order in original subgraph IDs in gSpan FSM
# total_cork_subgraphs = len(final_discriminative_subgraphs)
# # print(total_cork_subgraphs)
# final_discriminative_subgraphs.sort()

# ##############################
# # read cork dicriminative subgraphs from gSpan subgraph file
# cork_subgraph_objects = []

# with open(subgraph_file, 'r') as fr:
# 	line = fr.readline()
# 	while line: 
# 		line = line.strip().split()
# 		if len(line)!=0:
# 			if line[0]=='t':
# 				subgraph_id = int(line[2])
# 				# if subgraph is discriminative, store the graph
# 				if subgraph_id in final_discriminative_subgraphs:
# 					G = nx.Graph()
# 					line = fr.readline().split(" ")
# 					while line[0]!='x':
# 						if line[0]=='v':
# 							G.add_node(int(line[1]), label=int(line[2]))
# 						elif line[0]=='e':
# 							G.add_edge(int(line[1]), int(line[2]), label=int(line[3]))
# 						line = fr.readline().split(" ")
# 					cork_subgraph_objects.append(G)
# 		line = fr.readline()
# fr.close()

# ##############################
# # Ordering the subgraphs 
# # order of subgraphs read should be same as decalared by cork) - ensured already by
# #  sorting of 'final_discriminative_subgraphs', given the subgraph IDs in gSpan file appear in order starting from 0
# order_subgraph_features = OrderedDict(zip(final_discriminative_subgraphs,cork_subgraph_objects))
# ordered_list_cork_subgraph_objects = order_subgraph_features.values()

##############################
# check for these graphs in the test file

zeros = np.zeros(len(discriminative_subgraphs), dtype=np.int8)
keys = np.arange(len(discriminative_subgraphs))
# print(len(discriminative_subgraphs))
print("Writing test file . . .")

# parse test file (aido format)
with open(test_file, 'r') as fr, open(encode_test, 'w') as fw:
	line = fr.readline()
	while line: 
		line = line.strip()
		if len(line)==0:
			break
		if line[0]=='#':
			graph_id = int(line[1:])
			curr_label = str(labels[graph_id])
			G=nx.Graph()
			# read vertices
			num_vertices = int(fr.readline().strip())
			for i in range(num_vertices):
				v_alpha_label = fr.readline().rstrip()
				if v_alpha_label in vertex_labels.keys():
					v_num_label = int(vertex_labels[v_alpha_label])
				else:
					v_num_label = len(list(vertex_labels.keys()))
				G.add_node(int(i), label=v_num_label)
			num_edges = int(fr.readline().strip())
			for i in range(num_edges):
				edge = fr.readline()
				edge_nums = edge.split(" ")
				G.add_edge(int(edge_nums[0]),int(edge_nums[1]),label=int(edge_nums[2])-1)
			# print(G.nodes())
			# print(G.edges())
			# print(G[1][])
			# exit()
			# check for all subgraphs in G
			binary_vector = dict(zip(keys, zeros))

			for i in range(len(discriminative_subgraphs)):
				# index = final_discriminative_subgraphs[i]
				G_freq = discriminative_subgraphs[i]
				GM = iso.GraphMatcher(G,G_freq,node_match=iso.categorical_node_match('label', ''),  edge_match=iso.categorical_node_match('label', ''))
				is_isomorph = GM.subgraph_is_isomorphic()
				if is_isomorph:
					binary_vector[i] = 1
				else:
					binary_vector[i] = 0
			# for key, G_freq in enumerate(ordered_list_cork_subgraph_objects):
			# 	GM = isomorphism.GraphMatcher(G,G_freq)
			# 	is_isomorph = GM.subgraph_is_isomorphic()
			# 	if is_isomorph:
			# 		binary_vector[key] = 1
			# 	else:
			# 		binary_vector[key] = 0
			new_embedding = str(binary_vector).replace(" ", "")
			new_embedding = new_embedding.replace(",", " ")
			new_embedding = new_embedding.replace("}", "")
			new_embedding = new_embedding.replace("{", "")
			# fw.write(curr_label+" "+new_embedding + "\n")
			fw.write(new_embedding + "\n")

		line = fr.readline()
fr.close()
fw.close()

step7 = time.time()
print(f'Made binary features for Test: {step7-step6}')



