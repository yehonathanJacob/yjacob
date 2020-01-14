/**
 * Represents a convex polygon in the plain
 *
 * @author Yehonathan Jacob
 * @version 12-05-2017
 */
public class Polygon
{
    // instance variables
    private Point[] _vertices; //Arrey of vertices
    private int _noOfVertices;//Number of vertices
    private final int DEFAULT_AREY_LENGTH = 10;

    /**
     * Constructor for objects of class Polygon. Construct a new arrey of vertices with ability of 10 elements
     */
    public Polygon()
    {
        _vertices = new Point[DEFAULT_AREY_LENGTH];
        _noOfVertices = 0;
    }

    //methods: Set
    /**
     * This method sets new vertex
     * @param x - The new x coordinate
     * @param y - The new y coordinate
     * @return True if the given Vertex was entered successfully
     */
    public boolean addVertex(double x, double y)
    {
       if(_noOfVertices < DEFAULT_AREY_LENGTH)
       {
           _vertices[_noOfVertices] = new Point(x,y);
           _noOfVertices++;
           return true;
       }
       return false;
    }
    
    //methods: Get
    /**
     * This method get the highest vertex
     * @return Point - the highest vertex
     */
    public Point highestVertex()
    {
        Point highestVertex = null;
        for(int i=0;i<_noOfVertices;i++)
        {
            if(highestVertex == null)
            {
                highestVertex = _vertices[i];
            }
            else
            {
                if(highestVertex.getY() < _vertices[i].getY())
                {
                    highestVertex = _vertices[i];
                }
            }
        }
        if(highestVertex == null)
        {
            return null;
        }
        return new Point(highestVertex);
    }
    
    //other method
    /**
     * Returns a string representation of Polygon in the format ((x1,y1),(x2,y2)..).
     * @override toString in class java.lang.Object
     * @return A String representation of the Polygon
     */
    public String toString()
    {
        if (_noOfVertices == 0)
        {
            return "The polygon has 0 vertices.";
        }
        String theString = "The polygon has "+_noOfVertices+" vertices:\n(";
        for(int i=0;i<_noOfVertices-1;i++)
        {
            theString+="("+_vertices[i].getX()+","+_vertices[i].getY()+"),";
        }
        theString+="("+_vertices[_noOfVertices-1].getX()+","+_vertices[_noOfVertices-1].getY()+"))";
        return theString;
    }
    
    /**
     * This method get the highest vertex
     * @return The perimeter of the polygon
     */
    public double calcPerimeter()
    {
        double _perimeter = 0;
        if(_noOfVertices > 2)
        {
            Point _first = new Point(_vertices[_noOfVertices-1]);
            Point _second;
            for(int i=0;i<_noOfVertices;i++)
            {
                _second = new Point(_vertices[i]);
                _perimeter += _first.distance(_second);
                _first = new Point(_second);
            }
        }
        else
        {
            if(_noOfVertices == 2)
            {
                _perimeter = _vertices[0].distance(_vertices[1]);
            }
        }
        return _perimeter;
    }
    
    /**
     * This method calc the area of the polygon
     * @return the area size of the polygon
     */
    public double calcArea()
    {
        if(_noOfVertices<3)
        {
            return 0;
        }
        double areaSize = 0;
        Point p1 = new Point(_vertices[0]);
        Point p2 = new Point(_vertices[1]);
        Point p3;
        for(int i=2;i<_noOfVertices;i++)
        {
            p3 = new Point(_vertices[i]);
            areaSize += triangleArea(p1, p2, p3);
            p2 = new Point(p3);
        }
        return areaSize;
    }
    
    /**
     * This method check if this polygon is bigger then another one
     * @param other - The other polygon
     * @return True - if this polygon is bigger
     */
    public boolean isBigger(Polygon other)
    {
        return this.calcArea() > other.calcArea();
    }
    
    /**
     * This method get a Point in the polygon and return the index number of it.
     * @param other - The other point
     * @return the number of index
     */    
    public int findVertex(Point other)
    {
        for(int i=0;i<_noOfVertices;i++)
        {
            if(other.equals(_vertices[i]))
            {
                return i;
            }
        }
        return -1;
    }
    
    /**
     * This method get a Point in the polygon and return the next point int the polygon
     * @param other - The other point
     * @return the next point
     */
    public Point getNextVertex(Point other)
    {
        int _indexOfPoint = this.findVertex(other);
        if(_indexOfPoint != -1)
        {
            if(_noOfVertices == 1 || _indexOfPoint == _noOfVertices-1)
            {
                return new Point(_vertices[0]);
            }
            else
            {
                return new Point(_vertices[_indexOfPoint+1]);
            }
        }
        return null;
    }
    
    /**
     * This method give the blocking recrangle of this polygon
     * @return the blocking recrangle of this polygon
     */
    public Polygon getBoundingBox()
    {
        if(_noOfVertices<3)
        {   
            return null;
        }
        Polygon _recrangle = new Polygon();
        Point _left = new Point(_vertices[0]);
        Point _right = new Point(_vertices[0]);
        Point _top = new Point(_vertices[0]);
        Point _bottom = new Point(_vertices[0]);
        for(int i=1;i<_noOfVertices;i++)
        {
            if(_left.getX() > _vertices[i].getX())
            {
                _left = new Point(_vertices[i]);
            }
            if(_right.getX() < _vertices[i].getX())
            {
                _right = new Point(_vertices[i]);
            }
            if(_top.getY() < _vertices[i].getY())
            {
                _top = new Point(_vertices[i]);
            }
            if(_bottom.getY() > _vertices[i].getY())
            {
                _bottom = new Point(_vertices[i]);
            }
        }
        _recrangle.addVertex(_left.getX(),_bottom.getY());
        _recrangle.addVertex(_right.getX(),_bottom.getY());
        _recrangle.addVertex(_right.getX(),_top.getY());
        _recrangle.addVertex(_left.getX(),_top.getY());
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
