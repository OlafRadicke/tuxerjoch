
import httplib2
import requests
import json


class RestCouch:
##
#   A wrapper class for the rest api of couchdb

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

    def doGET(self, uir_path):
    ##
    # A GET-Request
    # @param uir_path the uri path

        #h = httplib2.Http(".cache")
        h = httplib2.Http()
        return h.request("http://" + self.uri_host + ":" + self.uri_port + uir_path, "GET")


    def doGET2(self, uir_path):
    ##
    # A GET-Request
    # @param uir_path the uri path
        requeststring = "http://" + self.uri_host + ":" + self.uri_port + uir_path
        print(requeststring)
        headers = {'content-type': 'application/json'}
        return requests.get(requeststring, auth=(self.user, self.password), headers=headers)

    def doPUT(self, uir_path):
    ##
    # A PUT-Request
    # @param uir_path the uri path

        requeststring = "http://" + self.uri_host + ":" + self.uri_port + uir_path
        print(requeststring)
        return requests.put(requeststring, auth=(self.user, self.password))

    def doPUT2(self, uir_path, json_doc):
    ##
    # A PUT-Request
    # @param uir_path the uri path
    # @param json_doc a json document

        requeststring = "http://" + self.uri_host + ":" + self.uri_port + uir_path
        print(requeststring)
        print(json_doc)
        return requests.put(requeststring, auth=(self.user, self.password), data=json_doc)

    def doDELETE(self, uir_path):
    ##
    # A DELETE-Request
    # @param uir_path the uri path

        requeststring = "http://" + self.uri_host + ":" + self.uri_port + uir_path
        print(requeststring)
        return requests.delete(requeststring, auth=(self.user, self.password))

    def doPOST(self, uir_path, json_doc):
    ##
    # A Post-Request
    # @param uir_path the uri path
    # @param json_doc a json document

        requeststring = "http://" + self.uri_host + ":" + self.uri_port + uir_path
        print(requeststring)
        print(json_doc)
        return requests.post(requeststring, auth=(self.user, self.password), data=json_doc)


    def createDB(self, db_name):
    ##
    #    Creates a new data base.
    #    @param db_name name of the new database

        return self.doPUT("/" + db_name)


    def deleteDB(self, db_name):
    ##
    #    Delete a data base.
    #    @param db_name name of the database

        return self.doDELETE("/" + db_name)

    def getAllDBs(self):
        ##
        # Get all databes names

        uri_path = "/_all_dbs"
        return self.doGET2(uri_path)



    def getUUID(self):
        ##
        # Get bback a UUID as string
        respon = self.doGET2("/_uuids")
        return json.loads(respon.text)["uuids"][0]

    def insertDoc(self, json_doc):
        ##
        # Insert a json document in a database.
        uri_path = "/" + self.databese + "/" + self.getUUID()
        return self.doPUT2(uri_path, json_doc)

    def insertNamedDoc(self, name, json_doc):
        ##
        # Insert a named json document in a database.
        uri_path = "/" + self.databese + "/" + name
        return self.doPUT2(uri_path, json_doc)


    def getAllDocs(self):
        ##
        # Get all documents

        uri_path = "/" + self.databese + "/_all_docs"
        return self.doGET2(uri_path)


    def searchDocs(self, json_doc):
        ##
        # Search docomens with keys
        # @param json_doc json with search keys

        ##
        # Insert a json document in a database.
        uri_path = "/" + self.databese + "/_all_docs"
        return self.doPOST(uri_path, json_doc)

    def getDocValue(self, uuid):
        ##
        # Get back the value of a jason document
        return  self.doGET2( "/" + self.databese + "/" + uuid)

    def getDesign(self):
        ## A design
        uri_path = "/" + self.databese + "/_design/first_design/_view/all"
        return self.doGET2(uri_path)

    def getNamedDesign(self, design_name):
        ## A design
        uri_path = "/" + self.databese + "/_design/first_design/_view/" + design_name
        return self.doGET2(uri_path)

    def addDesign(self, json_doc):
        ##
        # Insert a new design.
        uri_path = "/" + self.databese + "/_design/" + "first_design"
        print(json_doc)
        return self.doPUT2(uri_path, json_doc)

