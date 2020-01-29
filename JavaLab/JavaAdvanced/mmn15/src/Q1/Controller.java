package Q1;

/**
 * Controller to control each number from gettting change not at the rite time
 */
public class Controller {
    private int numOfChecked;//number of checked has benn made
    private int valid;

    /**
     * constractor to reset the Controller
     * @param until
     */
    public Controller(int until){
        reset(until);
    }

    /**
     * this function reset the controller
     * @param until
     */
    public void reset(int until){
        numOfChecked = 0;
        valid = until;
    }

    /**
     * set a finish to one of the controller
     */
    public synchronized void finishCheck(){
        numOfChecked++;
        if (numOfChecked>=valid) notifyAll();
    }

    /**
     * fucntion that make a sleeping mode untill the controller is fully checked
     */
    public synchronized void waitForChecks(){
        while (numOfChecked<valid)
            try{
                wait();
            }catch (InterruptedException e){
                System.out.printf("interrupted while waiting%n");
            }
    }
    public int getCheck(){return numOfChecked;}
}
