import re

def func():
    f1=open('new.txt','w')
    stopwords=[]
    vocabulary=[]
    for i in open('stopwords.txt'):
        i=re.sub('\n', '', i)
        stopwords.append(i.lower())
    for f in open('data.txt'):
        f=re.sub('[^A-Za-z\s\+\-\']+',' ',f)
        f=re.sub('\'','',f)
        f=re.sub('\s+', ' ', f)
        words=f.split(' ')
        for i in words:
            i=i.lower()
            if i not in stopwords:

                f1.write(i + ' ')
                vocabulary.append(i)
        f1.write('\n')
    sorted_set=sorted(set(vocabulary))
    f2=open('vocabulary.txt','w')
    for i in sorted_set:
        if(vocabulary.count(i)>=2 and len(i)>1):
                f2.write(i  + '\n')

func()



