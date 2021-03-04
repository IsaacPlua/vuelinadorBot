import pandas as pd

o=open('OUTPUT_NN.txt','r')
f=open('test.txt','r')
O=o.readlines()
F=f.readlines()
df=pd.DataFrame(columns=['text','class'])
for i,j in enumerate(O):
    classe=j.split('\t')[1]
    texto=F[i].split('\t')[2]
    df.loc[i,:]=[texto, classe]
print(df.head())
df.to_csv('df.csv')
