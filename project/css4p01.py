# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 14:33:14 2024

@author: bekeu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

movies = pd.read_csv("movie_dataset.csv",index_col = "Rank")
print(movies.info())
print("\n")
print(movies.describe())
print("\n")

score_ave = movies["Metascore"].mean()
movies["Metascore"].fillna(score_ave,inplace = True)

revenue_ave = movies["Revenue (Millions)"].mean()
movies["Revenue (Millions)"].fillna(revenue_ave,inplace = True)
print(movies.info())
print("\n")

#Question 1, highest rated movie.
print(movies.loc[movies["Rating"] == movies["Rating"].max()]["Title"])
print("The highest rated movie is "+str(movies.loc[55,"Title"])+"\n")

#Question 2, average revenue
print("The average revenue of all movies is "+str(movies["Revenue (Millions)"].mean().round(decimals=2))+" million\n")

#Question 3, average revenue between 2015 and 2017
period_revenue = movies.loc[(2014 < movies["Year"])&(2018 > movies["Year"])]["Revenue (Millions)"].mean()
print("The average revenue of movies from 2015 to 2017 is "+str(period_revenue.round(decimals=2))+" million\n")

#Question 4, movie count in 2016
print("In 2016 there were "+str(len(movies.loc[movies["Year"] == 2016]))+" movies released\n")

#Question 5, movie count in directed by Christopher Nolan
print("Christopher Nolan directed "+str(len(movies.loc[movies["Director"] == "Christopher Nolan"]))+" movies\n")

#Question 6, movie count with greater than 8.0 rating
print(str(len(movies.loc[movies["Rating"] >= 8.0]))+" movies have a rating of at least 8.0\n")

#Question 7, average rating of movies directed by Christopher Nolan
print("Christopher Nolan directed movies have an average rating of "+str(movies.loc[movies["Director"] == "Christopher Nolan"]["Rating"].mean().round(decimals=2))+"\n")

#Question 8, year of the highest average rating
max_year = 2000
rating = 0
for x in range(10):    
    y = movies.loc[movies["Year"] == 2006+x]["Rating"].mean()
    if y > rating:
        max_year = 2006+x
        rating = y

print("The year with the highest average rating is "+str(max_year)+"\n")

#Question 9, percentage increase in movies made between 2006 and 2016?
#already have 2016 movie count of 297
print("In 2006 there were "+str(len(movies.loc[movies["Year"] == 2006]))+" movies released\n")

up = len(movies.loc[movies["Year"] == 2016])
down = len(movies.loc[movies["Year"] == 2006])
print("Thus, we have a "+str((up-down)/down*100)+"% increase in the number of movies over 10 years (according to the database)\n")

#Question 10, most common actor count
actor_list = []
counter_list = []
for x in range(len(movies["Actors"])):
    y = movies.loc[x+1,"Actors"].replace(", ",",").split(",")
    for c in range(len(y)):
        if actor_list.count(y[c])==0:
            actor_list.append(y[c])
        counter_list.append(y[c])

count = []
for x in range(len(actor_list)):
    y = counter_list.count(actor_list[x])
    count.append(y)
    
actors = pd.DataFrame(
    {"Actor" : actor_list,
     "Count" : count
     })


print(actors.loc[actors["Count"] == actors["Count"].max()]["Actor"])
print("The most common actor is "+str(actors.loc[238,"Actor"])+", appearing in "+str(actors["Count"].max())+" movies\n")

#Question 11, number of unique genres
genre_list = []
counter_list = []
for x in range(len(movies["Genre"])):    
    y = movies.loc[x+1,"Genre"].split(",")
    for c in range(len(y)):
        if genre_list.count(y[c])==0:
            genre_list.append(y[c])
        counter_list.append(y[c])
            
count2 = []
for x in range(len(genre_list)):
    y = counter_list.count(genre_list[x])
    count2.append(y)
    
genres = pd.DataFrame(
    {"Genre" : genre_list,
     "Count" : count2
     })

print("The number of unique genres is "+str(len(genre_list))+"\n")

#Question 12?
"""
I need a plot or something.
I also need to rearrange the dataframe to get correct correlations
Here's an idea. Convert all string data into numerical data somehow.
So, a director score, an actor score, and a genre score, all
correlated to rating, metascore, and revenue somehow.
"""

director_list = []
counter_list = []
for x in movies["Director"]:
    if director_list.count(x)==0:
        director_list.append(x)
    counter_list.append(x)
    
count3 = []
for x in range(len(director_list)):
    y = counter_list.count(director_list[x])
    count3.append(y)
    
directors = pd.DataFrame(
    {"Director" : director_list,
     "Count" : count3
     })

"""
I now have dataframes with counts for directors, actors, and genres.
Add all of that into the movies dataframe with the correct dimensions.
"""

actor_score = []
for x in movies["Actors"]:
    y = x.replace(", ",",").split(",")
    m=0
    for c in range(len(y)):
        m+=int(actors.loc[actors["Actor"]==y[c]]["Count"])
    actor_score.append(m)
    
director_score = []
for x in movies["Director"]:
    m=0
    m+=int(directors.loc[directors["Director"]==x]["Count"])
    director_score.append(m)

genre_score = []
for x in movies["Genre"]:
    y = x.split(",")
    m=0
    for c in range(len(y)):
        m+=int(genres.loc[genres["Genre"]==y[c]]["Count"])
    genre_score.append(m)
    
movies["Genre Score"] = genre_score

movies["Director Score"] = director_score

movies["Actor Score"] = actor_score

sns.pairplot(movies)
plt.savefig("pairplot.png")
plt.figure(figsize=(20,14))
sns.heatmap(movies.corr(numeric_only=True),annot=True,linewidths=3)
plt.savefig("heatmap.png")
