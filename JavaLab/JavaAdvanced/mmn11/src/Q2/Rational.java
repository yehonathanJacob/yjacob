/**
 * Represents a Rational number
 *
 * @author Yehonathan Jacob
 * @version 11-03-2019
 */
package Q2;

public class Rational {
	
	// instance variables
	private int Numerator;
	private int Denominator;
	
	/**
     * Constructor for objects of class Word.
     */
	public Rational(double Numerator,double Denominator)
	{		
		if ((double)(int)(Numerator) - Numerator == 0.0 && (double)(int)(Denominator) - Denominator == 0.0 && Denominator>0)
		{
			this.Numerator = (int)(Numerator);
			this.Denominator = (int)(Denominator);
		}
		else
		{
			this.Numerator = 0;
			this.Denominator = 1;
		}
	}
	
	/**
     * Returns a string representation of Rational
     * @return String - this class as a String
     * @override toString in class java.lang.Object
     */
	public String toString() {return  this.Numerator+"/"+this.Denominator; }
	
	/*
	 * getNumerator
	 * */
	public int getNumerator() {return this.Numerator;}
	
	/*
	 * getDenominator
	 * */
	public int getDenominator() {return this.Denominator;}
	
	/*
	 * check if greater than given Rational
	 * */
	public boolean greaterThan(Rational r1) {
		return this.Numerator*r1.getDenominator() > this.Denominator*r1.getNumerator();
	}
	
	/*
	 * check if equal to given Rational
	 * */
	public boolean equals(Rational r1) {
		return this.Numerator*r1.getDenominator() == this.Denominator*r1.getNumerator();
	}
	
	/*
	 * add this Rational to given Rational 
	 * */
	public Rational plus(Rational r1)
	{
		return new Rational(this.Numerator*r1.getDenominator() + this.Denominator*r1.getNumerator(), this.Denominator*r1.getDenominator());
	}
	
	/*
	 * sub this Rational from given Rational 
	 * */
	public Rational minus(Rational r1)
	{
		return new Rational(this.Numerator*r1.getDenominator() - this.Denominator*r1.getNumerator(), this.Denominator*r1.getDenominator());
	}
	
	/*
	 * mul this Rational to given Rational 
	 * */
	public Rational multiply(Rational r1)
	{
		return new Rational(this.Numerator*r1.getNumerator(), this.Denominator*r1.getDenominator());
	}
	
	
	public Rational reduce() {
		int GCD = gcd(this.Numerator,this.Denominator);
		return new Rational(this.Numerator/GCD ,this.Denominator/GCD );
	}
	
	/*
	 * get gcd of (x,y)
	 * */
	private int gcd(int x, int y)
	{
		if (y == 0)
			return x;
		return gcd(y, x % y);
	}
	
}
