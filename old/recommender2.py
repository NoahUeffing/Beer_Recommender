import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to convert all strings to lower case and strip spaces


def clean_data(x):
    if isinstance(x, str):
        return str.lower(x.replace(" ", ""))
    else:
        return ''


def create_soup(x):
    return x['Category'] + ' ' + x['Style'] + ' ' + x['ABV'] + ' ' + x['Brewery'] + ' ' + x['Taste_Profile'] + ' ' + x['Country'] + ' ' + x['Food_Pairing'] + ' ' + x['Flavours'] + ' ' + x['IBU'] + ' ' + x['Province']

# Give recommendations for input beer


def get_recommendations(name, cosine_sim):
    # Get the index of the beer that matches the name
    idx = indices[name]

    # Get the pairwsie similarity scores of all beers with input beer
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the beers based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar beers
    sim_scores = sim_scores[1:11]

    # Get the beer indices
    beer_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar beers
    return metadata['Name'].iloc[beer_indices]
    # Add to previous line to add link to output
    #+ " " + metadata['Link'].iloc[beer_indices]


likedBeer = input("Enter a beer for related recommendations: ")

# Load Beers Metadata
metadata = pd.read_csv('beers.csv', low_memory=False)

# Replace NaN with an empty string
# metadata['Flavours'] = metadata['Flavours'].fillna('')

descriptors = ['Category', 'Style', 'ABV', 'Brewery',
               'Taste_Profile', 'Country', 'Food_Pairing', 'Flavours', 'IBU', 'Province']

for descriptor in descriptors:
    metadata[descriptor] = metadata[descriptor].apply(clean_data)

# Create a new soup feature
metadata['soup'] = metadata.apply(create_soup, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(metadata['soup'])
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# Reset index of main DataFrame and construct reverse mapping
metadata = metadata.reset_index()
indices = pd.Series(metadata.index, index=metadata['Name'])

print(get_recommendations(likedBeer, cosine_sim2))
