package Q1;

/**
 * create an array of number and contoroller (referance to each other) and make sure a number cen be change only he was twise checked.
 */
public class ProcessArr {
    private final int NUM_OF_CHECK = 2;
    private int[] numbersArr;
    private Controller[] ConArr;

    public ProcessArr(int n){
        numbersArr = new int[n];
        ConArr = new Controller[n];
        for (int i=0;i<n;i++)
        {
            numbersArr[i] = (int)(Math.random()*100);
            ConArr[i] = new Controller(NUM_OF_CHECK);
        }
    }

    public void resetController(){
        for (Controller c:ConArr)
            c.reset(NUM_OF_CHECK);
    }

    public void waitFor(int i){
        ConArr[i].waitForChecks();
    }

    public void finish(int i){
        ConArr[i].finishCheck();
    }

    public int getiLeft(int i){
        return (i==0)? numbersArr.length-1:i-1;
    }

    public int getiRight(int i){
        return (i == numbersArr.length-1)? 0:i+1;
    }

    public int get(int i){
        return numbersArr[i];
    }
    public void set(int i,int value){
        numbersArr[i]=value;
    }

    @Override
    public String toString(){
        String status = "[";
        for (int i=0;i<numbersArr.length;i++)
            status += " "+numbersArr[i] +",";
        status = status.substring(0,status.length() -1);
        return status+"]";
    }

}
