/**
 * Segment1 represents a line (parallel to the x-axis) using two Points..
 *
 * @author Yehonathan Jacob
 * @version 23-04-2017
 */
public class Segment1
{
    // instance variables
    private Point _poLeft;//variable of the left point
    private Point _poRight;//variable of the right point
    
    //Constructors
    /**
     * Constructs a new segment using two Points. If the y coordinates are different, change the y of the right point to be equal to the y of the left point.
     * @param left - the left point of the segment
     * @param right - the right point of the segment
     */
    public Segment1 (Point left, Point right)
    {
        _poLeft = new Point(left);
        if(left.getY() == right.getY())
        {
            _poRight = new Point(right);
        }
        else
        {
            _poRight = new Point(right.getX(),left.getY());
        }
    }
    /**
     * Constructs a new segment using 4 specified x y coordinates: Two coordinates for the left point and two coordinates for the right point. If the y coordinates are different, change the y of the right point to be equal to the y of the left point.
     * @param leftX - X value of left point
     * @param leftY - Y value of left point
     * @param rightX - X value of left point
     * @param rightY - Y value of left point
     */
    public Segment1 (double leftX ,double leftY ,double rightX ,double rightY)
    {
        _poLeft = new Point(leftX,leftY);
        _poRight = new Point(rightX,leftY);
    }
    /**
     * Copy Constructor. Construct a segment using a reference segment.
     * @param other - the reference segment
     */
    public Segment1 (Segment1 other)
    {
        _poLeft = new Point(other.getPoLeft());
        _poRight = new Point(other.getPoRight());
    }
    
    //methods Get:
    /**
     * Returns the left point of the segment.
     * @return The left point of the segment
     */
    public Point getPoLeft()
    {
        return _poLeft;
    }
    /**
     * Returns the rigth point of the segment.
     * @return The right point of the segment
     */
    public Point getPoRight()
    {
        return _poRight;
    }
    /**
     * Returns the segment length.
     * @return The segment length
     */ 
    public double getLength()
    {
        return _poRight.getX() - _poLeft.getX();
    }
    
    //other method
     /**
     * Return a string representation of this segment in the format (3.0,4.0)---(3.0,6.0).
     * @override toString in class java.lang.Object
     * @return String representation of this segment
     */
    public String toString()
    {
        return _poLeft.toString() + "---" + _poRight.toString();
    }
    /**
     * Check if the reference segment is equal to this segment.
     * @param other - the reference segment
     * @return True if the reference segment is equal to this segment
     */
    public boolean equals (Segment1 other)
    {
        return _poLeft.equals(other.getPoLeft()) && _poRight.equals(other.getPoRight());
    }
    /**
     * Check if this segment is above a reference segment.
     * @param other - the reference segment
     * @return True if this segment is above the reference segment
     */
    public boolean isAbove (Segment1 other)
    {
        return other.getPoLeft().getY() < this.getPoLeft().getY();
    }
    /**
     * Check if this segment is under a reference segment.
     * @param other - the reference segment
     * @return True if this segment is under the reference segment
     */
    public boolean isUnder (Segment1 other)
    {
        return other.isAbove(this);
    }
    /**
     * Check if this segment is left of a received segment.
     * @param other - the reference segment
     * @return True if this segment is left to the reference segment
     */
    public boolean isLeft (Segment1 other)
    {
        return this.getPoRight().getX() < other.getPoLeft().getX();
    }
    /**
     * Check if this segment is right of a received segment.
     * @param other - the reference segment
     * @return True if this segment is right to the reference segment
     */
    public boolean isRight (Segment1 other)
    {
        return this.getPoLeft().getX() > other.getPoRight().getX();
    }
    /**
     * Move the segment horizontally by delta.
     * @param delta - the displacement size
     */
    public void moveHorizontal (double delta)
    {
        _poLeft.move(delta,0);
        _poRight.move(delta,0);
    }
    /**
     * Move the segment vertically by delta.
     * @param delta - the displacement size
     */
    public void moveVertical (double delta)
    {
        _poLeft.move(0,delta);
        _poRight.move(0,delta);
    }
    /**
     * Change the segment size by moving the right point by delta. Will be implemented only for a valid delta: only if the new right point remains the right point.
     * @param delta - the length change
     */
    public void changeSize (double delta)
    {
        if(_poRight.getX()+delta >= _poLeft.getX())
        {
            _poRight.move(delta,0);
        }
    }
    /**
     * Check if a point is located on the segment.
     * @param p - a point to be checked
     * @return True if p is on this segment
     */
    public boolean pointOnSegment (Point p)
    {
        return p.getY() == _poLeft.getY() && p.getX() >= _poLeft.getX() && p.getX() <= _poRight.getX();
    }
    /**
     * Check if this segment is bigger than a reference segment.
     * @param other - the reference segment
     * @return True if this segment is bigger than the reference segment
     */
    public boolean isBigger (Segment1 other)
    {
        return this.getLength() > other.getLength();
    }
    /**
     * Returns the overlap size of this segment and a reference segment.
     * @param other - the reference segment
     * @return The overlap size
     */
    public double overlap (Segment1 other)
    {
        if(other.getPoLeft().getX() > _poRight.getX() || other.getPoRight().getX() < _poLeft.getX())
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
    public double trapezePerimeter (Segment1 other)
    {
        if(other.getPoLeft().getY() == _poRight.getY())
            return 0;
        else
        {
            return _poLeft.distance(other.getPoLeft()) + _poRight.distance(other.getPoRight()) + this.getLength() + other.getLength();
        }
    }
}//end of class
