import httplib, urllib
import json
import time

def sendData(conn, data):
   outdata = json.dumps(data)
   params = urllib.urlencode(data)
   headers = {"Content-type": "application/x-www-form-urlencoded",
              "Accept": "text/plain"}
   conn.request('POST','/data', params, headers)
   response  = conn.getresponse()
   print response.read()
   print response.status, response.reason
   
conn  = httplib.HTTPConnection('localhost:5000')
n = 1000
sleep = 0.05
totaltime = n * sleep
start = time.time()
for i in range(n):
   data = {'wavelength': 100+i,
          'channel': 1,
          }
   sendData(conn, data)
   time.sleep(sleep)
elapsed = time.time() - start
print "Expected:", totaltime
print "Elapsed :", elapsed
print "Difference:", elapsed - totaltime

