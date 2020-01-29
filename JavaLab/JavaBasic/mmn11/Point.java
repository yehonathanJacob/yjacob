
/**
 * Write a description of class Point here.
 *
 * @author Yehonathan Jacov
 * @version 1
 * @date 23/04/2017
 */
public class Point
{
    // instance variables - replace the example below with your own
    public int x = 0;

    /**
     * Constructor for objects of class Point
     */
    public Point()
    {
        // initialise instance variables
        x = 1;
    }
    
    public String toString()
    {
        return x+"";
    }
    
    public int GetX(){
        return x;
    }

    /**
     * An example of a method - replace this comment with your own
     *
     * @param  y  a sample parameter for a method
     * @return    the sum of x and y
     */
    public int sampleMethod(int y)
    {
        // put your code here
        return x + y;
    }
}
