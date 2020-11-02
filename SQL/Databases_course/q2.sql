create or replace function trigf1() returns trigger as $$
-- 	declare global variable
declare
	num_of_units integer = (select units from stock as st where st.code = new.code and st.bid = new.bid);
	price_per_item float = (select uprice from product as pr where pr.code = new.code);

-- function code
begin
	if (num_of_units < new.units)
	then
		raise notice 'Number of requested units is less than left';
		return null;
	else
		update stock
		set units = num_of_units - new.units
		where code = new.code and bid = new.bid;
		
		update receipt
		set total = total + (new.units * price_per_item)
		where rdate = new.rdate and bid = new.bid and rtime = new.rtime;
		
		return new;
	END IF;
end;

$$ LANGUAGE 'plpgsql';
create trigger T1
    before insert or update 
	on Purchase
    FOR EACH ROW
    EXECUTE PROCEDURE trigf1();
		
		
	