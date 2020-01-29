package Q2;

/**
 * Process that move 10 time the object referance to SharedData.
 * @param <T> The object must be a referance of SharedData.
 */
public class Process1 <T extends SharedData> extends Thread{
    private T sd;//the object to work on.

    /**
     * standart constructor that get an object referance to a SharedData
     * @param sd
     */
    public Process1(T sd){this.sd = sd;}

    @Override
    public void run() {
        int x,y;
        for (int i = 0; i < 10; i++)
        {
            x = (int)(Math.random()*100);
            y = (int)(Math.random()*100);
            sd.move(x,y);
            try {
                Thread.sleep((int)(Math.random()*1000));
            }catch (InterruptedException e){System.out.printf("Erorr int P1: %s%n",e.getMessage());}
        }
    }
}
