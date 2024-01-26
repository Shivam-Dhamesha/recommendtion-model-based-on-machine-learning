#Waring igonre
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#Data PrePreocessing fxns
import ast
def objToList(obj):
    l=[]
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l

def castThree(obj):
    l=[]
    count=0
    for i in ast.literal_eval(obj):
        if count!=3:
            l.append(i['name'])
            count+=1
        else:
            break
    return l

def getD(obj):
    l=[]
    count=0
    for i in ast.literal_eval(obj):
        if i['job']=="Director":
            l.append(i['name'])
            break
    return l

def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


#Modules
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
from sklearn.metrics.pairwise import cosine_similarity


#URLs
url_movies = "data_m.csv"
url_credits= "data_c.csv"

movies=pd.read_csv(url_movies)
credits=pd.read_csv(url_credits)

#MAIN 


#Data PreProcessing

movies=movies.merge(credits,on='title')
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.dropna(inplace=True)
movies['genres']=movies['genres'].apply(objToList)
movies['keywords']=movies['keywords'].apply(objToList)
movies['cast']=movies['cast'].apply(castThree)
movies['crew']=movies['crew'].apply(getD)
movies['overview']=movies['overview'].apply(lambda x:x.split())
movies['genres']=movies['genres'].apply(lambda x: [i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x: [i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x: [i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x: [i.replace(" ","") for i in x])

# New Col named tags
movies['tags']=movies['overview']+movies['keywords']+movies['cast']+movies['crew']
movies['tags']=movies['tags'].apply(lambda x:" ".join(x))
movies['tags']=movies['tags'].apply(lambda x:x.lower())
#Processed Data
data=movies[['movie_id','title','tags']]
data['tags']=data['tags'].apply(stem)

#Form SKLEARN 

cv=CountVectorizer(max_features=5000,stop_words='english')
vect=cv.fit_transform(data['tags']).toarray()

sim=cosine_similarity(vect)

#MAIN 2.0

print(sim)

# movies_index = data[data['title']=="batman"].index[0]
# distance=sim[movies_index]
# movies_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
# for i in movies_list:
#     print(data.iloc[i[0]].title)

def recom(movie):
    movies_index = data[data['title']==movie].index[0]
    distance=sim[movies_index]
    movies_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movies_list:
        print(data.iloc[i[0]].title)

recom("Iron Man")





