import java.util.Scanner;
public class Line 
{
/*
 *This Class was made to calculate the distance between two points.
 *Input: A(x,y) B(x,y)
 *Output: distance between A To B
 */
	public static void main (String [] args)
	{
		Scanner scan = new Scanner (System.in);
		int Ax,Ay;
		int Bx,By;//variables of point B
		double distance;
		System.out.println("Please enter 2 integers.");
		System.out.print("A: x = ");
		Ax = scan.nextInt();
		System.out.print("A: y = ");
		Ay = scan.nextInt();
		System.out.println("Please enter another 2 integers.");
		System.out.print("B: x = ");
		Bx = scan.nextInt();
		System.out.print("B: y = ");
		By = scan.nextInt();
		distance =  Math.sqrt(Math.pow((Ax-Bx), 2)+Math.pow((Ay-By), 2));
		System.out.println("The length of the line between the points A("+Ax+","+Ay+") and B("+Bx+","+By+") is "+distance);
		
	} // end of method main
} // end of class Line
