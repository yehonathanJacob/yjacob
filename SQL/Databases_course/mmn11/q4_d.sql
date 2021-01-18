-- delete from purchase;
-- delete from receipt;
-- delete from stock;
-- delete from supplier;
-- delete from branch;
-- delete from product;

-- select bid, rdate, rtime
-- from purchase
-- where units < 3
-- and date_part('month', now()) = extract(MONTH from(rdate))
-- and date_part('year', now()) = extract(YEAR from(rdate));

select count(code) as num_sid, sid
from product
group by sid
where num_sid=1;