#Author: Adrian LaCour
#Description: Parses through a website url with JSON data. Inserts the list into
#             a Google Firestore database 

import json
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#Open up the Google Firestore databse, credentials have been removed since this is being put public
cred = credentials.Certificate("dungeons-and-dragons-comp-app-e462a73a2dd5.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


#Iterate through entire json document and run, getting all of the monsters
for i in range (1, 326):
    print(i)

    url = ("http://www.dnd5eapi.co/api/monsters/" + str(i) + "/")#Dynamically change the url
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
        u'size' : response['size'],
        u'type' : response['type'],
        u'subtype' : response['subtype'],
        u'alignment' : response['alignment'],
        u'armorClass' : response['armor_class'],
        u'hitPoints' : response['hit_points'],
        u'hitDice' : response['hit_dice'],
        u'speed' : response['speed'],
        u'strength' : response['strength'],
        u'dexterity' : response['dexterity'],
        u'constitution' : response['constitution'],
        u'intelligence' : response['intelligence'],
        u'wisdom' : response['wisdom'],
        u'damageVulnerabilities' : response['damage_vulnerabilities'],
        u'damageResistances' : response['damage_resistances'],
        u'damageImmunities' : response['damage_immunities'],
        u'conditionImmunities' : response['condition_immunities'],
        u'senses' : response['senses'],
        u'languages' : response['languages'],
        u'challengeRating' : response['challenge_rating'],
        u'specialAbilities' : [],
        u'actions' : [],
        u'legendaryActions': []
        }

    #Add in the special abilities, actions, and legendary actions
    if 'charisma' not in response:
        pass
    else:
        data[u'charisma'] = response['charisma']



    if 'special_abilities' not in response:
        pass
    else:
        specialData = {}
        for item in response['special_abilities']:
            print(item)
            if 'attack_bonus' not in response:
                pass
            else:
                specialData[u'attackBonus'] = item['attack_bonus']
            if 'damage_dice' not in response:
                pass
            else:
                specialData[u'damageDice'] = item['damage_dice']
                specialData[u'damageBonus'] = item['damage_bonus']
            specialData[u'description'] = item['desc']
            specialData[u'name'] = item['name']
            data[u'specialAbilities'].append(specialData)


    if 'actions' not in response:
        pass
    else:
        specialData = {}
        for item in response['actions']:
            if 'attack_bonus' not in response:
                pass
            else:
                specialData[u'attackBonus'] = item['attack_bonus']
            if 'damage_dice' not in response:
                pass
            else:
                specialData[u'damageDice'] = item['damage_dice']
                specialData[u'damageBonus'] = item['damage_bonus']
            specialData[u'description'] = item['desc']
            specialData[u'name'] = item['name']
            data[u'actions'].append(specialData)


    if 'legendary_actions' not in response:
        pass
    else:
        specialData = {}
        for item in response['legendary_actions']:
            if 'attack_bonus' not in response:
                pass
            else:
                specialData[u'attackBonus'] = item['attack_bonus']
            if 'damage_dice' not in response:
                pass
            else:
                specialData[u'damageDice'] = item['damage_dice']
                specialData[u'damageBonus'] = item['damage_bonus']
            specialData[u'description'] = item['desc']
            specialData[u'name'] = item['name']
            data[u'legendaryActions'].append(specialData)


    #Put the above data in the current database
    doc_ref = db.collection(u'Monsters').document(docName).set(data) #dynamically add in the document, as the monster name
