with above_50(bid,rdate,rtime,number_of_supplier,total) as (
select re.bid, re.rdate, re.rtime, count(distinct pr.sid) as number_of_supplier, re.total
from receipt as re natural join purchase as pu, product as pr
where re.total > 50
and pu.code != (select code from product where pname ='prod1 n')
and pr.code = pu.code
group by re.bid, re.rdate, re.rtime)

select bid, rdate, rtime
from above_50
where number_of_supplier = (select min(number_of_supplier) from above_50);