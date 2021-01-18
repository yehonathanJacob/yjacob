select t.sid, s.sname, t.pname_1
from (select sid, count(code) as num_sid, max(pname) as pname_1
		from product
		group by sid) as t,
	supplier as s
where s.sid = t.sid and t.num_sid = 1;
