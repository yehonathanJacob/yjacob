package Q1;

public class Q1_2 {
    /**
     * @param sGroup is the SortedGroup to get value from
     * @param x is the parameter to compare value to
     * @param <T> the type of element comming back. Must extends Comparable<T>
     * @return an new SortedGroup with all T-objects in sGroup that are greater than x
     */
    public static <T extends Comparable<T>>  SortedGroup<T> reduce(SortedGroup<T> sGroup,T x){
        SortedGroup<T> new_sGroup = new SortedGroup<T>();
        int i = 0,size = sGroup.size();
        while(i<size){
            if (sGroup.get(i).compareTo(x)>0)
                break;
            i++;
        }
        while(i<size){
            new_sGroup.add(sGroup.get(i));
            i++;
        }
        return new_sGroup;
    }
}
