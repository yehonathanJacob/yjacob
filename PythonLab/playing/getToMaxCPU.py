from datetime import datetime
import multiprocessing


def worker(num, i):
	for j in range(i):
		num += j


def runAllProcess():
	num = 0
	jobs = []
	print(f'{datetime.now()}: Starting all process')
	for i in range(pow(10, 4)):
		p = multiprocessing.Process(target=worker, args=(num, i,))
		jobs.append(p)
		p.start()
	print(f'{datetime.now()}: All process runing')
	for p in jobs:
		p.join()
	print(f'{datetime.now()}: All process ended')


if __name__ == '__main__':
	runAllProcess()
