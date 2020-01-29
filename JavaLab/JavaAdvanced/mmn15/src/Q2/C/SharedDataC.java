package Q2.C;
import Q2.SharedData;

/**
 * This is type of SharedData, that unable to fucntion works like this:
 * Permit 'get' to be performed any time 'move' dosn't work (moveLock = false).
 * Permit 'moev' to be performed only if 'get' dosn't work, and no secition of 'move' work (moveLock and getLock = false)
 */
public class SharedDataC extends SharedData {
    private boolean getLock = false; //Locker for get
    private boolean moveLock = false;//Locker for move

    public SharedDataC(int x,int y){
        super(x,y);
    }

    /**
     * 'get' can be performed only if move dosn't.
     * If it happend, get is getting lock too (so move wont start to work)
     * @return super of get
     */
    public synchronized SharedData get(){
        getLock = true;
        while (moveLock) {
            try {
                wait();
            }catch (InterruptedException e){ System.out.printf("Erorr: %s%n",e.getMessage());}
        }
        SharedData toReturn = super.get();
        getLock = false;
        notifyAll();
        return toReturn;
    }

    /**
     * 'move' can be performed, only in move+get dosn't work now.
     * If it happend, move is getting lock so not 'move' or 'get' will happend
     * @param dx distance of x to move
     * @param dy distance of y to move
     */
    public synchronized void move(int dx, int dy){
        while (getLock || moveLock) {
            try {
                wait();
            }catch (InterruptedException e){ System.out.printf("Erorr: %s%n",e.getMessage());}
        }
        moveLock = true;
        super.move(dx,dy);
        moveLock = false;
        notifyAll();
    }
}
