import sys
import numpy as np 
import subprocess
from random import shuffle
from sklearn.metrics import f1_score, precision_recall_fscore_support, fbeta_score
import sys

################ change the training input to include equal active and inactive molecules ######################
# train_file = 'train.txt'
train_file = sys.argv[1]
new_train_file = 'new_train.txt'
# test_file = 'new_test.txt'
test_file = sys.argv[2]

# Randomly pick a set of inactive instances with size equal to number of total active instances in training set
# Generate new training and testing file

lines_i = []

num_a = 0
num_i = 0
with open(train_file, 'r') as fr, open(new_train_file, 'w') as fw:
	full_line = fr.readline()
	while full_line:
		line = full_line.split(" ")
		if len(line)!=0:
			label = int(line[0])
			if label==-1:
				num_i +=1
				lines_i.append(full_line)
			else:
				num_a +=1
				fw.write(full_line)
		full_line = fr.readline()
	shuffle(lines_i)
	for i in range(num_a):
		fw.write(lines_i[i])
fw.close()
fr.close()

################ LIBSVM ################

# get f-score of each set and average out to get final f-score
# test_file = new_train_file

prediction_file = 'output.txt'
str1 = "./libsvm-3.23/svm-train "+ new_train_file
str2 = "./libsvm-3.23/svm-predict "+test_file+ " " + new_train_file+ ".model " +prediction_file
subprocess.run(str1, shell=True, check=True)
subprocess.run(str2, shell=True, check=True)


y_true = []
i = 0
with open(test_file, 'r') as fr:
	line = fr.readline()
	while line:
		line = line.split(" ")
		if len(line)!=0:
			y_true.append(int(line[0]))
			i+=1
		line = fr.readline()
fr.close()

y_pred = []
i=0
with open(prediction_file, 'r') as fr_p:
	line = fr_p.readline()
	while line:
		line = line.split(" ")
		if len(line)!=0:
			y_pred.append(int(line[0]))
			i+=1
		line = fr_p.readline()
fr.close()

# print(y_pred)

f1_score = f1_score(y_true, y_pred)
p_r_f1 = precision_recall_fscore_support(y_true, y_pred)
# f_beta = fbeta_score(y_true, y_pred)

############## UndefinedMetricWarning: Some labels in Y-true never appear in Y-pred ################

print(f'\n\nF1 Score={f1_score} \nPrecision-Recall F1 score={p_r_f1}')# ---- F-Beta Score={f_beta}')


