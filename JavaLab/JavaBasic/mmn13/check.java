import java.util.*;
/**
 * Write a description of class check here.
 *
 * @author (your name)
 * @version (a version number or a date)
 */
public class check
{
    static public void main(String[] args)
    {
        Polygon pp = new Polygon();
        int counter =1;
        double xx,yy;
        Scanner scan = new Scanner (System.in);
        do
        {
            System.out.print("X"+counter+": ");
            xx = scan.nextDouble();
            System.out.print("Y"+counter+": ");
            yy = scan.nextDouble();
        }while(pp.addVertex(xx,yy));
        System.out.println(pp.toString());
        
        
        
        
        Polygon p1 = new Polygon();
        
        System.out.println("Please enter x cordinate:");
        double x = scan.nextDouble();
        System.out.println("Please enter y cordinate:");
        double y = scan.nextDouble();
        while(x!=-1.0 && y!=-1.0 && p1.addVertex(x,y))
        {            
            System.out.println("Please enter x cordinate:");
            x = scan.nextDouble();
            System.out.println("Please enter y cordinate:");
            y = scan.nextDouble();
        }
        System.out.println("Highest Vertex:");
        Point p = p1.highestVertex();
        System.out.println(p);
        System.out.println("Polygon To String:");
        System.out.println(p1.toString());
        System.out.println("Calc Perimeter:");
        System.out.println(p1.calcPerimeter());
        System.out.println("Calc Area:");
        System.out.println(p1.calcArea());
        System.out.println("is index of point:");
        System.out.println(p1.findVertex(new Point(4,4)));
        System.out.println("is next point:");
        System.out.println(p1.getNextVertex(new Point(4,4)));
        System.out.println("get Bounding Box:");
        System.out.println(p1.getBoundingBox());
    }
}
