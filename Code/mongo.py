__author__ = 'Ian'

import pprint
import csv

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline_hospital():

    pipeline = [
                {"$match": {"amenity":"hospital"}}

               ]
    return pipeline


def make_pipeline_amenity():

    pipeline =[{"$match":{"amenity":{"$exists":1}}},
               {"$group": {"_id": "$amenity", "count":{"$sum":1}}},
               {"$sort": {"count":-1}},
               {"$limit":100}
    ]

    return pipeline

def make_pipeline_shelter_location():

    pipeline =[{"$match": {"amenity":{"$exists":1},
                          "pos":{"$exists":1}}},
               {"$match": {"amenity":{"$in":["hospital","clinic","pharmacy", "place_of_worship","drinking_water", "shelter", "health_post", "community_centre"]}}},
               {"$project": {"amenity":"$amenity","Name":"$name", "location":"$pos"}}
    ]

    return pipeline

def make_missing_location():

    pipeline =[{"$match":{"amenity":{"$exists":1},
                          "pos":{"$exists":0},
                          "type":{"$in":["node", "way"]}}},

               {"$match": {"amenity":{"$in":["hospital","clinic","pharmacy", "place_of_worship","drinking_water", "shelter", "health_post", "community_centre"]}}}
    ]

    return pipeline

def make_profiling():

    shelter_profile_pipeline =[{"$match": {"amenity":{"$exists":1},
                                "pos":{"$exists":1},
                                "type":{"$in":["node", "way"]}}},
               {"$match": {"amenity":{"$in":["hospital","clinic","pharmacy", "place_of_worship","drinking_water", "shelter", "health_post", "community_centre"]}}},
               {"$group": {"_id": "$amenity", "count":{"$sum":1}}},
               {"$sort":{"count":-1}} ]


    missing_loc_profile_pipeline =[{"$match":{"amenity":{"$exists":1},
                                    "pos":{"$exists":0},
                                    "type":{"$in":["node", "way"]}}},

               {"$match": {"amenity":{"$in":["hospital","clinic","pharmacy", "place_of_worship","drinking_water", "shelter", "health_post", "community_centre"]}}},

               {"$group": {"_id": "$amenity", "count":{"$sum":1}}},
               {"$sort":{"count":-1}}
    ]

    return shelter_profile_pipeline, missing_loc_profile_pipeline

def run_query(db, pipeline):
    result = db.nepal.aggregate(pipeline)
    return result

def print_result(result, outfile):

    obj = open(outfile, 'wb')

    for document in result:

        obj.write(str(document)+"\n")

    obj.close


def print_csv(result, outfile):

    #OUTPUT SHELTER NAME, TYPE, LOCATIONS TO CSV file
    writer = csv.writer(open(outfile, 'wb'))

    #Insert header
    writer.writerow(["Amenity", "Lon", "Lat"])

    for document in result:

        #Extract the type of amenity
        amenity = document["amenity"]

        location = document["location"]

        #Extract longtitude and latitude from location list
        lat = location[0]
        lon = location[1]

        writer.writerow([amenity, lon, lat])

    print (">>>>> CSV Export Completed <<<<<")




if __name__ == "__main__":
    # Initial local db setup
    db = get_db('osm')

    # Create multiple query pipelines
    hospital_pipeline = make_pipeline_hospital()
    amenity_pipeline = make_pipeline_amenity()
    shelter_location_pipeline = make_pipeline_shelter_location()
    missing_location_pipeline = make_missing_location()
    shelter_profile_pipeline, missing_loc_profile_pipeline = make_profiling()

    #find top 10 amenity types
    amenity = run_query(db, amenity_pipeline)

    #find all shelter location such as hospital, clinic, pharmacy, places of worship, and water
    shelter = run_query(db, shelter_location_pipeline)

    #find all shelter with missing location to help improve map quality
    missing_location = run_query(db, missing_location_pipeline)

    missing_location_sum = run_query(db,missing_loc_profile_pipeline)


    #profiling the shelter and missing location elements

    shelter_prof = run_query(db, shelter_profile_pipeline)
    missing_loc_prof = run_query(db, missing_loc_profile_pipeline)



    #output query results to files
    #print_result(amenity, 'amenity.json')

    #print_result(shelter,'shelter.json')

    print_csv(shelter, 'shelter_location.csv')

    #print_result(missing_location,'missing_location.json')

    #print_result(missing_loc_prof, 'missing_location_summary.json')

    #print_result(shelter_prof, 'shelter_summary.json')


