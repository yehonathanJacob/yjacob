/**
 * Represents a Word WordsList all details in the game
 *
 * @author Yehonathan Jacob
 * @version 11-03-2019
 */

package Q1;
import java.util.*;

public class WordsList {

	// instance variables
	private ArrayList<String> Words = new ArrayList<String>();
	private int WordsLength;
	
	/**
     * Constructor for objects of class Word.
     */
	public WordsList() {
		String[] Arr = {"Apple", "banana", "tomato", "house", "window", "ship", "door", "mirror", "airplane", "train", "rope", "table", "wall", "shelf", "child", "mother", "school", "game", "big", "small"};	
		for (int i=0;i<Arr.length;i++) { 
			Words.add(Arr[i]);
		}
		WordsLength = Arr.length;
	}
	/**
     * Constructor for objects of class Word.
     */
	public WordsList(String[] Arr)
	{
		for (int i=0;i<Arr.length;i++) { Words.add(Arr[i]);}
		WordsLength = Arr.length;
	}
	
	/*
	 * Get a random word from word list
	 * */
	public String getWrod() {
		Random rand = new Random();
		int i = rand.nextInt(WordsLength);
		return Words.get(i);
				
	}
}
