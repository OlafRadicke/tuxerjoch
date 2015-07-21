TUXERJOCH
=========

Source code / website:
https://github.com/OlafRadicke/tuxerjoch

# Project mission #

TUXERJOCH is only a proof of concept.


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

## RPM repo ##

under [rpm.the-independent-friend.de](https://rpm.the-independent-friend.de/)
you can find ready complied rpms.

# Configuration #

You are need a configuration file with name ./tuxerjoch.conf in the working
directory or under /etc/ with this content:

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
and host name configuration where  tuxerjoch service is listening. The
**"log_level"** can have the value:

* DEBUG
* INFO
* ERROR


The fresh installed system have the default password "tuxerjoch". After the
first login you can and need to change this. Click on "Einstellung" in
top of the page to change this.

## Password reset ##

If you forgot your password then you can delete the document "global_config" in
the CouchDB and restart the application. After then the default password
"tuxerjoch" is recovered. You can use the webinterface of couchDB to delete
easily the document "global_config". Call url
[http://127.0.0.1:5984/_utils/](http://127.0.0.1:5984/_utils/) in your Browser.

# CouchDB with docker #

If you like using docker for CouchDB then check this:

> docker pull fedora/couchdb

# Externe Dokus #
* **CouchDB-REST-API:** http://docs.couchdb.org/en/latest/api/index.html
* **CouchDB-REST-API views:** https://wiki.apache.org/couchdb/HTTP_view_API
* **python3-requests lib:** http://www.pythonforbeginners.com/requests/using-requests-in-python
* **Bottle-Docu:** http://bottlepy.org/docs/dev/tutorial.html

# Dodos #

## attachment ##

http://docs.couchdb.org/en/latest/api/document/attachments.html

## Dump function ##

For backups

## RSS feeds ##

Coming soon

# Picture resources #

The alpen picture is form
[commons.wikimedia.org](https://commons.wikimedia.org/wiki/File:Kronplatz_Nordf%C3%B6hn04_2013-01-08.jpg)
The origin file is licensed under the Creative Commons Attribution-Share Alike
3.0 Unported license.

# The name TUXERJOCH #

why the name TUXERJOCH? Well I was looking for neutral name, but I had no
ideas. So I used the random function of German Wikipedia and get this name.

https://en.wikipedia.org/wiki/Tuxer_Joch
