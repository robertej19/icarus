import feedparser
import geopy.distance


######## BASIC WORKING EXAMPLE 1 
# NewsFeed = feedparser.parse("https://inciweb.nwcg.gov/feeds/rss/incidents/")


# ##Run this as an example to see what is going on:
# first_entry = NewsFeed.entries[0]  #"NewsFeed" is a list of dictionaries, we want the first dictionary
# #print(first_entry.keys()) #Show the keys of the dictionary
# ##After running the above, we should see that the keys are:

# ##['title', 'title_detail', 'published', 'published_parsed', 
# ##'where', 'geo_lat', 'geo_long', 'links', 'link', 'id', 
# ##'guidislink', 'summary', 'summary_detail'])



######## BASIC WORKING EXAMPLE 2
# #As example, SNRA lat long @ alturas trailhead and see how far away each incident is 
# target_lat = 43.89798 
# target_long = -114.90373
# target_coords = (target_lat,target_long)

# for entry_number, entry in enumerate(NewsFeed.entries):
#     #print(entry_number)
#     #print(entry['geo_lat'])
#     print(entry['published'])
#     #print(entry['geo_long'])
#     incident_coords = (entry['geo_lat'],entry['geo_long'])

#     distance_km = geopy.distance.distance(target_coords, incident_coords).km
#     distance_miles = distance_km*0.621371
#     print(distance_miles)



######## BASIC WORKING EXAMPLE 3
# Now lets wrap this up into a function

def GetFiresCloseTo(target_lat=44.5902,target_long=104.7146,incident_radius_miles=50):
    NewsFeed = feedparser.parse("https://inciweb.nwcg.gov/feeds/rss/incidents/")
    
    target_coords = (target_lat,target_long)

    entries_within_radius = []
    for entry_number, entry in enumerate(NewsFeed.entries):
        incident_coords = (entry['geo_lat'],entry['geo_long'])
        distance_km = geopy.distance.distance(target_coords, incident_coords).km
        distance_miles = distance_km*0.621371
        if distance_miles <= incident_radius_miles:
            entry['distance_miles'] = distance_miles
            entries_within_radius.append(entry)

    sorted_entries_within_radius = sorted(entries_within_radius, key = lambda i: i['distance_miles'])

    return sorted_entries_within_radius

# We will use SNRA again and get a list returned of incidents with the specified radius
target_lat_1 = 43.89798 
target_long_1 = -114.90373
incident_radius_miles_1 = 10
sorted_entries_within_radius = GetFiresCloseTo(target_lat=target_lat_1,
                                                target_long=target_long_1,
                                                incident_radius_miles=incident_radius_miles_1)

#Now, lets print those out. We can put this script on a server, and have it send emails instead of printing out results.
if not sorted_entries_within_radius: #i.e. if there are no entries within the defined radius:
    print("No incidents have been reported within a radius of {} miles of ({},{})".format(incident_radius_miles_1,
            target_lat_1,target_long_1))
else:
    for entry in sorted_entries_within_radius:
        print("\nIncident found {:.2f} miles from target location\n".format(entry['distance_miles']))
        print("Incident Name: {}\n".format(entry['title']))
        print("Date Published: {}\n".format(entry['published']))
        print("Latitude: {} Longitude : {}\n".format(entry['geo_lat'],entry['geo_long']))
        print("Incident Summary: {} \n \n".format(entry['summary']))
