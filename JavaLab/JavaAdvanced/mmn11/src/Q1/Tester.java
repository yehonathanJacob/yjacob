package Q1;
import javax.swing.JOptionPane;
import java.util.*;

public class Tester {

	public static void main(String[] args) {
		// TODO Auto-generated method stub		
		WordsList WL = new WordsList();
		Word W;
		int count;		
		do//main loop: foreach game 
		{
			String action;
			do//loop for selecting valid action
			{				
				action = JOptionPane.showInputDialog(null, "Please type:\n'1' for getting a random Word\n'2' for input a Word","Welcome",JOptionPane.CLOSED_OPTION);
				if (action == null){System.exit(0);}		
			}while(!(action.length() == 1) || (!(action.charAt(0) == '1') && !(action.charAt(0) == '2')));
			switch (action.charAt(0)) {//switch for action
			case '1':
				W = new Word(WL.getWrod());				
				break;
			case '2':
				String newWord ="";
				boolean b1 = false;
				while(!b1)
				{
					newWord = JOptionPane.showInputDialog(null, "Please type a word with charters in range:\\n[a-z,A-Z]","Type a Word",JOptionPane.CLOSED_OPTION);					
					if (newWord == null){System.exit(0);}
					b1 = newWord.matches("^[a-zA-Z]+$");
				}
				W = new Word(newWord);
				break;
			default:
				W = new Word();
				break;
			}			
			String tryInput;
			count = 0;
			while(!W.isFounded()){//loop for game: for each try
				count++;
				tryInput = JOptionPane.showInputDialog(null,W.getStatus()+"\n"+W.GetLeftChar()+"\nPlease type a charters in range:\n[a-z,A-Z]","The Game",JOptionPane.CLOSED_OPTION);
				if (tryInput == null){System.exit(0);}
				if (tryInput.length() ==1)
				{
					W.SetChar(tryInput.charAt(0));
				}
				else
				{
					JOptionPane.showMessageDialog(null, "You need to type ONLY ONE CHARTER","Bad Input",JOptionPane.ERROR_MESSAGE);
				}
			}

		}while(JOptionPane.showConfirmDialog(null, "Congratulation!!\nYou finish the game after: "+count+" attempts.\nWould you like to have another game?","End of game Word: "+W.getleftWrod(),JOptionPane.YES_NO_OPTION) == 0);
		
	}

}
