#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <string.h>
#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <bits/stdc++.h>

using namespace std;

int getQvalue(vector<int> a, vector<int> b, vector<int> indices)
{
    int count = 0;
    for (int i = 0; i < indices.size(); i++)
    {
        if (a[indices[i]] != b[indices[i]])
        {
            return 0;
        }
    }
    return (-1);
}

vector<int> feature_selection(vector<vector<int> > inactive_graphs, vector<vector<int> > active_graphs, vector<int> features_used, vector<int> total_features, float t)
{
    vector<int> final_features;
    int global_max = INT_MIN;

    for (; ;)
    {
        int index = -1;
        int a = global_max;
        for (int f = 0; f < total_features.size(); f++)
        {
            int total_qvalue = 0;
            if (features_used[f] != 1)
            {
                final_features.push_back(total_features[f]);
                features_used[f] = 1;
                for (int i = 0; i < active_graphs.size(); i++)
                {
                    vector<int> vec_1;
                    vec_1 = active_graphs[i];

                    for (int j = 0; j < inactive_graphs.size(); j++)
                    {
                        vector<int> vec_2;
                        vec_2 = inactive_graphs[j];
                        total_qvalue = total_qvalue + getQvalue(vec_1, vec_2, final_features);
                    }
                }
                //cout<<total_qvalue<<endl;
                if (total_qvalue - global_max > 0)
                {
                    global_max = total_qvalue;
                    index = total_features[f];
                    final_features.erase(final_features.end() - 1);
                    features_used[f] = 0;
                }
                else
                {
                    features_used[f] = 0;
                    final_features.erase(final_features.end() - 1);
                }
            }
        }
        //cout<<"max: "<<global_max<<endl;
        if (index != -1)
        {
            final_features.push_back(index);
            features_used[index] = 1;
        }
        else if (index == -1 || final_features.size() == total_features.size())
        {
            return final_features;
        }
    }
    return final_features;
}

vector< vector<int> > getGraphEncodings(vector<vector<int> > graphs, vector<int> final_features)
{
    vector< vector<int> > new_encoding(graphs.size());
    for (int i = 0; i < graphs.size(); i++)
    {
        for (int j = 0; j < final_features.size(); j++)
        {
            new_encoding[i].push_back(graphs[i][final_features[j]]); 
        }
    }
    return new_encoding;
}


