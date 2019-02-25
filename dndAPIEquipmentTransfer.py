#Author: Adrian LaCour
#Description: Parses through a website url with JSON data. Inserts the list into
#             a Google Firestore database

import json
import requests
import copy

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#Open up the Google Firestore databse, credentials have been removed since this is being put public
cred = credentials.Certificate("dungeons-and-dragons-comp-app-399340606421.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


#Iterate through entire json document and run, getting all of the monsters
for i in range (1, 257):
    print(i)

    url = ("http://www.dnd5eapi.co/api/equipment/" + str(i) + "/")#Dynamically change the url
    response = requests.get(url).json()#Get the data for the specific monster

    #Remove the / in the names, as it affects the naming,a s the database thinks its a file path
    nameString = response['name']
    sep = '/'
    newName = nameString.split(sep, 1)[0]
    docName = newName

    #Put the data in a dictionary, for use in formatting for the database
    data = {
        u'index' : response['index'],
        u'name' : docName,

        u'equipmentCategory' : response['equipment_category'],
        }

    #Add in the special abilities, actions, and legendary actions
    if 'weapon_category' in response:
        data[u'subCategory'] : response['weapon_category']
    elif 'vehicle_category' in response:
        data[u'subCategory'] : response['vehicle_category']
    elif 'armor_category' in response:
        data[u'subCategory'] : response['armor_category']
    elif 'tool_category' in response:
        data[u'subCategory'] : response['tool_category']
    elif 'gear_category' in response:
        data[u'subCategory'] : response['gear_category']

    if 'weapon_range' not in response:
        pass
    else:
        data[u'weaponRange'] : response['weapon_range']

    data[u'cost'] = str(response['cost']['quantity']) + " " + str(response['cost']['unit'])

    if 'armor_class' in response:
        specialData = {}
        specialData[u'base'] = response['armor_class']['base']
        specialData[u'dexBonus'] = response['armor_class']['dex_bonus']
        specialData[u'maxBonus'] = response['armor_class']['max_bonus']
        data[u'armorClass'] = specialData

    if 'str_minimum' in response:
        data[u'strMinimum'] = response['str_minimum']

    if 'stealth_disadvantage' in response:
        data[u'stealthDisadvantage'] = response['stealth_disadvantage']

    if 'properties' in response:
        data[u'properties'] = []
        for item in response['properties']:
            data[u'properties'].append(copy.deepcopy(item['name']))

    if 'category_range' in response:
        data[u'categoryRange'] = response['category_range']

    if 'damage' in response:
        specialData = {}
        specialData[u'diceCount'] = response['damage']['dice_count']
        specialData[u'diceValue'] = response['damage']['dice_value']
        specialData[u'damageType'] = response['damage']['damage_type']['name']
        data[u'damage'] = specialData #May need to adjust this to append

    if '2h_damage' in response:
        specialData = {}
        specialData[u'diceCount'] = response['damage']['dice_count']
        specialData[u'diceValue'] = response['damage']['dice_value']
        specialData[u'damageType'] = response['damage']['damage_type']['name']
        data[u'2h_damage'] = specialData #May need to adjust this to append

    if 'speed' in response:
        data[u'speed'] = str(response['speed']['quantity']) + " " + str(response['speed']['unit'])

    if 'weight' in response:
        data[u'weight'] = response['weight']

    if 'desc' in response:
        str1 = ''.join(response['desc'])
        data[u'description'] = str1



    #Put the above data in the current database
    doc_ref = db.collection(u'Equipment').document(docName).set(data) #dynamically add in the document, as the monster name
