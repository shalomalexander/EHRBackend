# def train():
import pandas as pd
import numpy as np
import os
import sys
from sklearn.ensemble import RandomForestClassifier

print(os.path.join(os.path.abspath("DiseasePrediction2/testing.csv")))
df = pd.read_csv(os.path.join(os.path.abspath("DiseasePrediction2/training.csv"))) #Use for local system
#df = pd.read_csv("/var/www/sites/mysite/backend/DiseasePrediction2/training.csv") #Use for Pythonanywhere

X = df.iloc[:,:-1]
y = df.iloc[:,-1]

clf = RandomForestClassifier(n_estimators=100)
clf = clf.fit(X,np.ravel(y))

df_test = pd.read_csv(os.path.join(os.path.abspath("DiseasePrediction2/testing.csv"))) #Use for local system
#df_test = pd.read_csv("/var/www/sites/mysite/backend/DiseasePrediction2/training.csv") #Use for PythonAnywhere
X_df_test = df_test.iloc[:,:-1]
y_df_test = df_test.iloc[:,-1]

y_pred = clf.predict(X_df_test)

    # cm = confusion_matrix(y_pred, y_df_test)
    # print(accuracy_score(y_df_test, y_pred))
    # print(accuracy_score(y_df_test, y_pred,normalize=False))

import collections
def predict(s1,s2,s3,s4,s5):
    print(os.path.join(os.path.abspath("DiseasePrediction2/testing.csv")))


    l1=[]
    for col in df.columns:
        l1.append(col)
    l1.pop()

    symptoms = [s1,s2,s3,s4,s5]
    sym = []
    for i in range(len(l1)):
        sym.append(0)
    # for i in range(5):
    #     s = input("Enter symptom :- " )
    #     for j in range(len(l1)):
    #         if l1[j] == s:
    #             sym[j] = 1

    for j in symptoms:
        for k in range(len(l1)):
            if l1[k] == j:
                sym[k] = 1

    predictions_all = np.array([tree.predict([sym]) for tree in clf.estimators_])
    predictions_all=predictions_all.tolist()

    myList=[]
    list1=[]
    for i in range(len(predictions_all)):
        for x in predictions_all[i]:
            myList.append(round(x))
    # print(myList)
    dictionary = collections.Counter(myList)
    # print(dictionary)
    for k in dictionary.keys():
        list1.append([k,dictionary[k]])
    # print(list1)
    list1 = sorted(list1,key=lambda x: x[1],reverse = True)
    disease = clf.classes_

    d_list = []
    for i in list1:
        print('\n',disease[i[0]])
        d_list.append(disease[i[0]])
    
    return d_list[:5] 

def main():
    #train()
    predict("loss_of_appetite","nausea","back_pain","abdominal_pain","")
        
if __name__ == "__main__":
    main()