import urllib2
import urllib
import json
from util import *
def readField(query):
	examples = []
	pos = set()
	with open(query+".txt") as fin:
		for line in fin:
			(score, aid, name) = line.split('\t')
			score = int(score)
			aid = int(aid)
			examples.append((score, aid))
			pos.add(aid)
	res = getJson("http://arnetminer.org/services/search-expert?u=npbool&num=%d&q=%s"%
								 (len(examples)*2, urllib.quote(query)))

	for p in res["Results"]:
		if not p["Id"] in pos:
			examples.append(p["Id"])

	return examples

data = []

queries = ["data mining","multimedia","human computer interaction","high performance computing"]

def readData():
	for query in queries:
		examples = readField(query)
		data.append(examples)

def split(va_index):
	valid = []
	train = []
	for i in len(data):
		if i==va_index:
			valid = data[i]
		else:
			train.extend(data[i])
	return (train,valid)

def getRelatedConf(query):
	res = getJson("http://arnetminer.org/services/search-conference?u=npbool&q=%s&num=30"%urllib.quote(query))
	conf_id_list = ""

	for conf in res["Results"]:
		if conf_id_list=="":
			conf_id_list+=str(conf["Id"])
		else:
			conf_id_list+=","+str(conf["Id"])

	res = getJson("http://arnetminer.org/services/jconf/%s?u=npbool"%conf_id_list)
	conf_rank = [(conf["Id"], conf["Score"], conf["Name"]) for conf in res]
	conf_rank.sort(key = lambda c:-c[1])
	return conf_rank[:8]

if __name__=="__main__":
	getRelatedConf("multimedia")