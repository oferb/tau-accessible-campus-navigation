import urllib.request
import json
import webbrowser


def get_coordinates_of_path(lat1, lon1, lat2, lon2):
  url = "https://graphhopper.com/api/1/route?point=" + lon1 + "," + lat1 + "&point=" + lon2 + "," + lat2 + "&vehicle=foot&locale=he-IL&points_encoded=false&weighting=fastest&layer=Thunderforest&key=ce343110-4f66-44c3-84ec-1c33cc1ffe15"
  # + "&avoid=steps&ch.disable=true" 
  # + "&algorithm=alternative_route&ch.disable=true" 
  # + "&alternative_route.max_paths=10&alternative_route.max_share_factor=10&alternative_route.max_weight_factor=10" 
  # + "&layer=Omniscale" OR "&layer=Thunderforest" - with or without it works! ---> default is Omniscale (?)
  # point_hints - A way for giving Graphhopper a hint on one of the coordinate (start\end)
  # details flag options : https://discuss.graphhopper.com/t/new-routing-api-feature-path-details-and-support-for-avoiding-motorway-ferry-toll/2539
  # + "&details=surface&details=road_class" - kind of the surface (paved, asphelt, sand...) and kinf of the road (steps, footway, motorway...)

  text = urllib.request.urlopen(url).read()
  jsonL = json.loads(text)
  list_of_coordinates=(jsonL['paths'][0]['points']['coordinates'])
  list_of_insructions=(jsonL['paths'][0]['instructions'])
  #print (list_of_coordinates)
  #print (list_of_insructions)
  print (jsonL)
  return list_of_coordinates, list_of_insructions

def get_path_url(lat1, lon1, lat2, lon2):
  # Return the url to visualize path
  url = "https://www.openstreetmap.org/directions?engine=fossgis_osrm_foot&route=" + lon1 + "%2C" + lat1 + "%3B" + lon2 + "%2C" + lat2 + "#map=18/32.11315/34.80386"
  webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
  webbrowser.get().open(url, new=2, autoraise=True)
  print (url)

get_coordinates_of_path("34.80178", "32.11332", "34.80591", "32.11296") # start and end coordinates of the chosen path
get_path_url("34.80178", "32.11332", "34.80591", "32.11296") # start and end coordinates of the chosen path


# 3. Figure out how to manipulate the graphhopper paths:
#    - We can avoid things: stairs
#    - Can we pass through certain buildings?


# 4. Consider multiple paths and names for paths



