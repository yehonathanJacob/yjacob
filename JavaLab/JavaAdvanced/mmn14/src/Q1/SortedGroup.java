package Q1;

import java.util.ArrayList;
import java.util.Iterator;

/**
 * Represents a SortedGroup created by ArrayList
 *
 * @author Yehonathan Jacob
 * @version 08-05-2019
 */

public class SortedGroup <T extends Comparable<T>> extends ArrayList<T>{

    /**
     * Constructor for objects of class SortedGroup.
     */
    public SortedGroup(){
        super();
    }

    /**
     * adding new elemnt to SortedGroup
     * @param newElement the new elemnt to enter
     * @return return boolean value if able to return
     */
    public boolean add(T newElement){
        int size = this.size(), i =0;
        for (i=0;i<size;i++){
            if (this.get(i).compareTo(newElement) >= 0)
                break;
        }
        this.add(i,newElement);
        return true;
    }

    /**
     * removint elemnts equals to spesific elemnt.
     * @param element element to comper to
     * @return the number of elements removed.
     */
    public int remove(T element){
        int numOfRemove = 0;
        Iterator<T> iterator = this.iterator();
        T comper;
        ArrayList<T> elementToDelete = new ArrayList<T>();
        while (iterator.hasNext()){
            comper = iterator.next();
            if (comper.equals(element)){
                iterator.remove();
                numOfRemove++;
            }
        }
        return numOfRemove;
    }

    /**
     * This method the SortedGroup as Iterator
     * @return This SortedGroup as Iterator
     */
    public Iterator<T> iterator(){
        return super.iterator();
    }

    @Override
    public String toString() {
        String s = "[\n";
        for (int i=0;i<this.size();i++){
            s += this.get(i).toString() +",\n";
        }
        s+= "]";
        return s;
    }
}
