import urllib2
import urllib
import json

def getJson(url):
	res = urllib2.urlopen(url)
	return json.loads(res.read())
