
# coding: utf-8

# # Movie Analaysis 
# 
# This is a dataset of the movies and their budget,revenue,gender,rating and reviwes from the imdb. From the given dataset i would like to ask some questions, so that it would be helpful in connecting people with their type of movie, so that the movie business can be imporved.
# 
# ## QUESTIONS
# * Highest and lowerst Number of movies released in which year ?
# * Which genre movie has the Highest voting average ?
# * Which genre movies getting the Highest revenue ?
# * Which genre movies mostly liked by the people ?
# * Does the popularity of the movies depends on the runtime of the movie?
# * Does the movie with higher budget yields high revenue?
# * How many number of movies have been release each year in each genre?
# * Which heros has made the most contribution in movies in terms of revenue?
# * Which director has made the most contribution in movies in terms of revenue?

# In[88]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 
import itertools
get_ipython().magic('matplotlib inline')
movies= pd.read_csv("tmdb-movies.csv")
movies.head(2)


# # Assessing & Cleaning the Data

# In[89]:


movies.shape


# In[90]:


movies.info()


# In[91]:


#Removing the column which are not required for analysis
movies.drop(['tagline','keywords','overview','budget_adj','revenue_adj'],axis=1, inplace=True) 
movies.head(2)


# In[92]:


#converting the column with interger or float from string object datatype to float
movies.runtime = pd.to_numeric(movies.runtime,errors= 'coerce')
movies.vote_count = pd.to_numeric(movies.vote_count,errors='coerce')
movies.vote_average = pd.to_numeric(movies.vote_average,errors='coerce')
movies.budget = movies.budget.astype(float)
movies.revenue = movies.revenue.astype(float)


# In[93]:


#creating gener and lead_role column for analysis & replaceing the genres string values seperated with comma.
movies['genre'] = movies.genres.str.split('|',expand= True)[0]
movies['lead_role'] = movies.cast.str.split('|',expand=True)[0]
movies['genres'] = movies['genres'].str.replace('|',',')
movies.head(2)


# In[94]:


#To remove the duplicates
movies.drop_duplicates(inplace=True)


# In[95]:


#convert all the budget and revenue amount in Billion Dollar Amount
movies.budget = movies.budget/1000000000 
movies.revenue = movies.revenue/1000000000 
movies.head(4)


# In[96]:


#Renaming the buget and revenue column in billions
movies = movies.rename(columns={'budget':'budget_in_billion','revenue':'revenue_in_billion'})


# In[97]:


#filtering the release_year and genre to required length for better analysis
movies.release_year = movies.release_year.astype(str)
movies = movies[movies['release_year'].str.len() == 4]
movies = movies[movies['genre'].str.len() <= 15]
movies.release_year = movies.release_year.astype(int)


# # Explorations Phase

# In[98]:


#Release years and count from the data
print("Total Number of Release Years:", movies.release_year.nunique())
print("Release Years:", movies.release_year.unique())


# In[99]:


# Basic analysis from the Data
print ("Total number of movies:",movies.original_title.nunique())
print ("Total number of Geners:",movies.genre.nunique())
print ("Different Geners:",movies['genre'].unique())
print ("Total number of directors:",movies['director'].nunique())


# In[100]:


#to display the statistical values of all numerical data's
movies.describe()


# In[101]:


#Number of release in each year
plt.figure(figsize=(25,20))
sns.countplot(x='release_year',data=movies)
plt.show()


# In[38]:


#comparision graph between the genre & vote_average
plt.figure(figsize = (25,10))
sns.barplot(x='genre',y='vote_average',data = movies)
plt.show()


# In[39]:


#comparision between the genre and popularity
plt.figure(figsize=(25,10))
sns.barplot(x='genre',y='popularity',data=movies)
plt.show()


# In[40]:


#comparision between different genres and their budget
plt.figure(figsize=(25,10))
sns.barplot(x='genre',y='budget_in_billion',data=movies)
plt.show()


# In[41]:


#comparision between the different genres and their revenue
plt.figure(figsize=(25,10))
sns.barplot(x='genre',y='revenue_in_billion',data=movies)
plt.show()


# In[42]:


#scatter polt to analyse whether the popularity based on the movie runtime 
plt.figure(figsize=(20,10))
sns.lmplot(x='runtime',y='popularity',data= movies,fit_reg = True)
plt.show();


# In[43]:


#scatter plot to analyse whether revenue of a movie based on the budget  
plt.figure(figsize=(20,10))
sns.lmplot(x='budget_in_billion',y='revenue_in_billion',data= movies,fit_reg=True)
plt.show();


# In[44]:


