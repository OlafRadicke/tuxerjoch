
import requests
import json


class RestWrapper:
    ## A wrapper class for the rest api of couchdb

    uri_host = "localhost"
    uri_port = "5984"
    user = ""
    password = ""
    database = ""

    def setHost(self, hostname):
        self.uri_host = hostname

    def setPort(self, portnumber):
        self.uri_port = portnumber

    def setUser(self, name):
        self.user = name

    def setPassword(self, password):
        self.password = password

    def setDB(self, name):
        self.databese = name

    def doGET(self, uri_path):
        ## A GET-Request
        # @param uri_path the uri path
        request_uri = "http://" + self.uri_host + ":" + self.uri_port + uri_path
        print( request_uri )
        headers = {'content-type': 'application/json'}
        return requests.get(request_uri, auth=(self.user, self.password), headers=headers)

    def doPUT(self, uri_path):
        ## A PUT-Request
        # @param uri_path the uri path
        request_uri = "http://" + self.uri_host + ":" + self.uri_port + uri_path
        print(request_uri)
        return requests.put(request_uri, auth=(self.user, self.password))

    def doPUT2(self, uri_path, json_doc):
        ## A PUT-Request
        # @param uri_path the uri path
        # @param json_doc a json document
        request_uri = "http://" + self.uri_host + ":" + self.uri_port + uri_path
        return requests.put(request_uri, auth=(self.user, self.password), json=json.loads(json_doc))

    def doDELETE(self, uri_path):
        ## A DELETE-Request
        # @param uri_path the uri path
        request_uri = "http://" + self.uri_host + ":" + self.uri_port + uri_path
        return requests.delete(request_uri, auth=(self.user, self.password))

    def doPOST(self, uri_path, json_doc):
        ## A Post-Request
        # @param uri_path the uri path
        # @param json_doc a json document
        request_uri = "http://" + self.uri_host + ":" + self.uri_port + uri_path
        headers = {'content-type': 'application/json'}
        return requests.post(request_uri, auth=(self.user, self.password), json=json.loads(json_doc), headers=headers)

    def createDB(self, db_name):
        ## Creates a new data base.
        #  @param db_name name of the new database
        return self.doPUT("/" + db_name)


    def deleteDB(self, db_name):
        ## Delete a data base.
        #  @param db_name name of the database
        return self.doDELETE("/" + db_name)

    def getAllDBs(self):
        ## Get all databes names
        uri_path = "/_all_dbs"
        return self.doGET(uri_path)

    def getUUID(self):
        ## Get bback a UUID as string
        response = self.doGET("/_uuids")
        return json.loads(response.text)["uuids"][0]

    def insertDoc(self, json_doc):
        ## Insert a json document in a database.
        uri_path = "/" + self.databese + "/" + self.getUUID()
        return self.doPUT2(uri_path, json_doc)

    def insertNamedDoc(self, name, json_doc):
        ## Insert a named json document in a database.
        uri_path = "/" + self.databese + "/" + name
        return self.doPUT2(uri_path, json_doc)

    def getAllDocs(self):
        ## Get all documents
        uri_path = "/" + self.databese + "/_all_docs"
        return self.doGET(uri_path)

    def deleteDoc(self, name):
        response = self.getDocValue(name)
        rev_no = json.loads(response.text)["_rev"]
        uri_path = "/" + self.databese + "/" + name
        request_uri = "http://" + self.uri_host + ":" + self.uri_port + uri_path
        json_doc = '{"_id": "' + name + '", "_rev": "' + rev_no + '", "_deleted":true}'
        return requests.put( request_uri, auth=(self.user, self.password), json=json.loads(json_doc))

    def getDocValue(self, uuid):
        ## Get back the value of a jason document
        return  self.doGET( "/" + self.databese + "/" + uuid)

    #----------- DESINGN -----------------------

    def getDesign(self):
        ## A design
        uri_path = "/" + self.databese + "/_design/first_design/_view/all"
        return self.doGET(uri_path)


    def addDesign(self, json_doc):
        ## Insert a new design.
        uri_path = "/" + self.databese + "/_design/" + "first_design"
        return self.doPUT2(uri_path, json_doc)


    def addNamedDesign(self, name, json_doc):
        ## Insert a new design.
        uri_path = "/" + self.databese + "/_design/" + name
        return self.doPUT2(uri_path, json_doc)

    def getDesignCode(self, design_name):
        ## A design
        uri_path = "/" + self.databese + "/_design/" + design_name
        return self.doGET(uri_path)

    #------------------------- VIEWS ---------------------------

    def getTempView(self, json_doc):
        ## Get a teporary view
        uri_path = "/" + self.databese + "/_temp_view"
        return self.doPOST(uri_path, json_doc)


    def getNamedView(self, design_name, view_name):
        ## A design
        uri_path = "/" + self.databese + "/_design/" + design_name + "/_view/" + view_name
        return self.doGET(uri_path)
