# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:53:50 2017

@author: Abhijeet Singh
diedit dan disesuaikan ulang oleh:
Ikhwanul Muslimin, 15 Dzulhijjah 1438/5 September 2017
untuk keperluan tugas NLP
WARN: Hapus content file training_matrix.arff dan test_matrix.arff sebelum run program
"""
from __future__ import print_function
import os
import numpy as np
np.set_printoptions(threshold=np.nan)
from collections import Counter
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.svm import LinearSVC
# from sklearn.metrics import confusion_matrix

numberWordinDict = 3000
train_dir = 'train-mails'
test_dir = 'test_mails'

def make_Dictionary(train_dir):
    emails = [os.path.join(train_dir,f) for f in os.listdir(train_dir)]   
    all_words = []      
    for mail in emails:    
        with open(mail) as m:
            for i,line in enumerate(m):
                if i == 2:
                    words = line.split()
                    all_words += words
    
    dictionary = Counter(all_words)
    
    list_to_remove = dictionary.keys()
    for item in list_to_remove:
        if item.isalpha() == False: 
            del dictionary[item]
        elif len(item) == 1:
            del dictionary[item]
    dictionary = dictionary.most_common(numberWordinDict)
    return dictionary
    
def extract_features(mail_dir): 
    files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files),numberWordinDict))
    docID = 0;
    for fil in files:
      with open(fil) as fi:
        for i,line in enumerate(fi):
          if i == 2:
            words = line.split()
            for word in words:
              wordID = 0
              for i,d in enumerate(dictionary):
                if d[0] == word:
                    wordID = i
                    features_matrix[docID,wordID] = words.count(word)
        docID = docID + 1     
    return features_matrix

def getAllFilename(mail_dir):
    emails = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)] 
    for i,mail in enumerate(emails):
        emails[i] = os.path.splitext(os.path.basename(mail))[0]

    return emails

# Create a dictionary of words with its frequency and extract feature

dictionary = make_Dictionary(train_dir)
train_matrix = extract_features(train_dir)
test_matrix = extract_features(test_dir)

# Start make format arff
#for train data
filetraining=open('./training_matrix.arff', 'a') #open file to save
print("% 1. Title: Spam Dataset training\n%\n% 2. Sources: Hasil Feature Matrix\n%\n@RELATION spam", end="\n", file=filetraining)
for i,d in enumerate(dictionary):
    if d[0] == "class":
        print("@ATTRIBUTE class_ NUMERIC", end="\n", file=filetraining)
    else:
        print("@ATTRIBUTE "+d[0]+" NUMERIC", end="\n", file=filetraining)

print("@ATTRIBUTE class {spam, not-spam}", end="\n", file=filetraining)

#for test data
filetest=open('./test_matrix.arff', 'a') #open file to save
print("% 1. Title: Spam Dataset test\n%\n% 2. Sources: Hasil Feature Matrix\n%\n@RELATION spam", end="\n", file=filetest)
for i,d in enumerate(dictionary):
    if d[0] == "class":
        print("@ATTRIBUTE class_ NUMERIC", end="\n", file=filetest)
    else:
        print("@ATTRIBUTE "+d[0]+" NUMERIC", end="\n", file=filetest)

print("@ATTRIBUTE class {spam, not-spam}", end="\n", file=filetest)

# Prepare feature vectors per training/test mail and its labels

filename_list = getAllFilename(train_dir)
print("@DATA", end="\n", file=filetraining)
for i, d in enumerate(train_matrix):
    for j, n in enumerate(d):
        print(str(n)+",", end="", file=filetraining)
    if filename_list[i][:1] == 's':
        print("spam", end="\n", file=filetraining)
    else:
        print("not-spam", end="\n", file=filetraining)

filename_list = getAllFilename(test_dir)
print("@DATA", end="\n", file=filetest)
for i, d in enumerate(test_matrix):
    for j, n in enumerate(d):
        print(str(n)+",", end="", file=filetest)
    if filename_list[i][:1] == 's':
        print("spam", end="\n", file=filetest)
    else:
        print("not-spam", end="\n", file=filetest)