#Dataframe on the mean popularity for each genre from highest to lowest
movies.groupby('genre',as_index=False)['popularity'].mean().sort_values('popularity',ascending = False)


# In[45]:


#DataFrame on the mean voting avergare for each genre from highest to the lowest
movies.groupby('genre',as_index=False)['vote_average'].mean().sort_values('vote_average',ascending = False)


# In[46]:


#List of all unique Genre of movies
unique_genres = movies['genres'].unique()
individual_genres = []
for genre in unique_genres:
    individual_genres.append(genre.split(','))
individual_genres = list(itertools.chain.from_iterable(individual_genres))
individual_genres = set(individual_genres)

individual_genres


# In[47]:


#Total number of movies on each genre
#A detailed analysis on total movie release in each year for each genre
print ( "Number of movies in each genre \n")
for genre in individual_genres:
    seperate_genre = movies['genres'].str.contains(genre).fillna(False)
    plt.figure(figsize=(15,10))
    plt.xlabel('Year')
    plt.ylabel('Number of Movies Made')
    plt.title(str(genre))
    movies[seperate_genre].release_year.value_counts().sort_index().plot(kind='bar',color ='b',alpha=0.5,rot=45)
    print(genre, len(movies[seperate_genre]))


# In[48]:


# Percentage of movies released on each genre 
genre_percent = np.zeros(len(individual_genres))
i =0
for genre in individual_genres:
    current_genre = movies['genres'].str.contains(genre).fillna(False)
    percent = len(movies[current_genre])/10842 * 100
    genre_percent[i] = percent
    i += 1
    print (genre, percent)


# In[49]:


#DataFrame for clear visualization and to make Analysis on them
genre_df = pd.DataFrame(genre_percent,index = individual_genres,columns=['percentage'])
genre_df['percentage'] = genre_df['percentage'].round(2)
genre_df 


# In[50]:


#Pie chart analysis on the top 5 genres based on the total number of movies
explode = (0.05, 0.05, 0.08, 0.1, 0.12)
colors = ['#ff3232', '#ff4c4c', '#ff6666', '#ff7f7f', '#ff9999' ]
genre_df.sort_values(by='percentage', ascending=False).head(5).plot.pie(legend=False, subplots=True, autopct='%.2f%%', figsize=(8,8), explode=explode, colors=colors)
plt.ylabel('')
plt.title('Percent of Total Movies Made from Top 5 Genres', weight='bold', fontsize=16)


# In[51]:


#Total Revenue obtained by each genre
genre_revenue_percent = np.zeros(len(individual_genres))
i = 0
for genre in individual_genres:
    current_genre = movies['genres'].str.contains(genre).fillna(False)
    revenue_percent = movies[current_genre].revenue_in_billion.sum()/movies['revenue_in_billion'].sum() * 100
    genre_revenue_percent[i] = revenue_percent
    i += 1
    print (genre,revenue_percent)


# In[52]:


#Same as before made a DataFrame for clear visualization and to make Analysis on them
genre_revenue_df = pd.DataFrame(genre_revenue_percent, index = individual_genres,columns=['percentage'])
genre_revenue_df 


# In[53]:


#Pie chart analysis on the top 5 genres based on the revenue
explode = (0.05, 0.05, 0.08, 0.1, 0.12)
colors = ['#ff3232', '#ff4c4c', '#ff6666', '#ff7f7f', '#ff9999' ]
genre_revenue_df.sort_values(by='percentage',ascending=False).head(5).plot.pie(legend=False, subplots=True, autopct='%.2f%%', figsize=(8,8), explode=explode,colors = colors)
plt.ylabel('')
plt.title('Percent of Total Revenue Made from Top 5 Genres', weight='bold', fontsize=16)


# In[54]:


# Obtaining the first 10 directors based on the numbe of movies directed
most_active_director = movies.director.value_counts().head(10)
most_active_directors = most_active_director.index
most_active_directors


# In[76]:


# Obtaining the Revenues given by these top 10 directors in Billions
director_revenue_total = np.zeros(len(most_active_directors))
i =0 
for dirct in most_active_directors:
    current_director = movies['director'].str.contains(dirct).fillna(False)
    director_revenue = movies[current_director].revenue_in_billion.sum()
    director_revenue_total[i] = director_revenue
    i += 1
    print (dirct,director_revenue)


# In[77]:


#DataFrame for the clear Visualization and Analysis
dirct_revenue_df = pd.DataFrame(director_revenue_total,index = most_active_directors,columns=['Revenue'])
dirct_revenue_df


# In[79]:


