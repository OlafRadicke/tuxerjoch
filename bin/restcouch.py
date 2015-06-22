
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
        return requests.get(requeststring, auth=(self.user, self.password))

    def doPUT(self, uir_path):
    ##
    # A PUT-Request
    # @param uir_path the uri path

        requeststring = "http://" + self.uri_host + ":" + self.uri_port + uir_path
        print(requeststring)
        return requests.put(requeststring, auth=('olaf', 'olaf'))

    def doPUT2(self, uir_path, json_doc):
    ##
    # A PUT-Request
    # @param uir_path the uri path
    # @param json_doc a json document

        requeststring = "http://" + self.uri_host + ":" + self.uri_port + uir_path
        print(requeststring)
        print(json_doc)
        return requests.put(requeststring, auth=(self.user, self.password), data=json_doc)


    def createDB(self, db_name):
    ##
    #    Creates a new data base.
    #    @param db_name name of the new database

        return self.doPUT("/" + db_name)

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
