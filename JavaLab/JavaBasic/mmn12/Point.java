/**
 * Represents 2 dimensional points.
 *
 * @author Yehonathan Jacob
 * @version 23-04-2017
 */
public class Point
{
    // instance variables
    private double _radius;//variable of distance of the vector
    private double _alpha;//variable of the angle of vector in degrees
    private final int DEFAULT_VAL = 0;
    
    //Constructors
    /**
     * Constructor for objects of class Point. Construct a new point with the specified x y coordinates. If the x coordinate is negative it is set to zero. If the y coordinate is negative it is set to zero.
     * @param x - The x coordinate
     * @param y - The y coordinate 
     */
    public Point(double x, double y)
    {
        toPolar(x,y);
    }
    /**
     * Constructor for objects of class Point. Copy constructor, construct a point using another point.
     * @param other - The point from which to construct the new object
     */
    public Point (Point other)
    {
        toPolar(other.getX(),other.getY());
    }
 
    //methods: Get
    /**
     * This method returns the x coordinate of the point.
     * @return The x coordinate of the point
     */
    public double getX()
    {
        return Math.round((_radius * Math.cos(_alpha*(Math.PI/180)))*10000)/(double)10000;
    }
    /**
     * This method returns the y coordinate of the point.
     * @return The y coordinate of the point
     */
    public double getY()
    {
        return Math.round((_radius * Math.sin(_alpha*(Math.PI/180)))*10000)/(double)10000;
    }
    
    //methods: Set
    /**
     * This method sets the x coordinate of the point. If the new x coordinate is negative the old x coordinate will remain unchanged.
     * @param x - The new x coordinate
     */
    public void setX(double x)
    {
        if(x>=0)
        {
            toPolar(x,getY());
        }
    }
    /**
     * This method sets the y coordinate of the point. If the new y coordinate is negative the old y coordinate will remain unchanged.
     * @param y - The new y coordinate
     */
    public void setY(double y)
    {
        if(y>=0)
        {
            toPolar(getX(),y);
        }
    }
    
    //other method
    /**
     * Returns a string representation of Point in the format (x,y).
     * @override toString in class java.lang.Object
     * @return A String representation of the Point
     */
    public String toString()
    {
        return "("+getX()+","+getY()+")";
    }
    /**
     * Check if the given point is equal to this point.
     * @param other - The point to check equality with
     * @return True if the given point is equal to this point
     */
    public boolean equals (Point  other)
    {
        return (other.getX() == this.getX())&&(other.getY() == this.getY());
    }
    /**
     * Check if this point is above a received point.
     * @param other - The point to check if this point is above
     * @return True if this point is above the other point
     */
    public boolean isAbove (Point other)
    {
        return other.getY()<this.getY();
    }
    /**
     * Check if this point is below a received point.
     * @param other - The point to check if this point is below
     * @return True if this point is below the other point
     */
    public boolean isUnder (Point other)
    {
        return other.isAbove(this);
    }
    /**
     * Check if this point is left of a received point.
     * @param other - The point to check if this point is left of
     * @return True if this point is left of the other point
     */
    public boolean isLeft (Point other)
    {
        return other.getX()>this.getX();
    }
    /**
     * Check if this point is right of a received point.
     * @param other - The point to check if this point is right of
     * @return True if this point is right of the other point
     */
    public boolean isRight (Point other)
    {
        return other.isLeft(this);
    }
    /**
     * Check the distance between this point and a given point.
     * @param other - The point to check the distance from
     * @return The distance
     */
    public double distance (Point p)
    {
       return Math.sqrt((Math.pow(this.getX()-p.getX(),2))+(Math.pow(this.getY()-p.getY(),2)));
    }
    /**
     * Moves a point.
     * @param dx - The difference to add to x
     * @param dy - The difference to add to y
     */
    public void move (double dx, double dy)
    {
       if(getX() + dx >= 0 && getY() + dy >=0)
       {
           toPolar(getX() + dx,getY() + dy);
       }
    }
    
    //private method
    private void toPolar(double x,double y)
    {
        if(x<=0 || y<=0)
        {
            if(x<=0)
            {
                _alpha = 90;
                if (y<=0)
                {
                    _radius=0;
                }else
                {
                    _radius = y;
                }
            }else{
                _alpha = 0;
                _radius = x;
            }
        }else
        {
            _alpha = Math.atan(y/x) * (180/Math.PI);
            _alpha = Math.round(_alpha*10000)/(double)10000;
            _radius = Math.sqrt(Math.pow(x,2)+Math.pow(y,2));
            _radius = Math.round(_radius*10000)/(double)10000;
        }
    }
}//end of class
