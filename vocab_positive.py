import re
import math
import pickle

def vocab(list,text,char):
    vocabulary=[]
    count=0
    for f in list:
         if f.split(' ')[0]==char:
             words=f.split(' ')
             for i in words:
                 vocabulary.append(i)
         count+=1
    sorted_set=sorted(set(vocabulary))
    f1=open(text,'w')
    for i in sorted_set:
        if(len(i)>1 and vocabulary.count(i)>=2):
            f1.write(i + ' ' + str(vocabulary.count(i)) + '\n')

def find_total_count(text):
    total_frequency=0
    for f in open(text):
        f=re.sub('\n', '', f)
        word,frequency= f.split(' ')
        total_frequency+=int(frequency)
    return total_frequency

def vocab_size():
    count=0
    for f in open('vocabulary.txt'):
        count+=1
    return count

def file_size():
    count=0
    for f in open('new.txt'):
        count+=1
    return count

def create_probability_distribution(text,tot_count,pickle_text):
    dict={}
    total=0
    v = vocab_size()
    for f in open('vocabulary.txt'):
        f=re.sub('\n', '', f)
        dict[f]=1
    for f in open(text):
        f=re.sub('\n', '', f)
        word,frequency=f.split(' ')
        dict[word]+=int(frequency)
    for i in dict:
        dict[i]=float(dict[i])/float(tot_count + v)
        total+=dict[i]
    pickle.dump(dict,pickle_text)

def prior_probability(training_set):
    positive=negative=0
    for f in training_set:
        if f.split(' ')[0]=='+':
            positive+=1
        else:
            negative+=1
    return positive,negative

def test(training_set,test_set):
    vocab=[]
    positive_dict = pickle.load(open('positive.pickle'))
    negative_dict = pickle.load(open('negative.pickle'))
    correct=tp=tn=fp=fn=0
    positive_prior,negative_prior=prior_probability(training_set)
    for f in open('vocabulary.txt'):
        f=re.sub('\n', '', f)
        vocab.append(f)
    for f in test_set:
        words=f.split(' ')
        sentiment = f.split(' ')[0]
        positive_probability=0
        negative_probability=0
        for i in words:
            if i in vocab:
                positive_probability+=math.log(positive_dict[i])
                negative_probability+=math.log(negative_dict[i])
        positive_probability+=math.log(positive_prior)
        negative_probability+=math.log(negative_prior)
        if(positive_probability>negative_probability):
            if(f.split(' ')[0]=='+'):
                correct+=1
                tp+=1
            else:
                fp+=1
        else:
            if f.split(' ')[0] == '-':
                correct += 1
                tn+=1
            else:
                fn+=1
    return correct,tp,tn,fp,fn

def cross_validation():
    list=[]
    tot_accuracy=0
    fold_size=file_size()/10
    for f in open('new.txt'):
        f=re.sub('\n', '', f)
        list.append(f)
    for i in range(9,-1,-1):
        test_set=list[i*fold_size:][:fold_size]
        training_set=list[0:i*fold_size] + list[(i+1) * fold_size:]
        vocab(training_set,'vocabulary_positive.txt','+')
        vocab(training_set,'vocabulary_negative.txt','-')
        total_positive_count = find_total_count('vocabulary_positive.txt')
        total_negative_count = find_total_count('vocabulary_negative.txt')
        create_probability_distribution('vocabulary_positive.txt' ,total_positive_count, open('positive.pickle','w'))
        create_probability_distribution('vocabulary_negative.txt' ,total_negative_count,open('negative.pickle','w'))
        correct,tp,tn,fp,fn=test(training_set,test_set)
        print (correct)
        accuracy = float(tp+tn)/float(tp+tn+fp+fn)
        tot_accuracy+=accuracy
    print (tot_accuracy)

cross_validation()


