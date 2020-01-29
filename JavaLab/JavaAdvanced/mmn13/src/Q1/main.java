package Q1;

import java.io.File;
import java.lang.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Scanner;
import javax.swing.*;

public class main {

    public static Scanner input;
    /**
     * create a game, by first getting a Word from the project int mmn 11 and then create the class game
     * @param args
     */
    public static void main(String[] args) throws Exception{
        WordsList WL = new WordsList();
        Word W;
        String action;
        do//loop for selecting valid action
        {
            action = JOptionPane.showInputDialog(null, "Please type:\n'1' for getting a random Word\n'2' for input a Word\n'3' for input a File of words splited buy ' '","Welcome",JOptionPane.CLOSED_OPTION);
            if (action == null){System.exit(0);}
        }while(!(action.length() == 1) || (!(action.charAt(0) == '1') && !(action.charAt(0) == '2') && !(action.charAt(0) == '3')));
        switch (action.charAt(0)) {//switch for action
            case '1': // get a random word from list
                W = new Word(WL.getWrod());
                break;
            case '2': //input a word by typeing
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
            case '3': //get words form a file
                JFileChooser fileChooser = new JFileChooser();
                fileChooser.setCurrentDirectory(new File("."));
                fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
                int result;
                do{
                    result = fileChooser.showDialog(null,"Please select a file");
                }while (result == JFileChooser.CANCEL_OPTION
                        || fileChooser.getSelectedFile().toPath() ==  null
                        || !Files.exists(fileChooser.getSelectedFile().toPath()));
                Path path = fileChooser.getSelectedFile().toPath();
                ArrayList<String> Arr = new ArrayList<String>();
                input = new Scanner(path);
                while (input.hasNext()){
                    Arr.add(input.next());
                }
                input.close();
                WL =  new WordsList(Arr);
                W = new Word(WL.getWrod());
                break;
            default:
                W = new Word();
                break;
        }
        game g= new game(W);
        g.run();
    }
}
