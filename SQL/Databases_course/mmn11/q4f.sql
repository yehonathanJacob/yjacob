select b.bid, b.bname
from branch as b, (select count(code) as number_of_product, bid
				   from stock
				   group by bid) as a
where a.bid = b.bid 
	and a.number_of_product = (select count(code) from product);
