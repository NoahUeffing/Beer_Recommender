from flask import Flask, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sqlite3

# Used to convert each string in beers table to standard format for comparison
# Convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, str):
        return str.lower(x.replace(" ", ""))
    else:
        return ''

# Used to allow each entry in beers2 table to be printed for html output
def clean_string(x):
    if isinstance(x, str):
        return str(x)
    else:
        return ''

# Creates word soup for similairty comparision
def create_soup(x):
    return x['Category'] + ' ' + x['Style'] + ' ' + x['ABV'] + ' ' + x['Brewery'] + \
        ' ' + x['Taste_Profile'] + ' ' + x['Country'] + ' ' + x['Food_Pairing'] + ' ' + \
        x['Flavours'] + ' ' + x['IBU'] + ' ' + x['Province']

# Gives beer reccomendations for a given beer name, using an input cosine similarity measure and indicies,
# as well as dataframe for stylized output
def get_recommendations(name, cosine_sim, indices, dataFrame):
    # Find liked beer in the dataframe
    if (dataFrame['Name'] == name).any():
        results = []
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

        # Gather each beer and it's attributes for out
        recommendations = dataFrame['Name'].iloc[beer_indices] + \
            "?" + dataFrame['Category'].iloc[beer_indices] + "?" + dataFrame['Style'].iloc[beer_indices] + \
            "?" + dataFrame['IBU'].iloc[beer_indices] + "?" + dataFrame['ABV'].iloc[beer_indices] + \
            "?" + dataFrame['Brewery'].iloc[beer_indices] + "?" + dataFrame['Province'].iloc[beer_indices] + \
            "?" + dataFrame['Country'].iloc[beer_indices] + "?" + dataFrame['Taste_Profile'].iloc[beer_indices] + \
            "?" + dataFrame['Food_Pairing'].iloc[beer_indices] + "?" + dataFrame['Flavours'].iloc[beer_indices] + \
            "?" + dataFrame['Link'].iloc[beer_indices]

        # Format the each recommended beer's attribbutes into an html list
        for val in recommendations:
            entry = val.split("?")
            results.append(
                "<li><b><i>" + entry[0] + "</i></b><a href=" + entry[11] + "> Link</a>" + "<ul><li> <b>Category</b>: " +
                entry[1] + "</li> <li><b>Style</b>: " + entry[2] + "</li><li> <b>IBU</b>: " + entry[3] +
                "</li><li> <b>ABV</b>: " + entry[4] + "</li><li> <b>Brewery</b>: " + entry[5] +
                "</li><li> <b>Province</b>: " + entry[6] + "</li><li> <b>Country</b>: " + entry[7] +
                "</li><li> <b>Taste Profile</b>:  " + entry[8] + "</li><li> <b>Food Pairing</b>: " + entry[9] +
                "</li><li> <b>Flavours</b>: " + entry[10] + "</li></ul></li><br>")

        # Return the top 10 most similar beers as an html table
        return "".join(results)

    # If liked beer is not in the dataframe
    else:
        return "No beer named '" + name + "' found in the database. Try copy and pasting a name from the 'Name'" + \
            " column into the recommender."


app = Flask(__name__)

# Homepage
@app.route('/')
# Format all beers in db to an html table
def home():
    conn = sqlite3.connect('NSLC_Beers.db')

    beerList = pd.read_sql('''  
    SELECT * FROM NSLC_BEERS
            ''', conn)
    del beerList['Link']
    beerList.index += 1
    beerList = beerList.fillna('')
    beerList.rename(columns={'Taste_Profile': 'Taste Profile',
                             'Food_Pairing': 'Food Pairing'}, inplace=True)
    beerList = beerList.to_html()
    return HOME_HTML.format(beerList)


# html code for home page
HOME_HTML = """
    <html>
    <body>
        <h2>NSLC Beer Recommender</h2>
        <form action="/recommend">
            Enter any beer name from the list below (case-sensitive)<input type='text' name='likedBeer'><br>
            <input type='submit' value='Recommend Beer'>
        </form>
        {0}
    </body></html>"""

# Recommendations page
@app.route('/recommend')
# Generate the recommendations for output as an html list
def recommend():
    # gets liked beer from homepage form input
    likedBeer = request.args.get('likedBeer', '')
    # Check if liked beer was entered before button was pushed
    if likedBeer == '':
        msg = 'No beer was entered.'
    else:
        msg = 'Here are some beers like ' + likedBeer + ':'

    conn = sqlite3.connect('NSLC_Beers.db')

    # dataframe used to get recommendations
    beers = pd.read_sql('''  
    SELECT * FROM NSLC_BEERS
            ''', conn)
    # dataframe used to output formated recommendations (maintain case, spacing, and stop words)
    beers2 = pd.read_sql('''  
    SELECT * FROM NSLC_BEERS
            ''', conn)

    descriptors = ['Category', 'Style', 'ABV', 'Brewery',
                   'Taste_Profile', 'Country', 'Food_Pairing', 'Flavours', 'IBU', 'Province']

    # Format the dataframes for their intended useage
    for descriptor in descriptors:
        beers[descriptor] = beers[descriptor].apply(clean_data)
        beers2[descriptor] = beers2[descriptor].apply(clean_string)

    # Create a new soup feature
    beers['soup'] = beers.apply(create_soup, axis=1)

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(beers['soup'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

    # Reset index of main DataFrame and construct reverse mapping
    beers = beers.reset_index()
    indices = pd.Series(beers.index, index=beers['Name'])
    # Return the recommendations in html form
    return RECOMMEND_HTML.format(msg, get_recommendations(likedBeer, cosine_sim2, indices, beers2))


# html for recommendations page
RECOMMEND_HTML = """
    <html><body>
        <h2>{0}</h2>
        <a href="/">Back to Recommender</a>
        <ol>
            {1}
        </ol>
    </body></html>
    """

if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(host="localhost", debug=True)
