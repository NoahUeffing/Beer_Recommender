import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

likedBeer = input("Enter a beer for related recommendations: ")

df = pd.read_csv('beers.csv')
# print(df)
# print(df.columns)

df = df[['Name', 'Flavours']]

# print(df.head())

# print(df.isnull().sum())
df.dropna(inplace=True)


tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3),
                     min_df=0, stop_words='english')

matrix = tf.fit_transform(df['Flavours'])
cosine_similarities = linear_kernel(matrix, matrix)
beer_name = df['Name']

indices = pd.Series(df.index, index=df['Name'])


def beer_recommend(beer):

    idx = indices[beer]

    sim_scores = list(enumerate(cosine_similarities[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:31]  # start at zero to include inputted beer

    beer_indices = [i[0] for i in sim_scores]

    return beer_name.iloc[beer_indices]


# Add .head(n) to only show n results
print(beer_recommend(likedBeer))
