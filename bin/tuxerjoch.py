# -*- coding: utf-8 -*-
import restcouch

rc = restcouch.RestCouch()
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

respon = rc.createDB("test_db2")
print(respon.headers)
print(respon.text) # or r.json()
print( rc.getUUID() )

json_data = '{"title":"There is Nothing Left to Lose","artist":"Foo Fighters"}'
rc.insertDoc(json_data)

##print(resp)
#print(content)
