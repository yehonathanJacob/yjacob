package Q1;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.*;

/**
 * main panel to present GUI
 */
public class MainPanel extends JFrame {
    private ProcessArr pArr; //the objects of array, of the number and controller.
    private JButton submit; // a button to start the work
    private JTextArea outTxt; //Output area
    private JTextField inputN,inputM; //Input for N and M

    public MainPanel(String title){
        super(title);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel Header = new JPanel();
        Header.setLayout(new FlowLayout());
        Header.add(new JLabel("Insert n: "));
        inputN = new JTextField("",5);
        inputN.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        Header.add(inputN);
        Header.add(new JLabel("Insert m: "));
        inputM = new JTextField("",5);
        inputM.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        Header.add(inputM);
        submit = new JButton("Start");
        Header.add(submit);
        add(Header, BorderLayout.NORTH);

        outTxt = new JTextArea(null,null,10,30);
        outTxt.setEditable(false);
        outTxt.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        add(outTxt,BorderLayout.CENTER);

        submit.addActionListener(new submitBtn());
        pack();
        setMinimumSize(new Dimension(getWidth(),getHeight()));

    }

    private class submitBtn implements ActionListener{
        @Override
        public void actionPerformed(ActionEvent e) {
            int N,M;
            try{
                N = Integer.parseInt(inputN.getText());
                M = Integer.parseInt(inputM.getText());
            }catch (Exception ex){
                JOptionPane.showMessageDialog(null, "You must input only plain numbers.","Bad Input",JOptionPane.ERROR_MESSAGE);
                return;
            }
            outTxt.setText("");
            pArr = new ProcessArr(N);
            outTxt.append("######## START #######\n");
            for(int i =0;i<M;i++){
                outTxt.append(i+": "+pArr.toString()+"\n");
                ExecutorService executor = Executors.newCachedThreadPool();
                for (int j=0;j<N;j++){
                    executor.execute(new moveInArr(pArr,j));
                }
                executor.shutdown();
                try{
                    executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
                }catch (InterruptedException a){
                    System.out.printf("error %n");
                }
                pArr.resetController();
            }
            outTxt.append(M+": "+pArr.toString()+"\n");
            outTxt.append("######## END #######");
        }
    }
}
