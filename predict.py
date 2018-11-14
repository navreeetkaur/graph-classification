import numpy as np 
from random import shuffle
from sklearn.metrics import f1_score, precision_recall_fscore_support, fbeta_score

################ change the training input to include equal active and inactive molecules ######################

train_file = './data/50_bin_encode.txt'
new_train_file = './data/train.txt'


# Randomly pick a set of inactive instances with size equal to number of total active instances in training set
# Generate new training and testing file


num_a = 317
num_i = 22038

lines_i = []

with open(train_file, 'r') as fr, open(new_train_file, 'a') as fw:
	full_line = fr.readline()
	while full_line:
		line = full_line.split(" ")
		if len(line)!=0:
			label = int(line[0])
			if label==-1:
				lines_i.append(full_line)
			else:
				fw.write(full_line)
		full_line = fr.readline()
	shuffle(lines_i)
	for i in range(num_a):
		fw.write(lines_i[i])
fr.close()
fw.close()


################ LIBSVM ################

# get f-score of each set and average out to get final f-score

# prediction_file = 'output.txt'


# y_true = []
# i = 0
# with open(labels_file, 'r') as fr:
# 	line = fr.readline()
# 	print(type(line))
# 	while line:
# 		line = line.split(" ")
# 		if len(line)!=0:
# 			y_true.append(int(line[0]))
# 			# if (i%1000)==0:
# 			# 	print(f'Done-- labels: {i}')
# 			i+=1
# 		line = fr.readline()
# fr.close()

# y_pred = []
# i=0
# with open(prediction_file, 'r') as fr_p:
# 	line = fr_p.readline()
# 	while line:
# 		line = line.split(" ")
# 		if len(line)!=0:
# 			y_pred.append(int(line[0]))
# 			# if (i%1000)==0:
# 			# 	print(f'Done-- preds: {i}')
# 			i+=1
# 		line = fr_p.readline()
# fr.close()

# print(y_pred)

# f1_score = f1_score(y_true, y_pred)
# p_r_f1 = precision_recall_fscore_support(y_true, y_pred)
# # f_beta = fbeta_score(y_true, y_pred)

# ############## UndefinedMetricWarning: Some labels in Y-true never appear in Y-pred ################

# print(f'\n\nF1 Score={f1_score} \nPrecision-Recall F1 score={p_r_f1}')# ---- F-Beta Score={f_beta}')


