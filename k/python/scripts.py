import hashlib

def getMD5Hash(x):
	return hashlib.md5(x).hexdigest();

def paperUri():
	return "person/"+getMD5Hash(getValue("authors")+getValue("title")+getValue("affiliation")+getValue("venue")+getValue("address")+getValue("publishers")+getValue("year")+getValue("pages"));