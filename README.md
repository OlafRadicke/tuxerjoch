TUXERJOCH
---------

Source code / website:
https://github.com/OlafRadicke/tuxerjoch


# Dependencies #

* python3
* python3-requests
* python3-bottle
* python3-simplejson
* python3-cherrypy

# (pre) install #

## Build a rpm ##

For installation over rpm you can build a rpm with this command:

```
> rpmbuild -bb ./tuxerjoch.spec
```

# Configuration #

there is a configuration file with name ./tuxerjoch.conf

```
 {
     "couch_host": "127.0.0.1",
     "couch_port": "5984",
     "couch_user": "admin",
     "couch_passwd": "admin",
     "couch_db": "tuxerjoch",
     "webservice_host": "127.0.0.1",
     "webservice_port": "8080",
     "log_file": "tuxerjoch.log",
     "log_level": "DEBUG"
 }
```

**"couch_*"** is the couch db configuration. **"webservice_*"** is port
and host ware tuxerjoch is listening. **"log_level"** can have the value:

* DEBUG
* INFO
* ERROR

The fresh installed system have the default password "tuxerjoch". After the
first login you can and need to change this. Click on "Einstellung" in top.

If you forgot your password then you can delete the document "global_config" in
the CouchDB and restart the application. After then the default password is
recovered. You can use the webinterface of couchDB easily. Call
http://localhost:5984/ in your Browser.

# CouchDB with docker #

If you like using docker for CouchDB then do this:

> docker pull fedora/couchdb

# Externe Dokus #
## CouchDB-REST-API ##

http://docs.couchdb.org/en/latest/api/index.html

## CouchDB-REST-API views ##
https://wiki.apache.org/couchdb/HTTP_view_API

## python3-requests ##

http://www.pythonforbeginners.com/requests/using-requests-in-python

## Bottle-Docu ##

http://bottlepy.org/docs/dev/tutorial.html

# Dodos #

## attachment ##

http://docs.couchdb.org/en/latest/api/document/attachments.html

# Picture resources #

The alpen picture is form
https://commons.wikimedia.org/wiki/File:Kronplatz_Nordf%C3%B6hn04_2013-01-08.jpg
The origin file is licensed under the Creative Commons Attribution-Share Alike
3.0 Unported license.

# The name TUXERJOCH #

why the name TUXERJOCH? Well I was looking for neutral name, but I had no
ideas. So I used the random function of German Wikipedia and get this name.

https://en.wikipedia.org/wiki/Tuxer_Joch
