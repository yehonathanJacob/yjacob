package Q2;

import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;

public class main {
    private static HomePanel home;
    public static void main(String[] args) {

        /*Q2_Date date = new Q2_Date(18,Q2_Date.Months.August,2016);
        System.out.printf("Date: %s%n",date.toString());
        HashMap<Q2_Date,String> data = new HashMap<>();
        data.put(new Q2_Date(24, Q2_Date.Months.August,2019),"checkdata");
        System.out.printf("data: %s%n",data.toString());
        try {
            ObjectOutputStream output = new ObjectOutputStream(new FileOutputStream("check"));
            output.writeObject(data);
            output.flush();
            output.close();
            System.out.printf("save%n");
        }
        catch (Exception e){

        }*/
        /*try {
            ObjectInputStream input = new ObjectInputStream(new FileInputStream("check"));
            HashMap<Q2_Date,String> data = (HashMap<Q2_Date,String>)input.readObject();
            System.out.printf("data: %s%n",data.toString());
        }catch (Exception e){

        }*/
        /*Q2_Date date = new Q2_Date();
        System.out.printf("%s%n",date.toString());*/

        if (JOptionPane.showConfirmDialog(null, "Would you like to load data from file?","Open File",JOptionPane.YES_NO_OPTION) == 0)
        {
            try{
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
                ObjectInputStream input = new ObjectInputStream(Files.newInputStream(path));
                HashMap<Q2_Date,String> data = (HashMap<Q2_Date,String>)input.readObject();
                home = new HomePanel(data);

            }catch (Exception e){
                JOptionPane.showMessageDialog(null, "Couldn't read from file","Bad Input",JOptionPane.ERROR_MESSAGE);
                home = new HomePanel();
            }
        }
        else {
            home = new HomePanel();
        }
        JFrame window = new JFrame();
        window.add(home);
        window.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        window.pack();
        window.setMinimumSize(new Dimension(window.getWidth(),window.getHeight()));
        window.setVisible(true);
        window.addWindowListener(new java.awt.event.WindowAdapter() {
            @Override
            public void windowClosing(java.awt.event.WindowEvent windowEvent) {
                int res = JOptionPane.showConfirmDialog(window,
                        "Would you like to saveyour notes?", "Close Window?",
                        JOptionPane.YES_NO_CANCEL_OPTION,
                        JOptionPane.QUESTION_MESSAGE);
                if (res != JOptionPane.CANCEL_OPTION)
                {
                    if (res == JOptionPane.YES_OPTION)
                    {
                        JFileChooser fileChooser = new JFileChooser();
                        int user_command = fileChooser.showSaveDialog(null);
                        if (user_command == JFileChooser.APPROVE_OPTION) {
                            try
                            {
                                File file = fileChooser.getSelectedFile();
                                ObjectOutputStream outputStream = new ObjectOutputStream(new FileOutputStream(file));

                                outputStream.writeObject(home.data);
                                outputStream.close();

                            }
                            catch (Exception e) {
                                JOptionPane.showMessageDialog(null, "Couldn't save file","Bad Input",JOptionPane.ERROR_MESSAGE);
                            }
                        }

                    }
                    System.exit(0);
                }
            }
        });
    }
}
