package Q1;
import java.util.Arrays;

public class Person implements Comparable<Person> {
    /**
     *  instance variables
     */
    private int height;
    private String name;
    private short[] id;

    /**
     * Person constractor
     * @param nHeight height in cm of person
     * @param nName name as String of person
     * @param nId Array of number to present id.
     */
    public Person(int nHeight,String nName,short[] nId){
        height = nHeight;
        name = nName;
        id = new short[nId.length];
        for (int i=0;i<id.length;i++){
            id[i] = nId[i];
        }
    }

    /**
     * Person constractor
     * @param nHeight height in cm of person
     * @param nName name as String of person
     * @param nId String of id.
     */
    public Person(int nHeight,String nName, String nId){
        height = nHeight;
        name = nName;
        id = new short[nId.length()];
        for (int i=0;i<id.length;i++){
            id[i] = Short.parseShort(nId.charAt(i)+"");
        }
    }

    @Override
    public int compareTo(Person o) {
        if (this.height < o.height)
            return -1;
        return (this.height == o.height)? 0 : 1;
    }

    @Override
    public String toString(){
        String sId = "";
        for (int i=0;i<id.length;i++){
            sId += ((Short)(id[i])).toString();
        }
        return String.format("{Height: %dcm\tID: %s\tName: %s\t}",height,sId,name);
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof Person){
            Person p = (Person)(obj);
            return (p.height == this.height && Arrays.equals(p.id,this.id) && p.name == this.name);
        }
        return super.equals(obj);
    }
}
