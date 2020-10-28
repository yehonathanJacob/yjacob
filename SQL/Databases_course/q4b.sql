select pd.pname, sp.sname
from product as pd, supplier as sp
where pd.sid = sp.sid and pd.utype = 'kilo' and pd.uprice>15;