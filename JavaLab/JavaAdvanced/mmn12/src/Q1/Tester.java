package Q1;
import java.util.*;
import java.io.*;
import java.lang.*;


public class Tester {
	
	private static Scanner scan = new Scanner (System.in);// scanner for Tester class

	/*
	 * function that just continue running until she get a valid input from the standart input for BigInt
	 * @return new BigInt
	 * */
	public static BigInt getNumber() {		
		while (true)
		{
			try {
				System.out.println("type big number");
				BigInt b =  new BigInt(scan.next());
				return b;
			}catch(IllegalArgumentException e) 
			{
				System.out.println("Error in number!");
			}
		}
	}
	
	
	/*
	 * main method*/
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		BigInt b1 = getNumber();
		BigInt b2 = getNumber();
		System.out.printf("%s - %s = %s%n",b1.toString(),b2.toString(),b1.minus(b2).toString());
		System.out.printf("%s + %s = %s%n",b1.toString(),b2.toString(),b1.plus(b2).toString());
		System.out.printf("%s <? %s = %d%n",b1.toString(),b2.toString(),b1.compareTo(b2));
		System.out.printf("%s * %s = %s%n",b1.toString(),b2.toString(),b1.multiply(b2).toString());
		System.out.printf("%s / %s = %s%n",b1.toString(),b2.toString(),b1.divide(b2).toString());
		
	}

}
