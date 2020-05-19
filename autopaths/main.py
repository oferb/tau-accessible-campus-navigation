import urllib.request
import json
from utils import *


def main(lat1, lon1, lat2, lon2):
    all_paths = generate_all_paths(lat1, lon1, lat2, lon2)
    optimal_path = find_optimal(all_paths)
    return get_path_coordinates(optimal_path)


if __name__ == "__main__":
    print(main("34.80582783314952", "32.1131048828473", "34.802181", "32.113266"))  # Exact Science - Entrance
    # print(main("34.80563", "32.11109", "34.80621", "32.11144")) # Dan David - Exact Science
    # print(main("34.805303532", "32.1114499","34.8025733", "32.1132642")) # Dan David - Entrance
    # print(main("34.8022963", "32.1132731", "34.80525109", "32.11147289")) # Entrance - Dan David
    # print(main("34.8058278", "32.1131049", "34.8046353", "32.1131046")) # Exact Science - Gilman
    # print(main("34.8045982", "32.1130372", "34.80582783314952", "32.1131048828473")) # Gilman - Exact Science
    # print(main("34.805467" , "32.111407", "34.804405" , "32.112254")) # Dan David - Gilman
    # print(main("34.804405" , "32.112254" , "34.805467" , "32.111407")) # Gilman - Dan David
    # print(main("34.80225742979806", "32.1132505791583", "34.804572", "32.1131201")) # Entrance - Gilman
    # print(main("34.804597" , "32.112987" , "34.802191" , "32.113260")) # Gilman -Entrance
    # print(main("34.80178", "32.11332", "34.80591", "32.11296")) # chosen path
