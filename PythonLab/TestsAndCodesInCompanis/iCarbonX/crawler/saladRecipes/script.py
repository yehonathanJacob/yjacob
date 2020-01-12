import json
import codecs

A = []
B = []


def step3_addResepiseList(resepis):
	for ps in resepis:
		if "לט" in ps['name'] or "salad" in ps['name']:
			B.append(ps)
			if len(ps['img']) > 0:
				A.append(ps)
	addA(A)
	addB(B)


def addAllresepis(resepis):
	splitResepis(resepis)
	addA(A)
	addB(B)


def splitResepis(resepis):
	for ps in resepis:
		B.append(ps)
		if len(ps['img']) > 0:
			A.append(ps)


def addA(newA):
	old = getA()
	for r in newA:
		old.append(r)
	newRes = json.dumps(old, ensure_ascii=False)
	with open('A.json', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()


def addB(newB):
	old = getB()
	for r in newB:
		old.append(r)
	newRes = json.dumps(old, ensure_ascii=False)
	with open('B.json', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()


def getA():
	f = codecs.open("A.json", "a+", "utf-8")
	f.seek(0, 0)
	old = f.read()
	f.close()
	if len(old) > 0:
		old = json.loads(old)
	else:
		old = []
	return old


def getB():
	f = codecs.open("B.json", "a+", "utf-8")
	f.seek(0, 0)
	old = f.read()
	f.close()
	if len(old) > 0:
		old = json.loads(old)
	else:
		old = []
	return old
