select b.bid, b.bname, max_total.total
from branch as b, (select bid, total
				   from receipt
				   where total = (select max(total) 
								  from receipt)) as max_total
where b.bid = max_total.bid;