# mongoDB_OSM_Nepal
Project to extract, cleanse, and visualize emergency facility near Kathmandu to help post earthquake rescue, aids, and rebuild

In Code folder, it contain all the python scripts that performs the following, 
1. mapparser.py - extract XML file
2. audit.py - analyze tag types to develop cleanse approach
3. data.py - cleanse data, create new data structure, and export to JSON format for MongoDB ingestion
4. mongo.py - perform various mongoDB queries to find all emergency facility locaitons, data issues, print output to text file, export all facility locations to csv for visualization in CartoDB
