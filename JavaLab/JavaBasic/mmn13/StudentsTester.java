/**
 * Students tester to Polygon class
 */
public class StudentsTester {
    public static void main(String[] args) {

        System.out.println("start");
        Polygon polygon = new Polygon();
        polygon.addVertex(2.0, 1.0);
        polygon.addVertex(5.0, 0.0);
        polygon.addVertex(7.0, 5.0);
        polygon.addVertex(4.0, 6.0);
        polygon.addVertex(1.0, 4.0);

        Point highest = polygon.highestVertex();
        System.out.println("\nTest highestVertex:\nhighest = "  +highest + " while it should be (4.0,6.0)" );
        System.out.println("\nTest toString() method:\n" + polygon);
        
        double perimeter = polygon.calcPerimeter();
        System.out.println("\nTest calcPerimeter:\nperimeter = "  + perimeter + " while it should be 18.47754906310363");

        double area = polygon.calcArea();
        System.out.println("\nTest calcArea:\narea = "  + area  +" while it should be: 22.499999999999996");
        Polygon biggerPolygon = new Polygon();
        biggerPolygon.addVertex(2.0, 1.0);
        biggerPolygon.addVertex(5.0, 0.0);
        biggerPolygon.addVertex(7.0, 5.0);
        biggerPolygon.addVertex(4.0, 7.0);
        biggerPolygon.addVertex(1.0, 4.0);

        System.out.println ("\nTest isBigger:\nexpected result here is false and actual result is: " + polygon.isBigger(biggerPolygon));// should be false
        
        Point point = new Point(4.0, 6.0);
        int index = polygon.findVertex(point);
        System.out.println("\nTest findVertex:\nindex = "  + index + " while actual result should be 3");
        
        Point actualNextVertex = new Point(1.0, 4.0);
        Point nextVertex = polygon.getNextVertex(point);
        System.out.println("\nTest getNextVertex:\nnext point after (4.0,6.0) is = " + nextVertex + " while it should be should be (1.0,4.0)");

        Polygon boundingBox = polygon.getBoundingBox();
        System.out.println("\nTest getBoundingBox:\nthe bounding box is:\n" + boundingBox + "\nwhile it should be:\nThe polygon has 4 vertices:\n((1.0,0.0),(7.0,0.0),(7.0,6.0),(1.0,6.0))");
        
        System.out.println("\nNote that this is only a basic test. Make sure you test all cases!");
        System.out.println("end");
  }
}
