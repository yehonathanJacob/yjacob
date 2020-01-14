package Q_2;
import java.util.*;
import java.io.*;
import java.lang.*;
import java.text.NumberFormat;

import javax.print.DocFlavor.STRING;
import javax.swing.JFrame;
import javax.swing.JOptionPane;

public class Tester {

	public static void main(String[] args) throws InterruptedException {
		// TODO Auto-generated method stub
		String action;
		do//loop for selecting valid action
		{				
			action = JOptionPane.showInputDialog(null, "Please type size:","Welcome",JOptionPane.CLOSED_OPTION);
			if (action == null){System.exit(0);}		
		}while(!(isInteger(action)) || Integer.parseInt(action) >=100);	
		int worldSize = Integer.parseInt(action);
		System.out.println("World size: "+worldSize);
		JFrame window = new JFrame();
		MyPanel drawing = new MyPanel();
		window.add(drawing);
		window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		window.setSize(drawing.sizeBox*worldSize+30,drawing.sizeBox*worldSize+50);
		window.setVisible(true);
		
		RobotsWrold robotsWrold = new RobotsWrold(worldSize);
		drawing.repaint(robotsWrold);
		Random rand = new Random();
		Position p = null;
		for (int i =0;i<5;i++)
		{
			do {
				p = new Position(rand.nextInt(worldSize),rand.nextInt(worldSize));
			}while(!(tryInster(p,robotsWrold)));
			System.out.println("inset: "+p.toString());
			Thread.sleep(1000);
			drawing.repaint(robotsWrold);
		}
		Robot r = robotsWrold.getRobot(p); //Robot that is going to move!
		int flag;
		for (int i=0;i<30;i++)// 30 moves
		{
			flag = 0;
			for (int j=0;j<4;j++)
			{
				p = new Position(r.getPosition());
				if (tryMove(p, robotsWrold))//means Robot moved
				{
					flag=1;
					break;
				}
				else//turn the robot
				{
					r.turnRight();
					Thread.sleep(1000);
					drawing.repaint(robotsWrold);
				}
			}
			if(flag==0)
			{
				JOptionPane.showMessageDialog(null, "Robot is stack","Error",JOptionPane.ERROR_MESSAGE);
				System.exit(0);
			}
			Thread.sleep(1000);
			drawing.repaint(robotsWrold);
		}
		JOptionPane.showMessageDialog(null, "Simulation is done!","Info",JOptionPane.INFORMATION_MESSAGE);
	}

	public static boolean isInteger( String input )
	{
	   try
	   {
	      Integer.parseInt( input );
	      return true;
	   }
	   catch( Exception e )
	   {
		   System.out.println("isInteger Eroor:"+ e);
	      return false;
	   }
	}
	public static boolean tryInster(Position p, RobotsWrold robotsWrold)
	{
		try
	   {
			robotsWrold.addRobot(p);
	      return true;
	   }
	   catch( Exception e )
	   {
		   System.out.println("tryInster Eroor:"+ e);
	      return false;
	   }
	}
	public static boolean tryMove(Position p, RobotsWrold robotsWrold)
	{
		try
		   {
				robotsWrold.moveRobot(p);
		      return true;
		   }
		   catch( Exception e )
		   {
			   System.out.println("tryMove Eroor:"+ e);
		      return false;
		   }
	}
}
