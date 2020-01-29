package Q2;

import java.io.Serializable;
import java.time.Year;
import java.util.*;
import java.util.HashMap;
import java.util.Hashtable;

public class Q2_Date implements Serializable {
    /**
     * instans variable
     */
    private int day;
    private int month;
    private int year;
    public enum  Months{ January,February,March,April,May,June,July,August,September,October,November,December}
    public HashMap<Integer,String> MonthsName = new HashMap<Integer, String>();

    public Q2_Date(int Day, int Month,int Year){
        create_MonthsName();
        day = Day;
        month = Month;
        year = Year;
    }
    public Q2_Date(){
        create_MonthsName();
        Date date = new Date();
        Calendar calendar = new GregorianCalendar();
        calendar.setTime(date);
        year = calendar.get(Calendar.YEAR);
        month = calendar.get(Calendar.MONTH);
        day = calendar.get(Calendar.DAY_OF_MONTH);
    }
    public Q2_Date(Q2_Date OldDate){
        this(OldDate.day, OldDate.month ,OldDate.year);
    }

    private void create_MonthsName(){
        MonthsName.put(0,"January");
        MonthsName.put(1,"February");
        MonthsName.put(2,"March");
        MonthsName.put(3,"April");
        MonthsName.put(4,"May");
        MonthsName.put(5,"June");
        MonthsName.put(6,"July");
        MonthsName.put(7,"August");
        MonthsName.put(8,"September");
        MonthsName.put(9,"October");
        MonthsName.put(10,"November");
        MonthsName.put(11,"December");
    }

    @Override
    public String toString() {
        return String.format("%d/%s/%d",day,MonthsName.get(month),year);
    }

    @Override
    public int hashCode() {
        return year*10000 + month*100+day;
    }

    @Override
    public boolean equals(Object obj) {
        if(obj instanceof Q2_Date){
            Q2_Date dToComp = (Q2_Date)(obj);
            return (dToComp.day == this.day && dToComp.month == this.month && dToComp.year == this.year);
        }
        return super.equals(obj);
    }

    /**
     * Get and Set function:
     */
    public int getYear(){return year;}
    public void setYear(int Year){ year = Year;}

    public int getMonth(){return month;}
    public void setMonth(int Month){month = Month;}

    public int getDay(){return day;}
    public void setDay(int Day){day = Day;}
}
