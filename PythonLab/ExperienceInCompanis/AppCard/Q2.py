def carParkingRoof(cars, k):
	ls = cars.copy()
	ls.sort()
	minRoof = ls[-1] - ls[0] + 1 if len(ls) < k else ls[k - 1] - ls[0] + 1
	for i in range(k - 1, len(ls)):
		roof = ls[i] - ls[i - k + 1] + 1
		minRoof = min(minRoof, roof)
	return minRoof
	# Write your code here


if __name__ == '__main__':

	cars_count = int(input())

	cars = []

	for _ in range(cars_count):
		cars_item = int(input())
		cars.append(cars_item)

	k = int(input())

	result = carParkingRoof(cars, k)

	print(str(result) + '\n')
