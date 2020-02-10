"""
examples:

python textToIp.py --ip 85.24.124.72
'01010101 00011000 01111100 01001000'

python textToIp.py --ip 172.31.37.72/20
From:  10101100 00011111 00100101 01001000
            172       31       37       72
To:    10101100 00011111 00101111 11111111
            172       31       47      255

To get ip range in linux:	ip addr show
"""
__author__ = "Yehonathan Jacob"
__date__ = "10/02/2020"
__email__ = "YehonathanJacob@gmail.com"

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ip','-i', help='Set ip as x.x.x.x/r')
args = parser.parse_args()
b_n = 8 # length of each int
ip_n = 32

def text_arr_to_ip_arr(text_arr,*args):
	return [format(int(__byte), *args).replace("0b","") for __byte in text_arr]

def text_to_ip(tx):
	if '/' in tx:
		ip,scope = tx.split('/')
	else:
		ip, scope = tx , False

	ipInts = ip.split('.')
	res = ""
	if scope:
		res += "From:  "
	start_ip = text_arr_to_ip_arr(ipInts,"#010b")
	res += " ".join(start_ip)
	if scope:
		res += "\n"+" "*7
		res += " ".join(text_arr_to_ip_arr(ipInts,"#8"))
		di = ip_n - int(scope) # delta i
		from_ip = "".join(start_ip)
		to_ip = from_ip[:-di] + "1"*di
		end_bin = [to_ip[i:i+b_n] for i in range(0,len(to_ip),b_n)]
		end_int = [int(b_ip,2) for b_ip in end_bin]
		res += "\nTo:    "
		res += " ".join(text_arr_to_ip_arr(end_int,"#010b"))
		res += "\n" + " " * 7
		res += " ".join(text_arr_to_ip_arr(end_int,"#8"))

	return res

if __name__ == '__main__':
	if args.ip:
		print(text_to_ip(args.ip))