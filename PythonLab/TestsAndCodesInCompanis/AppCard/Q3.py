# def numberGame(number):
#     number.sort()
#     while True:
#         i = checkTriple(number)
#         if i != -1:
#             x = number[i]
#             number.remove(x)
#             number.remove(x)
#             continue
#         else:
#             break
#     while True:
#         i = checkCouple(number, exclude=-1)
#         if i != -1:
#             num1 = number[i]
#             j = checkCouple(number, exclude=i)
#             if j != -1:
#                 num2 = number[j]
#             else:
#                 if i == 0:
#                     num2 = number[-1]
#                 else:
#                     num2 = number[0]
#             number.remove(num1)
#             number.remove(num2)
#             continue
#         else:
#             break
#     return len(number)
#
# def checkCouple(number,exclude=-1):
#     for i in range(len(number)-1):
#         if i != exclude and number[i] == number[i+1]:
#             return i
#     return -1
#
# def checkTriple(number):
#     for i in range(len(number)-2):
#         if number[i] == number[i+1] and number[i] == number[i+2]:
#             return i
#     return -1
########################################

def numberGame(number):
	number.sort()
	while True:
		i = checkTriple(number)
		if i != -1:
			x = number[i]
			number.remove(x)
			number.remove(x)
			continue
		else:
			break
	while True:
		i = checkCouple(number)
		if i != -1:
			num1 = number[i]
			number.remove(num1)
			j = checkCouple(number)
			if j != -1:
				num2 = number[j]
				number.remove(num2)
				special = checkCouple(number)
				if special != -1:
					num3 = number[special]
					number.remove(num3)

			else:
				if i == 0:
					num2 = number[-1]
				else:
					num2 = number[0]
				number.remove(num2)
			continue
		else:
			break
	return len(number)


def checkCouple(number):
	for i in range(len(number) - 1):
		if number[i] == number[i + 1]:
			return i
	return -1


def checkTriple(number):
	for i in range(len(number) - 2):
		if number[i] == number[i + 1] and number[i] == number[i + 2]:
			return i
	return -1


if __name__ == '__main__':
	print('d')
	cars_count = int(input())

	cars = []

	for _ in range(cars_count):
		cars_item = int(input())
		cars.append(cars_item)

	k = int(input())

	result = carParkingRoof(cars, k)

	print(str(result) + '\n')
