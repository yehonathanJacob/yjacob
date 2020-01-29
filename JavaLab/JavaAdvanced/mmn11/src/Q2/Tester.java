package Q2;
import java.util.*;

public class Tester {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner scan = new Scanner (System.in);
		Rational[] r = new Rational[2];		
		for (int i=0;i<2;i++)//create to new Rational numbers  
		{
			boolean flag = true;
			int a=0,b=0,num = i+1;
			while(flag)
			{
				System.out.println("type number "+num+":");
				System.out.print("a"+num+": ");
				a = scan.nextInt();
				System.out.print("b"+num+": ");
				b = scan.nextInt();
				if (b>0) {flag = false;}
				else {System.out.println("b"+num+" must be integer and greater than 0"); }
			}
			r[i] = new Rational(a,b);
		}
		
		if (scan != null) {scan.close();}
		
		//reduce
		System.out.println("reduce:\tr1: "+r[0].toString()+"->"+(r[0].reduce()).toString()+"\n\tr2: "+r[1].toString()+"->"+(r[1].reduce()).toString());
		
		//greaterThan
		System.out.println("if "+(r[0].reduce()).toString()+" > "+(r[1].reduce()).toString()+": "+(r[0].greaterThan(r[1])));
		
		//equals
		System.out.println("if "+(r[0].reduce()).toString()+" = "+(r[1].reduce()).toString()+": "+(r[0].equals(r[1])));
		
		//plus
		System.out.println((r[0].reduce()).toString()+" + "+(r[1].reduce()).toString()+" = "+((r[0].plus(r[1])).reduce()).toString());
		
		//minus
		System.out.println((r[0].reduce()).toString()+" - "+(r[1].reduce()).toString()+" = "+((r[0].minus(r[1])).reduce()).toString());
		
		//multiply
		System.out.println((r[0].reduce()).toString()+" * "+(r[1].reduce()).toString()+" = "+((r[0].multiply(r[1])).reduce()).toString());
		
	}

}
