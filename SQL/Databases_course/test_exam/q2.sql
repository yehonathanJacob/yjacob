with sab_aircraft(ano, manufacturer, sno, ayear) as
	(select ano, manufacturer, sno, ayear
from aircraft
where manufacturer = 'סאב'
and ayear <= 2005)
select ai.ano
from pilot as p, files as f, sab_aircraft as ai
where p.pid = f.pid and f.ano = ai.ano
and having(count(distinct p.pid))<=all
(select count(distinct p1.pid)
from  pilot as p1, files as f1, sab_aircraft as ai1
where p1.pid = f1.pid and f1.ano = ai1.ano
group by ai.ano)
group by ai.ano;