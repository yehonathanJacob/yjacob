package Q2;

//import Q1.game;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class CalculatorWindow extends JFrame{

    private TextField exercise; //where exercise will be
    private int numberStatus;//status of bing in the number
    public Calculator cl = new Calculator(); //the calculator from string of the text

    /**
     * calculator window that contain everything is in the frame
     * @param title
     */
    public CalculatorWindow(String title){
        super(title);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        exercise = new TextField("");
        exercise.setEditable(false);
        exercise.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        add(exercise,BorderLayout.NORTH);// add TextField where the clicked evaluation will appears.

        JPanel pane = new JPanel();//panel that will contain all the buttons
        pane.setLayout(new BoxLayout(pane, BoxLayout.Y_AXIS));

        JPanel NumbersPanel = new JPanel(); //number 0-9 and '.','(+/-)'
        NumbersPanel.setLayout(new GridLayout(4,3));
        JButton bt;
        for (int i=1;i<=9;i++){
            bt = new JButton(i+"");
            bt.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
            bt.addActionListener(new numberLisener());
            NumbersPanel.add(bt);
        }
        bt = new JButton(".");
        bt.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        bt.addActionListener(new ActionLisener());
        NumbersPanel.add(bt);
        bt = new JButton("0");
        bt.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        bt.addActionListener(new numberLisener());
        NumbersPanel.add(bt);
        bt = new JButton("(+/-)");
        bt.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        bt.addActionListener(new ActionLisener());
        NumbersPanel.add(bt);
        pane.add(NumbersPanel);

        JPanel actionPanel =  new JPanel(); //actions: '+', '-', '*', '/'
        actionPanel.setLayout(new GridLayout(1,4));
        bt = new JButton("+");
        bt.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        bt.addActionListener(new ActionLisener());
        actionPanel.add(bt);
        bt = new JButton("-");
        bt.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        bt.addActionListener(new ActionLisener());
        actionPanel.add(bt);
        bt = new JButton("*");
        bt.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        bt.addActionListener(new ActionLisener());
        actionPanel.add(bt);
        bt = new JButton("/");
        bt.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        bt.addActionListener(new ActionLisener());
        actionPanel.add(bt);
        pane.add(actionPanel);

        JPanel finalPanel = new JPanel();//actions: '=', '<clean>'
        finalPanel.setLayout(new GridLayout(1,2));
        bt = new JButton("<clean>");
        bt.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        bt.addActionListener(new ActionLisener());
        finalPanel.add(bt);
        bt = new JButton("=");
        bt.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        bt.addActionListener(new ActionLisener());
        finalPanel.add(bt);
        pane.add(finalPanel);

        add(pane,BorderLayout.CENTER);//adding all the actions

        JLabel bottomText = new JLabel("לפי הדרישות: אין סדר פעולות חשבון");
        bottomText.setHorizontalAlignment(SwingConstants.CENTER);
        add(bottomText,BorderLayout.SOUTH);//adding explain text
        pack();
        setMinimumSize(new Dimension(getWidth(),getHeight()));
        numberStatus = -1;

    }

    /**
     * listener when number is clicked.
     */
    private class numberLisener implements ActionListener{
        public void actionPerformed(ActionEvent e){
            int num = Integer.parseInt(e.getActionCommand());
            if (numberStatus <= 0)
                numberStatus += 2;
            exercise.setText(exercise.getText()+num);
        }
    }

    /**
     * listener when action is clicked.
     */
    private class ActionLisener implements ActionListener{
        public void actionPerformed(ActionEvent e){
            String action = e.getActionCommand();
            switch (action){
                case ".":
                    if (numberStatus == 1)
                    {
                        exercise.setText(exercise.getText() + action);
                        numberStatus = 0;
                    }
                    else
                    {
                        if (numberStatus == 2)
                            JOptionPane.showMessageDialog(null, "You can click '.' only ones.","Bad Input",JOptionPane.ERROR_MESSAGE);
                        if (numberStatus == -1)
                            JOptionPane.showMessageDialog(null, "You can click '.' in the middel of the number.","Bad Input",JOptionPane.ERROR_MESSAGE);
                    }
                    break;
                case "(+/-)":
                    if (numberStatus == -1)
                    {
                        exercise.setText(exercise.getText() + action);
                    }
                    else{
                        JOptionPane.showMessageDialog(null, "You can click '(+/-)' only at begging of a number.","Bad Input",JOptionPane.ERROR_MESSAGE);
                    }
                    break;
                case "+":
                case "-":
                case "*":
                case "/":
                    if (numberStatus >0)
                    {
                        exercise.setText(exercise.getText() + action);
                        numberStatus = -1;
                    }
                    else{
                        JOptionPane.showMessageDialog(null, "You can click '"+action+"' only after a number.","Bad Input",JOptionPane.ERROR_MESSAGE);
                    }
                    break;
                case "<clean>":
                    exercise.setText("");
                    numberStatus=-1;
                    break;
                case "=":
                    if (numberStatus >0)
                    {
                        System.out.printf("Start calculation%n");
                        try{
                            cl.runQuery(exercise.getText());
                            if(cl.status) {
                                String res;
                                if (cl.result<0)
                                    res = "(+/-)"+(cl.result+"").substring(1);
                                else
                                    res = cl.result+"";
                                if (res.contains("."))
                                    numberStatus = 2;
                                else
                                    numberStatus = 1;
                                exercise.setText(res);
                            }
                        }catch (Exception er){
                            if (er instanceof CalculatorError){
                                JOptionPane.showMessageDialog(null, er.getMessage(),"Calculator Error",JOptionPane.ERROR_MESSAGE);
                            }
                        }
                    }
                    else{
                        JOptionPane.showMessageDialog(null, "You can click '"+action+"' only after a number.","Bad Input",JOptionPane.ERROR_MESSAGE);
                    }
                    break;
                default:
                    JOptionPane.showMessageDialog(null, "Un recognise Input.","Bad Input",JOptionPane.ERROR_MESSAGE);
                    break;
            }
        }
    }

}
