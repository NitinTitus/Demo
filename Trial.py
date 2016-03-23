from nltk.classify import NaiveBayesClassifier
import re
import pickle

pos_comments = []
neg_comments = []

def word_feats(words):
    return dict([(words, True)])

for f in open('new.txt'):
    f=re.sub('\n', '', f)
    if f.split(' ')[0]=='+':
        pos_comments.append(f.split(' ', 1)[1])
    else:
        neg_comments.append(f.split(' ', 1)[1])

pos_features = [(word_feats(f) ,'+') for f in pos_comments]
neg_features = [(word_feats(f) ,'-') for f in neg_comments]
print(pos_features)
print(neg_features)

train_features = pos_features + neg_features

classifier = NaiveBayesClassifier.train(train_features)

print (classifier.classify(word_feats('Camera is really good. Nice phone. Bad screen though')))

f=open('model.pickle','wb')
pickle.dump(classifier,f)
f.close()