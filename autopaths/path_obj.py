# a wrap for the path
# returns a json
# this class creates a new path obj using GH

class Path:
    def __init__(self, x1, y1, x2, y2):
        self.path_from_graphhopper = self.Generate_path_from_graphhopper(lon1, lat1, lon2, lat2)
        self.length = self.get_length(path_from_graphhopper)
        self.objects = self.get_objects(path_from_graphhopper) # for Reem's team to implement,use get_objects function to generate this field, out should be 
        # some kind of dictionary (could be json) in which the keys are the objects and the values are their amount
        self.turns= self.get_turns(path_from_graphhopper) #dictionary with all objects

    def Generate_path_from_graphhopper(self, lon1, lat1, lon2, lat2):
        url = "https://graphhopper.com/api/1/route?point=" + lon1 + "," + lat1 + "&point=" + lon2 + "," + lat2 + "&vehicle=foot&locale=he-IL&points_encoded=false&weighting=fastest&layer=Thunderforest&key=ce343110-4f66-44c3-84ec-1c33cc1ffe15"
        text = urllib.request.urlopen(url).read()
        jsonL = json.loads(text)
        #list_of_coordinates=(jsonL['paths'][0]['points']['coordinates'])
        #list_of_insructions=(jsonL['paths'][0]['instructions'])
        #print (list_of_coordinates)
        #print (list_of_insructions)
        return jsonL

    def get_length(self, path_from_graphhopper):
        length = (jsonL['paths'][0]['distance'])
        return length
    
    def get_objects(self, path_from_graphhopper): #Reem's team implement
        return objects

    def get_turns(self, path_from_graphhopper): #Reem's team implement. output should be a dictionary with the table we've talked about
        return turns

    def to_json(self):
        as_json = dict(self.__dict__)
        return as_json

  