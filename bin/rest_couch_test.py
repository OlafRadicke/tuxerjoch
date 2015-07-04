# -*- coding: utf-8 -*-
import couch_backend.rest
import json

rc = couch_backend.rest.RestWrapper()
rc.setHost("127.0.0.1")
rc.setPort("5984")
rc.setPassword("admin")
rc.setUser("admin")
rc.setDB("erstedb")
#resp, content = rc.doGET("/")

#print("resp: ")
#print(resp)
#print("content: ")
#print(content)

# create database
print("--------createDB---------")
response = rc.createDB("erstedb")
print(response.headers)
print(response.text)

# get a UUID
#print( rc.getUUID() )

# Add a json document
print("-------insertDoc----------")
json_data = '{"Type": "artist", "title":"Goldbergvariationen","author":"Bach", "tags": ["eins","zwei","drei"]}'
response = rc.insertDoc(json_data)
print(response.headers)
print(response.text)


# Add a json document
print("-------insertDoc----------")
json_data = '{"Type": "artist", "title":"3. Symphony","author":"Bethoven"}'
response = rc.insertDoc(json_data)
print(response.headers)
print(response.text)


# Add a json document
print("-------insertDoc----------")
json_data = '{"Type": "artist", "title":"Kleine Nachtmusik","author":"Mozart"}'
response = rc.insertNamedDoc("kleine_nachtmusik", json_data)
print(response.headers)
print(response.text)


# Get value of a json document
print("-------getDocValue----------")
response = rc.getDocValue("kleine_nachtmusik")
print(response.headers)
print(response.text)
print(json.loads(response.text)["author"])

# get all documents
print("-------getAllDocs----------")
response = rc.getAllDocs()
print(response.headers)
print(response.text)


# Add design
print("-------addDesign----------")
json_doc = "{ \"_id\":\"_design/first_design\","
json_doc += "\"language\": \"javascript\","
json_doc += "\"views\":"
json_doc += "{"
json_doc += "\"all\": {"
json_doc += "\"map\": \"function(doc) { if (doc.Type == 'artist')  emit(null, doc) }\""
json_doc += "},"
json_doc += "\"by_artist_name\": {"
json_doc += "\"map\": \"function(doc) { if (doc.artist == 'Mozart')  emit(doc.artist, doc.title, doc) }\""
json_doc += "}"
json_doc += "}"
json_doc += "}"
response = rc.addDesign(json_doc)
print(response.headers)
print(response.text)

# get design
print("-------getDesign----------")
response = rc.getDesign()
print(response.headers)
print(response.text)


# get design
print("-------getNamedDesign----------")
response = rc.getNamedDesign("by_artist_name")
print(response.headers)
print(response.text)

# Get temporary view
print("-------getTempView----------")
json_doc = "{ \"map\" : \"function(doc) { if (doc.artist == 'Mozart') { emit(null, doc.title); } }\" }"
response = rc.getTempView(json_doc)
print(response.headers)
print(response.text)

# Get temporary view
print("-------getTempView-2----------")
json_doc = "{ \"map\" : \"function(doc) { if( doc.tags.indexOf('eins')  !== -1) { emit(null, doc.title); } }\" }"
response = rc.getTempView(json_doc)
print(response.headers)
print(response.text)

# Delete document
print("-------deleteDoc----------")
response = rc.deleteDoc("kleine_nachtmusik")
print(response.headers)
print(response.text)


# Get all databes names
print("-------getAllDBs----------")
response = rc.getAllDBs()
print(response.headers)
print(response.text)

# delete db
print("--------deleteDB---------")
response = rc.deleteDB("erstedb")
print(response.headers)
print(response.text)
