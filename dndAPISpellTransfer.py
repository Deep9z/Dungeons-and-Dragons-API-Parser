#Author: Adrian LaCour
#Description: Parses through a website url with JSON data. Inserts the list into
#             a Google Firestore database 


import json
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#Open up the Google Firestore databse, credentials have been removed since this is being put public
cred = credentials.Certificate("CredentialsInsteretedHere")
firebase_admin.initialize_app(cred)

db = firestore.client()



url = ("https://dl.dropboxusercontent.com/s/121t7xstyyeofxw/5e-SRD-Spells.json")
response = requests.get(url).json()

counter = 1#Make a counter to assing as the index of the spell

# Iterate through all of the spells, as it is givin as one large JSON file
for item in response:

    #Don't add in the license bit at the end of the JSON document
    if 'license' in item:
        break

    #Remove the / in the names, as it affects the naming,a s the database thinks its a file path
    nameString = item['name']
    sep = '/'
    newName = nameString.split(sep, 1)[0]
    docName = newName

    #Remove the paragraph marks from the description
    description = item['desc']
    description = description.replace("<p>", "")
    description = description.replace("</p>", "")


    #Put all of the informaiton intotheir proper fields
    data = {
        u'index' : counter,
        u'name' : newName,
        u'description' : description,
        u'higherLevel' : "",
        u'page' : item['page'],
        u'range' : item['range'],
        u'components' : item['components'],
        u'material' : "",
        u'ritual' : item['ritual'],
        u'duration' : item['duration'],
        u'concentration' : item['concentration'],
        u'castingTime' : item['casting_time'],
        u'level' : item['level'],
        u'school' : item['school'],#may need to change this
        u'classes' : item['class']
        }

    #If these pieces of data exist for the spell, ad it in
    if 'higher_level' not in item:
        pass
    else:
        higherLevel= item['higher_level']
        higherLevel = higherLevel.replace("<p>", "")
        higherLevel = higherLevel.replace("</p>", "")
        data[u'higherLevel'] = higherLevel

    if 'material' not in item:
        pass
    else:
        data[u'material'] = item['material']

    #add in archetype and circles,
    #Put the above data in the current database
    doc_ref = db.collection(u'Spells').document(docName).set(data) #dynamically add in the document, as the monster name
    counter += 1
