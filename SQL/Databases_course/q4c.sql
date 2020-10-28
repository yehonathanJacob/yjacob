select bid, rdate, rtime
from purchase
where units < 3
and date_part('month', now()) = extract(MONTH from(rdate))
and date_part('year', now()) = extract(YEAR from(rdate));