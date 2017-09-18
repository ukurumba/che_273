from tsp import tsp
import json
import requests
import sys

print("\n\n\nTSP Problem\n")
print("--------------------------------------------------------------\n")
print("Our goal is to find the shorest path between the given cities.\n")
print("We do this by using the Simulated Annealing algorithm.\n")
print("This requires the distance matrix for the cities, which we call from the Google Distance Matrix API.\n")
print("The code calling into the Google API is heavily taken from https://github.com/olliefr. Credit to this person not me.\n")



google_api_key = "AIzaSyA9Za2HLFr09zk5-ED4xD0GJJNIObCwQFU"
# Google Distance Matrix base URL to which all other parameters are attached
base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

# Google Distance Matrix domain-specific terms: origins and destinations
print("Total Number of Cities: " + str(len(sys.argv)-1))
if len(sys.argv) == 1:
	origins = ['Boston','Chicago','Dallas','Los Angeles', 'Miami', 'New York City', 'Rochester, NY']
	
else:
	origins = []
	for i in range(1,len(sys.argv)):
		origins.append(sys.argv[i])
destinations = origins
#['San Francisco', 'Victoria, BC']

# Prepare the request details for the assembly into a request URL
payload = {
	'origins' : '|'.join(origins),
	'destinations' : '|'.join(destinations), 
	'mode' : 'driving',
	'api_key' : google_api_key
}


print("Using the following cities: "+str(origins))
print("We call out to the Google API. After parsing we get the following distance matrix: \n")

# Assemble the URL and query the web service
r = requests.get(base_url, params = payload)



# Check the HTTP status code returned by the server. Only process the response, 
# if the status code is 200 (OK in HTTP terms).
if r.status_code != 200:
	print('HTTP status code {} received, program terminated.'.format(r.status_code))
else:
	try:
		# Try/catch block should capture the problems when loading JSON data, 
		# such as when JSON is broken. It won't, however, help much if JSON format
		# for this service has changed -- in that case, the dictionaries json.loads() produces
		# may not have some of the fields queried later. In a production system, some sort
		# of verification of JSON file structure is required before processing it. In XML
		# this role is performed by XML Schema.
		x = json.loads(r.text)

		# Now you can do as you please with the data structure stored in x.
		# Here, we print it as a Cartesian product.
		dist_mat = []
	
		for isrc, src in enumerate(x['origin_addresses']):
			newest_row = []
			for idst, dst in enumerate(x['destination_addresses']):

				row = x['rows'][isrc]


				cell = row['elements'][idst]

				if cell['status'] == 'OK':
					newest_row.append(float(cell['distance']['value'])/1000)
				else:
					print('{} to {}: status = {}'.format(src, dst, cell['status']))
			print(str(newest_row))
			dist_mat.append(newest_row)
		

		print("\nNow we call the simulated annealing algorithm to produce the shortest path: \n")

		tsp1 = tsp(dist_mat,500,-1.1)
		shortest_path = tsp1.find_path_sa(num_its = 1000)
		cost = tsp1.calc_cost(shortest_path)

		print("\n Final Answer: ")
		print([origins[i] for i in shortest_path])
		print("Cost: " + str(cost))



	except ValueError:
		print('Error while parsing JSON response, program terminated.')



