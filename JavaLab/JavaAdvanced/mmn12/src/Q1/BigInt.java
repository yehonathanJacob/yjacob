package Q1;
import java.util.*;
import java.io.*;
import java.lang.*;

public class BigInt implements Comparable {
	private ArrayList<Integer> number = new ArrayList<Integer>(); // The number
	private Character signal;// Signal: '+'or '-'
	
	public BigInt(String newNumber) throws IllegalArgumentException
	{ 
		int start = 0;
		if(newNumber.length() == 0 ) {
			signal = '+';
			number.add(0);
		}
		else {
			if (newNumber.charAt(start) == '+' || newNumber.charAt(start) == '-')
			{
				signal = newNumber.charAt(start);
				start ++;
			}
			else {
				signal = '+';
			}
			int End = start;

			start = newNumber.length() - 1;
			for (int i = start; i>=End; i--)
			{
				if (newNumber.charAt(i) >= '0' && newNumber.charAt(i) <= '9') {
					number.add(Integer.parseInt(newNumber.substring(i, i+1)));
				}
				else
				{
					throw new IllegalArgumentException();
				}
			}
			while (number.get(number.size() -1) == 0 && (number.size() > 1))
				number.remove(number.size() -1);
			if (!(number.size() > 0))
				throw new IllegalArgumentException();
		}
	}
	
	public BigInt(ArrayList<Integer> newNumber,Character newSignal)
	{
		this.number = newNumber;
		this.signal = newSignal;
	}
	public BigInt() {// '+0'
		this.number.add(0);
		this.signal='+';
	}
	
	public String toString() {
		String s = signal + "";
		for (int i=number.size() - 1; i>=0; i--) {
			s+= number.get(i).toString();
		}
		return s;
	}
	
	public BigInt plus(BigInt b)
	{
		if ((this.signal == '+' && b.signal == '+') || (this.signal == '-' && b.signal == '-'))
		{
			BigInt b1 = add(this, b);
			b1.signal = this.signal;
			return b1;
		}
		else {
			if(this.signal == '+')
				return sub(this,b);
			else
				return sub(b,this);
		}
	}
	
	public BigInt minus(BigInt b)
	{
		Character Nsiganl = '+';//'+' by defult
		if (b.signal == '+')
			Nsiganl = '-';
		return this.plus(new BigInt(b.number,Nsiganl));		
	}
	
	private BigInt add(BigInt b1, BigInt b2)
	{
		ArrayList<Integer> Nnumber= new ArrayList<Integer>();
		Character Nsiganl = '+';//'+' by defult
		int lengthB1 = b1.number.size() - 1, lengthB2 = b2.number.size()-1, length = Math.max(lengthB1, lengthB2);
		int temp =0,sum;
		for (int i = 0; i<=length;i++)
		{
			int x1=0,x2=0;
			if (lengthB1 >= i)
				x1 = b1.number.get(i);
			if (lengthB2 >= i)
				x2 = b2.number.get(i);
			sum = x1+x2+temp;
			temp = sum/10;
			if (sum>=10)
				sum = sum%10;
			Nnumber.add(sum);
		}
		while(temp != 0)
		{
			Nnumber.add((temp%10));
			temp = temp/10;
		}
		return new BigInt(Nnumber,Nsiganl);
	}
	
	private BigInt sub(BigInt b1, BigInt b2)
	{
		BigInt biger;
		BigInt smaller;
		int comp = comperNoSignal(b1, b2);
		ArrayList<Integer> Nnumber = new ArrayList<Integer>();
		Character Nsignal = '+';//'+' by defult
		if (comp == 0)
			return new BigInt();
		if (comp > 0)
		{
			biger = b2;
			smaller = b1;
			Nsignal = '-';
		}
		else
		{
			biger = b1;
			smaller = b2;
			Nsignal = '+';			
		}
		int temp =0,sum,lengthB1 = b1.number.size() - 1, lengthB2 = b2.number.size()-1;
		for (int i=0;i<=lengthB1;i++) {
			int x1 = biger.number.get(i),x2=0;
			if (lengthB2>=i)
				x2 = smaller.number.get(i);
			sum = x1 - x2 + temp;
			temp = 0;
			while (sum + ((-temp)*10)<0) {
				temp -= 1;
			}
			sum += ((-temp)*10);
			Nnumber.add(sum);
		}
		while (Nnumber.get(Nnumber.size() -1) == 0)
			Nnumber.remove(Nnumber.size() -1);
		return new BigInt(Nnumber,Nsignal);
	}
	
	private int comperNoSignal(BigInt b1, BigInt b2)//comper as if they are both '+'
	{
		int lengthB1 = b1.number.size() - 1, lengthB2 = b2.number.size()-1;
		if (lengthB1 != lengthB2)
			if (lengthB1>lengthB2)
				return -1;
			else
				return 1;
		//if not returned yet, so length is equal
		for (int i = lengthB1; i>=0;i--)
		{
			if (b1.number.get(i) !=  b2.number.get(i))
				if (b1.number.get(i) >  b2.number.get(i)) 
					return -1;
				else
					return 1;
		}
		//if not returned yet, so number, is equal
		return 0;
	}
	
	public int compareTo(Object c) {
		BigInt b = (BigInt)c;
		if (this.signal != b.signal)
		{
			if (this.signal == '+')
				return -1;
			else
				return 1;
		}
		int res = comperNoSignal(this,b);
		if (this.signal == '-')
			res *=-1;
		return res;
	}
	private BigInt mul(int x,int tens)
	{
		ArrayList<Integer> Nnumber = new ArrayList<Integer>();
		Character Nsignal = '+';//'+' by defult
		int sum,temp=0;
		for (int i=0;i<tens;i++)
			Nnumber.add(0);
		for (int i=0;i<this.number.size();i++)
		{
			sum = x*this.number.get(i);
			sum+=temp;
			temp = 0;
			while (sum - (temp*10) >= 10)
				temp +=1;
			sum -= (temp*10);
			Nnumber.add(sum);
		}
		while(temp != 0)
		{
			Nnumber.add((temp%10));
			temp = temp/10;
		}
		return new BigInt (Nnumber,Nsignal);
	}
	public BigInt divide(BigInt b) throws ArithmeticException{
		if (b.number.size() == 1 && b.number.get(0) == 0)
			throw new ArithmeticException();
		BigInt res = new BigInt();
		BigInt denominator = new BigInt(this.number,'+');
		BigInt counter = new BigInt(b.number,'+');
		BigInt sum = new BigInt(counter.number,counter.signal);
		BigInt one = new BigInt("1");
		while (denominator.compareTo(sum) <=0)
		{
			res = res.plus(one);
			sum = sum.plus(counter);
		}
		if (denominator.compareTo(sum) == 0)
			res = res.plus(one);
		if (this.signal != b.signal)
			res.signal = '-';
		return res;
			
	}
	public BigInt multiply(BigInt b)
	{
		BigInt res = new BigInt();
		int x;
		for (int i=0;i<b.number.size();i++)
		{
			x = b.number.get(i);
			res = res.plus(this.mul(x,i));
		}
		if (b.signal != this.signal)
			res.signal = '-';
		return res;
	}
	
}
