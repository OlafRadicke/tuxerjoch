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
respon = rc.createDB("erstedb")
print(respon.headers)
print(respon.text)

# get a UUID
#print( rc.getUUID() )

# Add a json document
print("-------insertDoc----------")
json_data = '{"Type": "artist", "title":"Goldbergvariationen","author":"Bach", "tags": ["eins","zwei","drei"]}'
respon = rc.insertDoc(json_data)
print(respon.headers)
print(respon.text)


# Add a json document
print("-------insertDoc----------")
json_data = '{"Type": "artist", "title":"3. Symphony","author":"Bethoven"}'
respon = rc.insertDoc(json_data)
print(respon.headers)
print(respon.text)


# Add a json document
print("-------insertDoc----------")
json_data = '{"Type": "artist", "title":"Kleine Nachtmusik","author":"Mozart"}'
respon = rc.insertNamedDoc("kleine_nachtmusik", json_data)
print(respon.headers)
print(respon.text)


# Get value of a json document
print("-------getDocValue----------")
respon = rc.getDocValue("kleine_nachtmusik")
print(respon.headers)
print(respon.text)
print(json.loads(respon.text)["author"])

# get all documents
print("-------getAllDocs----------")
respon = rc.getAllDocs()
print(respon.headers)
print(respon.text)


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
respon = rc.addDesign(json_doc)
print(respon.headers)
print(respon.text)

# get design
print("-------getDesign----------")
respon = rc.getDesign()
print(respon.headers)
print(respon.text)


# get design
print("-------getNamedDesign----------")
respon = rc.getNamedDesign("by_artist_name")
print(respon.headers)
print(respon.text)

# Get temporary view
print("-------getTempView----------")
json_doc = "{ \"map\" : \"function(doc) { if (doc.artist == 'Mozart') { emit(null, doc.title); } }\" }"
respon = rc.getTempView(json_doc)
print(respon.headers)
print(respon.text)

# Get temporary view
print("-------getTempView-2----------")
json_doc = "{ \"map\" : \"function(doc) { if( doc.tags.indexOf('eins')  !== -1) { emit(null, doc.title); } }\" }"
respon = rc.getTempView(json_doc)
print(respon.headers)
print(respon.text)

# Delete document
print("-------deleteDoc----------")
respon = rc.deleteDoc("kleine_nachtmusik")
print(respon.headers)
print(respon.text)


# Get all databes names
print("-------getAllDBs----------")
respon = rc.getAllDBs()
print(respon.headers)
print(respon.text)

# delete db
print("--------deleteDB---------")
respon = rc.deleteDB("erstedb")
print(respon.headers)
print(respon.text)
