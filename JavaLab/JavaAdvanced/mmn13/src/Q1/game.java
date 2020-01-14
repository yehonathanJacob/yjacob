package Q1;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.lang.*;
import javax.swing.*;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JFrame;

/**
 * class game is the system how handel the hole game by creatting a JFrame, and handelling it
 */
public class game {
    private Word wr; //the word of the game
    private panel p; // the panel of the hangging man
    private JButton cmdPress;// the button to try next char
    private JFrame window; // the fareme where the game is happening.
    private JPanel layer1,layer2,layer3;// layers for the game control of the game
    private JLabel status,leftChars; //labels for the game
    private TextField nextCh; //text fot input
    private int numOfHit; //number of hit for the game

    /**
     * constractor for the game
     * @param wr
     */
    public game(Word wr){
        this.wr = new Word(wr);
    }

    /**
     * the function to run the game
     */
    public void run(){
        numOfHit=0;
        window = new JFrame("Hanging Man");
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setSize(400,450);

        JPanel pane = new JPanel();
        pane.setLayout(new BoxLayout(pane, BoxLayout.Y_AXIS));

        layer1 = new JPanel();
        layer1.setLayout(new FlowLayout());
        layer1.add(new JLabel("Status: "));
        status = new JLabel(wr.getStatus());
        layer1.add(status);
        pane.add(layer1);

        layer2 = new JPanel();
        layer2.setLayout(new FlowLayout());
        cmdPress = new JButton("Try Next");
        cmdPress.addActionListener(new ButtonLisener1());
        nextCh = new TextField("",2);
        layer2.add(cmdPress);
        layer2.add(nextCh);
        pane.add(layer2);

        layer3 = new JPanel();
        layer3.setLayout(new FlowLayout());
        layer3.add(new JLabel("Left: "));
        leftChars = new JLabel(wr.GetLeftChar());
        layer3.add(leftChars);
        pane.add(layer3);

        p = new panel();
        window.add(pane,BorderLayout.NORTH);
        window.add(p,BorderLayout.CENTER);
        window.setVisible(true);

    }

    /**
     * class for the panel of the hangging man
     */
    private class panel extends JPanel{
        public panel()
        {
            super();
        }

        private int drawingLevel = 0;

        public void paintComponent(Graphics g){
            int width = getWidth();
            int height = getHeight();
            int midWidth = width/2,midHeight=height/2,stageW=width/100,stageH=height/100;
            g.clearRect(0, 0, width, height);
            g.setColor(new Color(139,69,19));
            g.drawLine(midWidth-45*stageW,98*stageH,midWidth+40*stageW,98*stageH);
            g.drawLine(midWidth-40*stageW,98*stageH,midWidth-40*stageW,5*stageH);
            g.drawLine(midWidth-40*stageW,5*stageH,midWidth,5*stageH);
            g.drawLine(midWidth,5*stageH,midWidth,10*stageH);
            g.setColor(Color.black);
            for (int i=0;i<drawingLevel;i++){
                switch (i ){
                    case 0:
                        g.drawOval(midWidth-10*stageW, 10*stageH, 20*stageW, 20*stageH);
                        break;
                    case 1:
                        g.drawLine(midWidth,30*stageH,midWidth,75*stageH);
                        break;
                    case 2:
                        g.drawLine(midWidth,45*stageH,midWidth+15*stageW,60*stageH);
                        break;
                    case 3:
                        g.drawLine(midWidth,45*stageH,midWidth-15*stageW,60*stageH);
                        break;
                    case 4:
                        g.drawLine(midWidth,75*stageH,midWidth+20*stageW,95*stageH);
                        break;
                    case 5:
                        g.drawLine(midWidth,75*stageH,midWidth-20*stageW,95*stageH);
                        break;
                    case 6:
                        g.setColor(Color.red);
                        g.drawLine(midWidth-20*stageW,10*stageH,midWidth+20*stageW,95*stageH);
                        g.setColor(Color.black);
                        break;
                }
            }

        }

        /**
         * move drawingLevel by one.
         */
        public void nextDraw(){drawingLevel ++;}
        public boolean isEnd(){return drawingLevel>=7;}
    }

    /**
     * the button that actualy handdelling the game
     */
    private class ButtonLisener1 implements ActionListener{
        public void actionPerformed(ActionEvent e){
            String s = nextCh.getText();
            if (s.length() == 1){
                numOfHit +=1;
                int res = wr.SetChar(s.charAt(0));
                if (!p.isEnd() && res == -1){
                    p.nextDraw();
                }
                leftChars.setText(wr.GetLeftChar());
                status.setText(wr.getStatus());
                p.repaint();
                if (wr.isFounded()){
                    JOptionPane.showMessageDialog(null, "Congratulation!!\nYou finish the game after: "+numOfHit+" attempts.","End of game Word: "+wr.getleftWrod(),JOptionPane.INFORMATION_MESSAGE);
                    System.exit(0);
                }
                if (p.isEnd())
                {
                    JOptionPane.showMessageDialog(null, "You have hit too many time so it is game over.\nThe Word was "+wr.getleftWrod(),"Game Over",JOptionPane.ERROR_MESSAGE);
                    System.exit(0);
                }

            }
            else{
                JOptionPane.showMessageDialog(null, "Pleas type ONE char.","Bad Input",JOptionPane.ERROR_MESSAGE);
            }
        }
    }

}
