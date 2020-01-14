import java.util.Scanner;
public class Congruent
{
    /*
     *This Class was made to check if two triangles are congruent or not.
     *Input: P11(x,y)P12(x,y) P13(x,y)
     *       P21(x,y)P22(x,y) P23(x,y)
     *Output:Answer if the two triangles are congruent or not.
     */
    public static void main (String [] args)
    {
        Scanner scan = new Scanner (System.in);
        int x11,y11,x12,y12,x13,y13;//point's variables of triangles: 1
        int x21,y21,x22,y22,x23,y23;//point's variables of triangles: 2
        double a1,b1,c1; //lengths of triangles: 1
        double a2,b2,c2; //lengths of triangles: 2
        System.out.println("Please enter point's variables of triangles: 1");
        System.out.print("x11 = ");
        x11 = scan.nextInt();
        System.out.print("y11 = ");
        y11 = scan.nextInt();
        System.out.print("x12 = ");
        x12 = scan.nextInt();
        System.out.print("y12 = ");
        y12 = scan.nextInt();
        System.out.print("x13 = ");
        x13 = scan.nextInt();
        System.out.print("y13 = ");
        y13 = scan.nextInt();
        System.out.println("Please enter point's variables of triangles: 2");
        System.out.print("x21 = ");
        x21 = scan.nextInt();
        System.out.print("y21 = ");
        y21 = scan.nextInt();
        System.out.print("x22 = ");
        x22 = scan.nextInt();
        System.out.print("y22 = ");
        y22 = scan.nextInt();
        System.out.print("x23 = ");
        x23 = scan.nextInt();
        System.out.print("y23 = ");
        y23 = scan.nextInt();
        /*calculate of triangles:1 lengths.*/
        a1 = Math.sqrt(Math.pow((x11-x12), 2)+Math.pow((y11-y12), 2));
        b1 = Math.sqrt(Math.pow((x12-x13), 2)+Math.pow((y12-y13), 2));
        c1 = Math.sqrt(Math.pow((x13-x11), 2)+Math.pow((y13-y11), 2));
        /*calculate of triangles:2 lengths.*/
        a2 = Math.sqrt(Math.pow((x21-x22), 2)+Math.pow((y21-y22), 2));
        b2 = Math.sqrt(Math.pow((x22-x23), 2)+Math.pow((y22-y23), 2));
        c2 = Math.sqrt(Math.pow((x23-x21), 2)+Math.pow((y23-y21), 2));
        System.out.println("The first triangle is ("+x11+","+y11+") ("+x12+","+y12+") ("+x13+","+y13+")");
        System.out.println("The lengths are "+a1+", "+b1+", "+c1+".");
        System.out.println("The first triangle is ("+x21+","+y21+") ("+x22+","+y22+") ("+x23+","+y23+")");
        System.out.println("The lengths are "+a2+", "+b2+", "+c2+".");
        if((a1 == a2 && b1 == b2 && c1 == c2)//
        || (a1 == a2 && b1 == c2 && c1 == b2)//
        || (a1 == b2 && b1 == a2 && c1 == c2)//
        || (a1 == b2 && b1 == c2 && c1 == a2)//
        || (a1 == c2 && b1 == a2 && c1 == b2)//
        || (a1 == c2 && b1 == b2 && c1 == a2)){
            System.out.println("The triangle are congruent.");
        }
        else{
        	System.out.println("The triangle are not congruent.");
        }
        /*distance =  Math.sqrt(Math.pow((Ax-Bx), 2)+Math.pow((Ay-By), 2));
        System.out.println("The length of the line between the points A("+Ax+","+Ay+") and B("+Bx+","+By+") is "+distance);*/
        
    } // end of method main
} // end of class Line