package Q1;

public class moveInArr implements Runnable {
    protected ProcessArr arr;//The precess array
    protected int i;// index of this Thread in the array

    /**
     * this Thread is moving the value of arr[i] as refferance to his neighbors
     * @param array the array the world is in
     * @param index index of this Thread in the array
     */
    public moveInArr(ProcessArr array,int index)
    {
        arr = array;
        i = index;
    }

    @Override
    public void run(){
        int left_i = arr.getiLeft(i), right_i = arr.getiRight(i);
        int value = arr.get(i);
        if (value<arr.get(left_i) && value<arr.get(right_i))
            value +=1;
        else if ((value>arr.get(left_i) && value>arr.get(right_i)))
            value -=1;
        arr.finish(left_i);
        arr.finish(right_i);

        arr.waitFor(i);
        System.out.printf(i+": from: "+arr.get(i)+"to: "+value+"%n");
        arr.set(i,value);

    }
}
