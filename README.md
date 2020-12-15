# Beer_Recommender

DBMS Project. NSLC Beer Recommender

- The project is hosted at https://nslc-beer-recommender.herokuapp.com
  This is a Python/Flask web application for my Database Managment Systems course at Acadia University. It aims to recommend beers available at the NSLC to the user after it is given a beer as input.

To install and run the dev environment:

- To install dependencies, navigate to main folder "Beer_Recommender" in either command prompt or terminal window and enter "pip install -r requirements.txt".

- To launch the app, using a terminal or comannd prompt, navigate to the directory containing all project files(Beer_Recommender) and enter "python nslcRecommender.py". This should launch the app and open a browser window to access the site.

createBeerDatabase.py can be run to generate a new NSLC_Beers.db file from beers.csv if the database needs to be updated or recreated.
If you plan on doing this, make sure to delete your NSLC_Beers.db file if it exists before running createBeerDatabase.py.
To add more beers to the database, simply add more entires in the beers.csv file and run createBeerDatabase.py.

The "old" folder contains previous versions of the recommender that use a command line interface to recommend beer.

Note: All code has been included in this submission, including pieces that were ultimately not used in the final app.
