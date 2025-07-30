import os
from distance_matrix import create_distance_matrix
from dotenv import load_dotenv
from vrp.models import VRPRequest
from vrp.config import API_KEY

load_dotenv()
API_key = os.getenv("API_KEY")


def test(data:VRPRequest){

  locations =  [data.depot] + data.stops
  distance_matrix = create_distance_matrix(locations, API_KEY)
  return distance_matrix
  
}
