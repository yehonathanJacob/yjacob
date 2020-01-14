/**
 * Represents Node of 2 dimensional points.
 *
 * @author Yehonathan Jacob
 * @version 18/06/2017
 */
public class PointNode
{
    private Point _point;//point value
    private PointNode _next;//next value
    
    //Constructors
    /**
     * Constructor for PointNode object
     * @parm p - the value of the object
     */
    public PointNode(Point p)
    {
        _point = new Point(p);
        _next = null;
    }
    /**
     * Constractor for PointNode object
     * @parm p - the value of the object
     * @parm n - the next object
     */
    public PointNode(Point p, PointNode n)
    {
        _point = new Point(p);
        _next = n;
    }
    /**
     * Constractor for PointNode object
     * @parm p - the object
     */
    public PointNode(PointNode p)
    {
        _point = p.getPoint();
        _next = p.getNext();
    }
    
    //methods
    /**
     * Get the value of the object
     * @return the value (Point) of the object
     */
    public Point getPoint()
    {
        return new Point(_point);
    }
    /**
     * Get the next Node
     * @return the next object
     */
    public PointNode getNext()
    {
        return _next;
    }
    /**
     * Set new Value to this object
     * @parm p - new value
     */
    public void setPoint(Point p)
    {
        _point = new Point(p);
    }
    /**
     * Set next object of PointNode
     * @parm next - next PointNode
     */
    public void setNext(PointNode next)
    {
        _next = next;
    }
}//end of class
