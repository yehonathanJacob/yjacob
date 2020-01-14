
/**
 * Represents a convex polygon in the plain.
 *
 * @author Yehonathan Jacob
 * @version 18/06/2017
 */
public class Polygon
{
    private PointNode _head;//The head of the list
    
    /**
     * Constructor for polygon empty list
     * This method order complexity of time O(1).
     * This method order complexity of space O(1)
     */
    public Polygon()
    {
        _head = null;
    }
    
    /**
     * This method sets new vertex
     * This method order complexity of time O(n).
     * This method order complexity of space O(1)
     * @parm p - new Point to add to list
     * @parm pos - number of new Point to be in list.
     * @return true - if it was success.
     */
    public boolean addVertex(Point p,int pos)
    {
        if(pos<1)
        {
            return false;
        }
        PointNode newPointNode = new PointNode(p);
        if(_head == null)
        {
            if(pos == 1)
            {                
                _head = newPointNode;
                return true;
            }
            else
            {
                return false;
            }
        }
        if(pos == 1)
        {
            newPointNode.setNext(_head);
            _head = newPointNode;
            return true;
        }        
        int moove = pos;
        PointNode behind = _head;
        while(moove > 2 && behind !=null )
        {
            behind = behind.getNext();
            moove--;
        }
        if(behind == null)
        {
            return false;
        }
        newPointNode.setNext(behind.getNext());
        behind.setNext(newPointNode);
        return true;
    }
    
    /**
     * This method get the highest vertex
     * This method order complexity of time O(n).
     * This method order complexity of space O(1)
     * @return Point - the higest vertex.
     */
    public Point highestVertex() 
    {
        if(_head == null)
        {
            return null;
        }
        Point highest = _head.getPoint();
        PointNode moove = _head.getNext();
        while(moove != null)
        {
            if(moove.getPoint().getY() > highest.getY())
                highest = moove.getPoint();            
            moove = moove.getNext();
        }
        return highest;        
    }
    
    /**
     * Returns a string representation of Polygon in the format ((x1,y1),(x2,y2)..).
     * This method order complexity of time O(n).
     * This method order complexity of space O(1)
     * @return String - this list as a sring
     * @override toString in class java.lang.Object
     */
    public String toString()
    {
        if(_head == null)
        {
            return "The polygon has 0 vertices.";
        }
        String theString = "(";
        PointNode nextPoint = _head;
        int noOfVertices = 0;
        while(nextPoint != null)
        {
            theString = theString + nextPoint.getPoint().toString();
            nextPoint = nextPoint.getNext();
            noOfVertices++;
        }
        theString = theString+")";
        theString = "The polygon has "+noOfVertices+" vertices:\n" + theString;
        return theString;    
    }
    
    /**
     * Get the primeter of Polygon
     * This method order complexity of time O(n).
     * This method order complexity of space O(1).
     * @return The perimeter of the polygon
     */
    public double calcPerimeter()
    {
        double perimeter = 0;
        if(_head != null && _head.getNext() != null)//check minimum of 2 value
        {
            if(_head.getNext().getNext() != null)//chceck minimum of 3 value
            {
                PointNode addNext = _head;
                while(addNext.getNext() != null)
                {
                    perimeter += addNext.getPoint().distance(addNext.getNext().getPoint());
                    addNext = addNext.getNext();
                }
                perimeter += addNext.getPoint().distance(_head.getPoint());
            }
            else//case only 2 value
            {
                perimeter = _head.getPoint().distance(_head.getNext().getPoint());
            }
        }
        return perimeter;
    }
    
    /**
     * This method calc the area of the polygon
     * This method order complexity of time O(n).
     * This method order complexity of space O(1).
     * @return the area size of the polygon
     */
    public double calcArea()
    {
        if(_head == null || _head.getNext() == null || _head.getNext().getNext() == null)//less than 3 points.
        {
            return 0;
        }
        double areaSize = 0;
        Point p1 = _head.getPoint();
        Point p2 = _head.getNext().getPoint();
        Point p3;
        PointNode run = _head.getNext().getNext();
        while(run != null)
        {
            p3 = run.getPoint();
            areaSize += triangleArea(p1, p2, p3);//order of O(1);
            p2 = new Point(p3);
            run = run.getNext();
        }        
        return areaSize;
    }
    
    /**
     * This method check if this polygon is bigger then another one
     * This method order complexity of time O(n).
     * This method order complexity of space O(1).
     * @param other - The other polygon
     * @return True - if this polygon is bigger
     */
    public boolean isBigger(Polygon other)
    {
        return this.calcArea() > other.calcArea();//order of O(n);
    }
    
    /**
     * This method get a Point in the polygon and return the index number of it.
     * This method order complexity of time O(n).
     * This method order complexity of space O(1).
     * @param p - The other point
     * @return the number of index
     */
    public int findVertex(Point p)
    {
        PointNode check = _head;
        int count = 0;
        while(check != null)
        {
            count++;
            if(check.getPoint().equals(p))
            {
                return count;
            }
            check = check.getNext();
        }
        return -1;
    }
    
    /**
     * This method get a Point in the polygon and return the next point int the polygon
     * This method order complexity of time O(n).
     * This method order complexity of space O(1).
     * @param p - The other point
     * @return the next point
     */
    public Point getNextVertex(Point p)
    {
        PointNode check = _head;        
        while(check != null)
        { 
            if(check.getPoint().equals(p))
            {
                if(check.getNext() != null)
                {
                    return check.getNext().getPoint();
                }
                else
                {
                    return _head.getPoint();
                }
            }
            check = check.getNext();
        }
        return null;
    }
    
    /**
     * This method give the blocking recrangle of this polygon
     * This method order complexity of time O(n).
     * This method order complexity of space O(1).
     * @return the blocking recrangle of this polygon
     */
    public Polygon getBoundingBox()
    {
        if(_head == null || _head.getNext() == null || _head.getNext().getNext() == null)
        {               
            return null;
        }
        Polygon _recrangle = new Polygon();
        Point _left = _head.getPoint();
        Point _right = _head.getPoint();
        Point _top = _head.getPoint();
        Point _bottom = _head.getPoint();
        PointNode moove = _head.getNext();
        Point pointMoove;
        while(moove != null)
        {
            pointMoove = moove.getPoint();
            moove = moove.getNext();
            if(_left.getX() > pointMoove.getX())
            {
                _left = new Point(pointMoove);
            }
            if(_right.getX() < pointMoove.getX())
            {
                _right = new Point(pointMoove);
            }
            if(_top.getY() < pointMoove.getY())
            {
                _top = new Point(pointMoove);
            }
            if(_bottom.getY() > pointMoove.getY())
            {
                _bottom = new Point(pointMoove);
            }
        }
        _recrangle.addVertex(new Point(_left.getX(),_bottom.getY()),1);
        _recrangle.addVertex(new Point(_right.getX(),_bottom.getY()),2);
        _recrangle.addVertex(new Point(_right.getX(),_top.getY()),3);
        _recrangle.addVertex(new Point(_left.getX(),_top.getY()),4);
        return _recrangle;
    }
    
    //private method
    private double triangleArea(Point p1, Point p2, Point p3)
    {
        double a = p1.distance(p2);
        double b = p2.distance(p3);
        double c = p3.distance(p1);
        double s = (a+b+c)/2;
        //Heron calc
        return  Math.sqrt(s*(s-a)*(s-b)*(s-c));
    }
}