int main()
{
    vector<vector<int> > active_graphs;
    vector<vector<int> > inactive_graphs;
    vector<int> id_active;
    vector<int> id_inactive;
                       
    ifstream file("a_encode.txt");
    
    srand(time(NULL));
    int no_features;
    int count = 0;

    while(!file.eof())
    {
        vector<int> row;
        string line;
        getline(file, line);

        int x;
        for(int l = 0; l < line.size(); l++){
            if (line[l] == ','){
                x = l;
                break;
            }
        }
        // if (count ==0){
        // cout <<"line: "<< line[0]<<line[1]<<endl;}
    
        if ( !file.good() )
            break;
        
        stringstream iss(line);
        no_features = (line.size()-x)/2;
        //cout<<no_features<<endl;

        int id = 0;
        for (int col = 0; col < no_features+1; ++col)
        {
            string val;
            getline(iss, val, ',');
            if (col == 0){
                id = atoi(val.c_str());
            }
            else{
                row.push_back(atoi(val.c_str()));
            }
        }

        active_graphs.push_back(row);
        id_active.push_back(id);
        //cout<<"id :"<<id<<endl;
        //count++;

        // if (count < 253){    
        //     active_graphs.push_back(row);
        // }
        // else if (count >= 253)
        // {
        //     inactive_graphs.push_back(row);
        // }
    }
    file.close();

    ifstream file1("i_encode.txt");

    while(!file1.eof())
    {
        vector<int> row;
        string line;
        getline(file1, line);
        // if (count == 0){
        // cout <<"line: "<< line <<endl;}
        int x;
        for(int l = 0; l < line.size(); l++){
            if (line[l] == ','){
                x = l;
                break;
            }
        }
        //cout<<"x:  "<<x;
        if ( !file1.good() )
            break;
        
        stringstream iss(line);
        no_features = (line.size()-x)/2;

        int id = 0;
        for (int col = 0; col < no_features+1; ++col)
        {
            string val;
            getline(iss, val, ',');
            if (col == 0){
                id = atoi(val.c_str());
            }
            else{
                row.push_back(atoi(val.c_str()));
            }
        }

        inactive_graphs.push_back(row);
        id_inactive.push_back(id);
    }

    // for (int i = 0; i < inactive_graphs.size(); i++){
    //     for (int j = 0; j < inactive_graphs[0].size(); j++){
    //         cout<<inactive_graphs[i][j]<<" ";
    //     }
    //     cout<<endl;
    // }

    // cout << inactive_graphs[0].size()<<endl;
    // cout << active_graphs[0].size()<<endl;

    // for (int i = 0; i< id_active.size(); i++){
    //     cout<<id_active[i]<<" ";
    // }

    // cout << "Yayyyy"<<endl;

    // for (int i = 0; i< id_inactive.size(); i++){
    //     cout<<id_inactive[i]<<" ";
    // }

    // cout << inactive_graphs.size()<<endl;
    float t = 0;
    if (no_features > 50 || active_graphs.size() > 250)
    {
        t = 0.1;
    }
    else{
        t = 0.05;
    }

    vector<int> total_features(no_features);
    for (int i = 0; i < no_features; i++){
        total_features[i] = i;
    }

    // cout<<no_features<<endl;

    vector<int> features_used(no_features);
    for (int i = 0; i < no_features; i++){
        features_used[i] = 0;
    }

    int size_active = active_graphs.size();
    int size_inactive = inactive_graphs.size();

    vector<vector<int> > features_10fold;
    int kfold = 8;

    for (int num = 0; num < kfold; num++)
    {
        vector<vector<int> > inactive_graphs_sub;
   
        for (int i = 0; i < size_active; i++)
        {
            inactive_graphs_sub.push_back(inactive_graphs[rand()%size_inactive]);
        }

        features_10fold.push_back(feature_selection(inactive_graphs_sub, active_graphs, features_used, total_features, t));
    }

    // //vector<int> final_f = feature_selection(inactive_graphs, active_graphs, features_used, total_features);
    
    // // for (int i = 0; i < features_10fold.size(); i++){
    // //     for (int j = 0; j < features_10fold[0].size(); j++){
    // //         cout<<features_10fold[i][j]<<" ";
    // //     }
    // //     cout<<endl;
    // // }

    set<int> final_set;

    for (int i = 0; i < features_10fold.size(); i++){
        for (int j = 0; j < features_10fold[0].size(); j++){
            final_set.insert(features_10fold[i][j]);
        }
    }

    vector<int> final_vector;

    auto itr = final_set.begin();
    for(;itr!=final_set.end();itr++)
    {
        final_vector.push_back(*itr);
    }

    for (int i = 0; i< final_vector.size(); i++){
        cout<<final_vector[i]<<" ";
    }
    

    vector<vector<int> > new_active = getGraphEncodings(active_graphs, final_vector);

    vector<vector<int> > new_inactive = getGraphEncodings(inactive_graphs, final_vector);


    // // for (int i = 0; i < new_inactive.size(); i++){
    // //     for (int j = 0; j < new_inactive[0].size(); j++){
    // //         cout<<new_inactive[i][j]<<" ";
    // //     }
    // //     cout<<endl;
    // // }

    int total = new_active.size() + new_inactive.size();
    vector<vector<int> > new_total(total);
    vector<int> labels(total);
    for (int i = 0; i < new_active.size(); i++){
        new_total[id_active[i]] = new_active[i];
        labels[id_active[i]] = 1;
    }
    for (int j = 0; j < new_inactive.size(); j++){
        new_total[id_inactive[j]] = new_inactive[j];
        labels[id_inactive[j]] = -1;
    }

    // // for (int i = 0; i < new_total.size(); i++){
    // //     for (int j = 0; j < new_total[0].size(); j++){
    // //         cout<<new_total[i][j]<<" ";
    // //     }
    // //     cout<<endl;
    // // }

    // // cout << labels.size()<<endl;
    // // cout << new_total.size() << endl;
    // // cout << new_total[0].size() << endl;

    ofstream myfile;
    myfile.open ("train_new.txt");
    for (int i = 0; i < total; i++)
    {
        myfile << labels[i]<<" ";
        for (int j = 0; j < final_vector.size(); j++)
        {
            myfile << j<<":"<<new_total[i][j]<<" ";
        }
        myfile << '\n';
    }

    myfile.close();

    ofstream myfile1;
    myfile1.open("cork_features_new.txt");
    for (int k = 0; k < final_vector.size(); k++)
    {
        myfile1 << final_vector[k] << " ";
    }
    myfile1.close();

}