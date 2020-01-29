package Q2;

/**
 * parent SharedData  class, made to get, and move the data.
 */
public class SharedData {
    protected int x=0;//x value.
    protected int y=0;//y value.

    /**
     * standrat constructor
     * @param x set x value
     * @param y set y value
     */
    public SharedData(int x,int y){
        this.x = x;
        this.y = y;
    }

    /**
     * get the data
     * @return new objects type SharedData with filled data
     */
    public SharedData get(){
        System.out.printf("get: %s%n",this.toString());
        return (new SharedData(x,y));
    }

    /**
     * move the data
     * @param dx distance of x to move
     * @param dy distance of y to move
     */
    public void move(int dx, int dy){
        x += dx;
        y += dy;
        System.out.printf("move: %s%n",this.toString());
    }

    @Override
    public String toString(){return String.format("(%d,%d)",this.x,this.y);}
}
