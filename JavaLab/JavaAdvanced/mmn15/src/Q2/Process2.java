package Q2;

/**
 * Process that get 10 time the object referance to SharedData.
 * @param <T> The object must be a referance of SharedData.
 */
public class Process2 <T extends SharedData> extends Thread{
    private T sd;//the object to work on.

    /**
     * standart constructor that get an object referance to a SharedData
     * @param sd
     */
    public Process2(T sd){this.sd = sd;}

    @Override
    public void run() {
        SharedData temp;
        for (int i = 0; i < 10; i++)
        {
            temp = sd.get();
            //System.out.printf("P2: get: %s%n",temp.toString());
            try {
                Thread.sleep((int)(Math.random()*1000));
            }catch (InterruptedException e){System.out.printf("Erorr in P2: %s%n",e.getMessage());}
        }
    }
}
