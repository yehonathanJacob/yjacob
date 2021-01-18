select p.pname
from pilot as p, files as f, aircraft as ai
where p.pid = f.pid
	and f.ano = ai.ano
	and f.since <= 2012
	and ai.manufacturer = 'סוחוי'
	and not exist (
select *
from pilot as p1, flies as f1, aircraft as ai1
where p1.pid = p.pid
and f1.pid = p1.pid
and a1.ano = f1.ano
and a1.manufacturer = 'דיאמונד'
);