#pie chart analysis on the directors with highest to the lowest
explode = np.linspace(0,0.4, 10)
colors = ['#ff3232', '#ff4c4c', '#ff6666', '#ff7f7f', '#ff9999' ]
dirct_revenue_df.sort_values(by='Revenue',ascending=False).plot.pie(legend=False, subplots=True, autopct='%.2f%%', figsize=(8,8), explode=explode,colors = colors)
plt.ylabel('')
plt.title('Revenue Contribution Made by Top 10 Directos', weight='bold', fontsize=16)


# In[68]:


# creating a index of top 10 lead_role who has done most films
most_active_hero = movies['lead_role'].value_counts().sort_values(ascending=False).head(10)
most_active_heros = most_active_hero.index


# In[83]:


# calcuating the revenue made by the top the lead roles
hero_total_revenue = np.zeros(len(most_active_heros))
i = 0 
for hero in most_active_heros:
    current_hero = movies['lead_role'].str.contains(hero).fillna(False)
    revenue_hero = movies[current_hero].revenue_in_billion.sum()
    hero_total_revenue[i] = revenue_hero 
    i += 1
    print (hero,revenue_hero)    


# In[85]:


# Creating DataFrame for a clear view and analysis 
hero_revenue_df = pd.DataFrame(hero_total_revenue, index = most_active_heros, columns=['Revenue'])
hero_revenue_df


# In[87]:


#pie chart analysis on the heros contribution in revenue from highest to the lowest
explode = np.linspace(0,0.4, 10)
colors = ['#ff3232', '#ff4c4c', '#ff6666', '#ff7f7f', '#ff9999' ]
hero_revenue_df.sort_values(by='Revenue',ascending=False).plot.pie(legend=False, subplots=True, autopct='%.2f%%', figsize=(8,8), explode=explode,colors = colors)
plt.ylabel('')
plt.title('Revenue Contribution Made by Top 10 Hero"s', weight='bold', fontsize=16)


# # Conclusion Phase 
# 
# ## Answers to the question from the analysis made in the exploration phase
# 
# * **Highest and lowerst Number of movies released in which year ?**
#  - The highest number of movie was released in 2014 which was 969 movies and the lowest movies was released on 1961    with only 31 movies
#  
# * **Which genre movie has the Highest voting average ?**
#  - As per the voting average the documentary films have got the highest voting average of 7 out of 10.
#  
# * **Which genre movies getting the Highest revenue ?**
#  - Adventure movies always tops the order on the total revenes obtained and it's average comes up to 120 million  
#  
# * **Which genre movies mostly liked by the people ?**
#  - Aventure movies are the most attracting genre for the people. 
#  
# * **Does the popularity of the movies depends on the runtime of the movie?**
#  - Yes, it does depends on the runtime of the movies,movies with the duration between 150 to 200 Miuntes has the      highest popularity, Where as a movie popularity get's reduced as the duration goes high.
#  
# * **Does the movie with higher budget yields high revenue?**
#  - Yes, higher the budget of the film, higher is the revenue yeild by the movie production company.
#  
# * **Which Hero has made the most contribution in movies in terms of revenue?**
#  - Tom hanks and Johnny Depp has given the highest revenues with the revenue of 7.7 Billion Doller by Tom Hanks and 6.41 Doller by Johnny Depp.
#  
# * **Which Director has made the most contribution in movies in terms of revenue?**
#  - Steven Spielberg	has made the higest revenue of 9.2 Billion Doller followe by Tim Burton with 3.8 Billion Doller
# 

# ## Finialized Conclusion on the Analysis
# 
# ### From all the analysis made on the Movies and their Genre , conclusion hits on two basics for movie Making,
# 
# * **Business Prespective**
# * **Awards Prespective**
# 
# * **Business Prespective:**
#   -  Based on the Business Prespective, movies can gain more revenues based on the follwing Charateristics
#     - Budget
#     - Genre
#     - Lead Role (said to be as hero)
#     - Runtime <br>
#     So from the given data basd on the business prespective movies with high budget, genre like Adventure,science Fiction,Action and Fantasy, based on the lead role and the run time a movie can make a great business in return for the investment. <br>
# * **Awards Prespective:**
#   - Awards Prespective movis have the following charateristics 
#    - Genre 
#    - Runtime 
#    - Budget <br>
#    So from the award Prespective movies mostly depends on the genres like documentary, History, Animation, Fantasy and Music because they have the higest voting average, then comes the runtime of the movie which should not drag, at last comes the budget, where awards to a movie can only from the voting rate and these voting rate solely depends on the genre of movie.
#    
# ###  Final communicative conclusion has been made from the analysis for the movies of different genre from the year 1961 to 2015 
