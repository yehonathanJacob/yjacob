import copy


def sumObjects(*parms):
	if len(parms) > 0:
		res = copy.copy(parms[0])
		for obj in parms[1:]:
			res += obj
		return res
	else:
		return None
