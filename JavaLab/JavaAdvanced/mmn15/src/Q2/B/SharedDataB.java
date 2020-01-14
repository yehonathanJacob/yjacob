package Q2.B;

import Q2.SharedData;

/**
 * type of SharedData, that make the functionality so every time only one can happend. and after one is happend- second must be happend.
 */
public class SharedDataB extends SharedData {
    private boolean flag = true;// flag to presnet wich function is working now.

    public SharedDataB(int x,int y){
        super(x,y);
        flag = true;
    }

    /**
     * can be performed only at the beginning- and after a 'move' task.
     * @return return the super get.
     */
    public synchronized SharedData get(){
        while (flag) {
            try {
                wait();
            }catch (InterruptedException e){ System.out.printf("Erorr: %s%n",e.getMessage());}
        }
        SharedData toReturn = super.get();
        flag = !flag;
        notifyAll();
        return toReturn;
    }

    /**
     * can be performed only at the beginning- and after 'get' task
     * @param dx distance of x to move
     * @param dy distance of y to move
     */
    public synchronized void move(int dx, int dy){
        while (!flag) {
            try {
                wait();
            }catch (InterruptedException e){ System.out.printf("Erorr: %s%n",e.getMessage());}
        }
        super.move(dx,dy);
        flag = !flag;
        notifyAll();
    }
}
