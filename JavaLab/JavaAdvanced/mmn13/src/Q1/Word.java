/**
 * Represents a Word with all details in the game
 *
 * @author Yehonathan Jacob
 * @version 11-03-2019
 */
package Q1;

import javax.swing.*;
import java.util.ArrayList;
import java.util.Arrays;


/**
 * calss from my mmn11
 */
public class Word {
	
	// instance variables
	private String Base; //Base of word that there is to find
	private String status; //status of Word to find
	private ArrayList<Character> leftChar = new ArrayList<Character>(); //char array that didn't selected
	private ArrayList<Character> foundChar = new ArrayList<Character>(); //char array that was selected
	
	 /**
     * Constructor for objects of class Word.
     */
	public Word() {
		Base = "";
		status = "";
		leftChar = new ArrayList<Character>(Arrays.asList('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w','x' ,'y','z'));
		foundChar = new ArrayList<Character>();
	}
	/**
     * Constructor for objects of class Word.
     */
	public Word(String newWord)
	{
		Base = newWord;
		status = "";
		for (int i=0;i<Base.length();i++) {status+= "_ ";}
		leftChar = new ArrayList<Character>(Arrays.asList('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w','x' ,'y','z'));
		foundChar = new ArrayList<Character>();
	}
	/**
	 * Constructor for objects of class Word.
	 */
	public Word(Word wr)
	{
		Base = wr.Base;
		status = wr.status;
		leftChar = new ArrayList<Character>(Arrays.asList('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w','x' ,'y','z'));
		foundChar = new ArrayList<Character>();
	}
	
	/*
	 * Get the left of word
	 * */
	public String getleftWrod() { return Base;}
	
	/*
	 * Get the status of word
	 * */
	public String getStatus() { return status;}
	
	/*
	 * Get the char that didn't selected yet
	 * */
	public String GetLeftChar() {return leftChar.toString();}
	
	/*
	 * Check if end of the game
	 * */
	public boolean isFounded() {return status.indexOf("_")<0;}
	
	
	/*
	 * Try set new char
	 * */	
	public int SetChar(char c) {
		if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'))
		{
			char newC = Character.toLowerCase(c);
			if (!foundChar.contains(newC)) { foundChar.add(newC); }
			if (leftChar.contains(newC)) { leftChar.remove(leftChar.indexOf(newC));}
			status = "";
			for (int i=0;i<Base.length();i++) {
				if (foundChar.contains(Base.toLowerCase().charAt(i))) {
					status+= Base.charAt(i)+" ";
				}
				else {
					status+= "_ ";
				}
			}
		}
		else
		{			
			JOptionPane.showMessageDialog(null, "Char must be in range:\n[a-z,A-Z]","Bad Input",JOptionPane.ERROR_MESSAGE);
			return 0;
		}
		return (Base.toLowerCase().contains(Character.toLowerCase(c)+""))? 1:-1;
	}
	

}
