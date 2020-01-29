/**
 * Segment2 represents a line (parallel to the x-axis) using a center point and length.
 *
 * @author Yehonathan Jacob
 * @version 23-04-2017
 */
public class Segment2
{
    // instance variables
    private Point _poCenter;//variable of the center point
    private double _length;//variable of the length of line
    
    //Constructors
    /**
     * Constructs a new segment using 4 specified x y coordinates: two coordinates for the left point and two coordinates for the right point. If the y coordinates are different, change the y of the right point to be equal to the y of the left point.
     * @param leftX - X value of left point
     * @param leftY - Y value of left point
     * @param rightX - X value of left point
     * @param rightY - Y value of left point
     */
    public Segment2 (double leftX ,double leftY ,double rightX ,double rightY)
    {
        _poCenter = new Point((leftX+rightX)/2,leftY);        
        _length = rightX - leftX;
    }
    /**
     * Constructs a new segment using a center point and the segment length.
     * @param poCenter - the Center Point
     * @param poCenter - the Center Point
     */
    public Segment2(Point poCenter, double length)
    {
        _poCenter = new Point(poCenter);
        _length = length;
    }
    /**
     * Constructs a new segment using two Points. If the y coordinates are different, change the y of the right point to be equal to the y of the left point.
     * @param left - the left point of the segment
     * @param right - the right point of the segment
     */
    public Segment2 (Point left, Point right)
    {
        _poCenter = new Point((left.getX() + right.getX())/2,left.getY());
        _length = right.getX() - left.getX();
    }
    
    /**
     * Copy Constructor. Construct a segment using a reference segment.
     * @param other - the reference segment
     */
    public Segment2 (Segment2 other)
    {
        _poCenter = new Point((other.getPoLeft().getX() + other.getPoRight().getX())/2, other.getPoLeft().getY());
        _length = other.getLength();
    }
    
    //methods Get:
    /**
     * Returns the left point of the segment.
     * @return The left point of the segment
     */
    public Point getPoLeft()
    {
        return new Point(_poCenter.getX() - 0.5 * _length , _poCenter.getY());
    }
    /**
     * Returns the rigth point of the segment.
     * @return The right point of the segment
     */
    public Point getPoRight()
    {
        return new Point(_poCenter.getX() + 0.5 * _length , _poCenter.getY());
    }
    /**
     * Returns the segment length.
     * @return The segment length
     */ 
    public double getLength()
    {
        return _length;
    }
    
    //other method
     /**
     * Return a string representation of this segment in the format (3.0,4.0)---(3.0,6.0).
     * @override toString in class java.lang.Object
     * @return String representation of this segment
     */
    public String toString()
    {
        return this.getPoLeft().toString() + "---" + this.getPoRight().toString();
    }
    /**
     * Check if the reference segment is equal to this segment.
     * @param other - the reference segment
     * @return True if the reference segment is equal to this segment
     */
    public boolean equals (Segment2 other)
    {
        return this.getPoLeft().equals(other.getPoLeft()) && this.getPoRight().equals(other.getPoRight());
    }
    /**
     * Check if this segment is above a reference segment.
     * @param other - the reference segment
     * @return True if this segment is above the reference segment
     */
    public boolean isAbove (Segment2 other)
    {
        return other.getPoLeft().getY() < this.getPoLeft().getY();
    }
    /**
     * Check if this segment is under a reference segment.
     * @param other - the reference segment
     * @return True if this segment is under the reference segment
     */
    public boolean isUnder (Segment2 other)
    {
        return other.isAbove(this);
    }
    /**
     * Check if this segment is left of a received segment.
     * @param other - the reference segment
     * @return True if this segment is left to the reference segment
     */
    public boolean isLeft (Segment2 other)
    {
        return this.getPoRight().getX() < other.getPoLeft().getX();
    }
    /**
     * Check if this segment is right of a received segment.
     * @param other - the reference segment
     * @return True if this segment is right to the reference segment
     */
    public boolean isRight (Segment2 other)
    {
        return this.getPoLeft().getX() > other.getPoRight().getX();
    }
    /**
     * Move the segment horizontally by delta.
     * @param delta - the displacement size
     */
    public void moveHorizontal (double delta)
    {
        Point left = new Point(this.getPoLeft());
        Point right = new Point(this.getPoRight());
        left.move(delta,0);
        right.move(delta,0);
        _poCenter = new Point((left.getX() + right.getX())/2,left.getY());
        _length = right.getX() - left.getX();
    }
    /**
     * Move the segment vertically by delta.
     * @param delta - the displacement size
     */
    public void moveVertical (double delta)
    {
        Point left = new Point(this.getPoLeft());
        Point right = new Point(this.getPoRight());
        left.move(0,delta);
        right.move(0,delta);
        _poCenter = new Point((left.getX() + right.getX())/2,left.getY());
        _length = right.getX() - left.getX();
    }
    /**
     * Change the segment size by moving the right point by delta. Will be implemented only for a valid delta: only if the new right point remains the right point.
     * @param delta - the length change
     */
    public void changeSize (double delta)
    {
        if(this.getPoRight().getX()+delta >= this.getPoLeft().getX())
        {
            Point left = new Point(this.getPoLeft());
            Point right = new Point(this.getPoRight());            
            right.move(delta,0);
            _poCenter = new Point((left.getX() + right.getX())/2,left.getY());
            _length = right.getX() - left.getX();
        }
    }
    /**
     * Check if a point is located on the segment.
     * @param p - a point to be checked
     * @return True if p is on this segment
     */
    public boolean pointOnSegment (Point p)
    {
        return p.getY() == this.getPoLeft().getY() && p.getX() >= this.getPoLeft().getX() && p.getX() <= this.getPoRight().getX();
    }
    /**
     * Check if this segment is bigger than a reference segment.
     * @param other - the reference segment
     * @return True if this segment is bigger than the reference segment
     */
    public boolean isBigger (Segment2 other)
    {
        return this.getLength() > other.getLength();
    }
    /**
     * Returns the overlap size of this segment and a reference segment.
     * @param other - the reference segment
     * @return The overlap size
     */
    public double overlap (Segment2 other)
    {
        if(other.getPoLeft().getX() > this.getPoRight().getX() || other.getPoRight().getX() < this.getPoLeft().getX())
            return 0;
        else
        {
            double L1 = this.getLength() + other.getLength();
            double L2 = Math.abs(this.getPoLeft().getX()-other.getPoLeft().getX());
            double L3 = Math.abs(this.getPoRight().getX()-other.getPoRight().getX());
            return (L1-L2-L3)/2;
        }
    }
    /**
     * Compute the trapeze perimeter, which is constructed by this segment and a reference segment.
     * @param other - the reference segment
     * @return The trapeze perimeter
     */
    public double trapezePerimeter (Segment2 other)
    {
        if(other.getPoLeft().getY() == this.getPoRight().getY())
            return 0;
        else
        {
            return this.getPoLeft().distance(other.getPoLeft()) + this.getPoRight().distance(other.getPoRight()) + this.getLength() + other.getLength();
        }
    }
}//end of class
