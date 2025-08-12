#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import io, json

def get_soup(url):
   response = requests.get(url)
   # print(response.content)
   # print(response.status_code)
   soup = BeautifulSoup(response.content, features="html.parser")
   return soup

def get_content(url):
   soup = get_soup(url)
   # print(soup.prettify())
   urls_dict = {}
   for a in soup.find_all('a'):
      if '/pincode/india/' in a['href']:
         urls_dict[a.get_text()] = a['href']
   return urls_dict

def get_pincode(url):
   soup = get_soup(url)
   for v in soup.find_all('td'):
      if v.getText().isdigit():
         return int(v.getText())

def get_locations(locations_url):
   output_locations = []
   for location in locations_url.keys():
      pincode = get_pincode(locations_url[location])
      print('\t\t', location, ':', pincode, ':', locations_url[location])
      output_location = {}
      output_location['location'] = location
      output_location['pincode'] = pincode
      output_locations.append(output_location)
   return output_locations

def get_districts(districts_url):
   output_districts = []
   for district in districts_url.keys():
      print('\t', district, ':', districts_url[district])
      output_district = {}
      output_district['district'] = district
      locations_url = get_content(districts_url[district])
      output_district['locations'] = get_locations(locations_url)
      output_districts.append(output_district)
   return output_districts

def get_states(states_url):
    output = []
    for state in states_url.keys():
       print(state, ":", states_url[state]) 
       output_dict = {}
       output_dict['state'] = state
       districts_url = get_content(states_url[state])
       output_dict['districts'] = get_districts(districts_url)
       output.append(output_dict)
    return output

def main(url):
    states_url = get_content(url)
    output_states = get_states(states_url)
    data = {'country': 'india', 'states': output_states}
    with io.open('india-pincode.txt', 'w', encoding='utf-8') as f:
       f.write(json.dumps(data, ensure_ascii=False))

if __name__ == '__main__':
   url = 'https://www.mapsofindia.com/pincode/india'
   main(url)
