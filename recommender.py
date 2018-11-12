from math import *
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_recommendations(title, cosine_sim, indices):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))


    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    print(sim_scores, "scores")

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:4]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return metadata['name'].iloc[movie_indices]



#metadata = pd.read_csv("movies.csv", low_memory=False)
metadata = pd.read_csv("centers3.csv", low_memory=False)

def create_soup(x):
    return ' '.join(x['a']) + ' ' + ' '.join(x['b']) + ' '  .join(x['c']) + ' ' + ' '.join(x['d']) + ' ' + ' '.join(x['e']) + ' ' + ' '.join(x['f']) + ' ' + ' '.join(x['g']) + ' ' + ' '.join(x['h']) + ' ' + ' '.join(x['i'])
    #return ' '.join(x['a']) + ' ' + ' '.join(x['b']) + ' '  .join(x['c'])

print(create_soup)
metadata['soup'] = metadata.apply(create_soup, axis=1)

#print(metadata.head(3))
#tfidf = TfidfVectorizer()
#tfidf_matrix = tfidf.fit_transform(metadata['soup'])
#cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
#indices = pd.Series(metadata.index, index=metadata['name']).drop_duplicates()

count = CountVectorizer(token_pattern=r"\b\w+\b")
count_matrix = count.fit_transform(metadata["soup"])
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
metadata = metadata.reset_index()
indices = pd.Series(metadata.index, index=metadata['name'])

print(cosine_sim2)

print(get_recommendations('Senter 31', cosine_sim2, indices))