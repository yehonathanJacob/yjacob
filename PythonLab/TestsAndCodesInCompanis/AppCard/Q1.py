import datetime
import calendar

import requests


def add_months(sourcedate, months):
	month = sourcedate.month - 1 + months
	year = sourcedate.year + month // 12
	month = month % 12 + 1
	day = min(sourcedate.day, calendar.monthrange(year, month)[1])
	return datetime.date(year, month, day)


def getUserTransaction(uid, txnType, monthYear):
	start = datetime.datetime.strptime(monthYear, '%m-%Y')
	end = add_months(start, 1)
	start_it = start.timestamp()  # calendar.timegm(start.timetuple())
	end_it = calendar.timegm(end.timetuple())
	baseUrl = f'https://jsonmock.hackerrank.com/api/transactions/search?txnType={txnType}&userId={uid}&monthYear={monthYear}'
	r = requests.get(baseUrl)
	beginData = r.json()
	NumOfPages = beginData['total_pages']
	dicAmount = {}
	for i in range(1, NumOfPages + 1):
		url = baseUrl + '&page={}'.format(i)
		r = requests.get(url)
		for data in r.json()['data']:
			time = data['timestamp']
			while time >= pow(10, 10):
				time = time / 10
			if time >= start_it and time < end_it:
				id = data['id']
				amountSt = data['amount'].replace(',', '').replace("$", "")
				amount = float(amountSt)
				dicAmount[id] = amount
	averageNum = Average(dicAmount.values())
	res = []
	for k, v in dicAmount.items():
		if v > averageNum:
			res.append(k)
	res.sort()
	return res


def Average(lst):
	return sum(lst) / len(lst)


if __name__ == '__main__':
	uid = int(input().strip())

	txnType = input()

	monthYear = input()

	result = getUserTransaction(uid, txnType, monthYear)

	print('\n'.join(map(str, result)))
