def find_optimal(all_paths):
  path_min_index = 0
  min_weight = sys.maxint
  for i in range(len(all_paths)):
    tmp_min = path_weight(all_paths[i])
    if (tmp_min < min_weight):
      min_weight = tmp_min
      path_min_index = i
  return all_paths[path_min_index]

def path_weight(path):
  #path_length_weight = path_length_weight(path)
  #path_objects_weight = path_objects_weight(path)
  #path_turns_weight = path_turns_weight()
  #total_weight = path_length_weight + path_objects_weight + path_turns_weight
  return path_length_weight(path) + path_objects_weight(path) + path_turns_weight(path)

def path_length_weight(path):
  len = path.length # TODO assert in what units the distance is meseaured in and normalize if neccessary
  return len

def path_turns_weight(path):
  turns = path.turns
  turns_total_weight = 0
  for i in range(len(turns)):
    turns_total_weight += i * turns[i]  # TODO figure out what the exact turns data structure API and edit the code accordingly
    # TODO figure out how to normalize and sum with the other weights (the ones based on length and objects)
  return turns_weight

        
#       find_min_path- create an array 
#       for(i=0, i<num_of_paths, i++) 
#           weight=path_weight(all_paths[i])- computes the path's weight using path_length_weight(path) and path_parameters_weight(path) funcs
#           find_min_path[i]=weight
#       optimal_path=find_min(find_min_path)- returns the index of optimal array
#       return (all_paths[optimal_path])
#
# path_length_weight(path)- gets a path. returns the weight of the path by length. 
# path_parameters_weight(path)- computes the path weight by known parameters
# find_min(find_min_path)- returns path's index
import urllib.request
import json
import webbrowser

def path_length_weight():
  #lon1 = "34.80298"
  #lat1 = "32.11324"
  #lon2 = "34.80584"
  #lat2 = "32.11304"
  lon1 = "34.80178"
  lat1 = "32.11332"
  lon2 = "34.80591"
  lat2 = "32.11296"
  url = "https://graphhopper.com/api/1/route?point=" + lon1 + "," + lat1 + "&point=" + lon2 + "," + lat2 + "&vehicle=foot&locale=he-IL&points_encoded=false&weighting=fastest&layer=Thunderforest&key=ce343110-4f66-44c3-84ec-1c33cc1ffe15"
  #get_path_url("34.80178", "32.11332", "34.80591", "32.11296")
  #url = "https://graphhopper.com/api/1/route?point=,34.80178,32.11332&point=34.80591,32.11296&vehicle=foot&locale=he-IL&points_encoded=false&weighting=fastest&layer=Thunderforest&key=ce343110-4f66-44c3-84ec-1c33cc1ffe15"
  #https://www.openstreetmap.org/directions?engine=graphhopper_foot&route=32.11325%2C34.80227%3B32.11310%2C34.80424#map=19/32.11262/34.80328
  text = urllib.request.urlopen(url).read()
  jsonL = json.loads(text)
  distance = (jsonL['paths'][0]['distance'])
  print(distance)

  def path_objects_score(Path path):
    getPathObjects(Path path)

path_length_weight()
