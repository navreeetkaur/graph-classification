# Graph Classification

This repository containes the following as part of Homework-3 of the Data Mining Course(COL761) at IIT Delhi.

1. Comparison of Frequent Subgraph Mining tools. The dataset of molecules tested against AIDS is used whose format is the following:
- #graphID
- number of nodes
- Series of Node Labels
- Number of edges
- Series of “Source node, Destination Node, Edge label”

gSpan, FSG (also known as PAFI), and Gaston are run against frequency threshold in the AIDS dataset at minSup = 5%, 10%, 25%, 50% and 95%.
Running times of each are plotted and the trend observed in the running times is explained.

2. Considering the same AIDS graph dataset, labels(active and inactive molecules against HIV virus) for a subgraph are provided in another dataset. 
A technique is designed to classify graphs by converting each graph into a binary feature vector where each dimension corresponds
to presence or absence of corresponding subgraph. Only the 'deterministic' frequent subgraphs are used. Graphs are then classfied
in the feature space using the linear kernel of LIBSVM. While traiing, it is also ensured that the training examples of active
and inactive moleclues is equal.


- ```sh compile.sh``` compiles all the source files.
- ```sh classify.sh <trainset filename containing graphs> <active graph IDs filename> <inactive graph IDs filename> <testset filename containing graphs>```
outputs two files train.txt and test.txt.  In train.txt, the ith line contains the class label of graph i followed by the feature vector representation 
of the ith graph in the trainset. The label of an active graph is “1” and an inactive graph is “-1”. Each line is of the following format:

```
<label> <index1>:<value1> <index2>:<value2> ...
.
. 
.
```

The test.txt file is of the same format as above, with the only exception being that the class label is not included. 
That is, it should be of the form
```
<index1>:<value1> <index2>:<value2> ...
. 
.
.
```

If test set contains 100 graphs, test.txt also contains 100 lines (same for train.txt as well). 

- ```install.sh``` clones in the current directory followed by executing bash commands to install all modules/dependencies/libraries
