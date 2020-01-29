package Q_2;
import java.util.*;
import javax.swing.JPanel;

import java.awt.Color;
import java.awt.Graphics;

public class MyPanel extends JPanel{
	public int sizeBox = 30;// size of each box
	public RobotsWrold robotsWrold = null;
	public String directions[] = {"<","^",">","v"};
	private Color cArr[] = {Color.blue,Color.cyan,Color.DARK_GRAY,Color.green,Color.magenta,Color.ORANGE,Color.pink,Color.red,Color.yellow,Color.LIGHT_GRAY};
	
	public MyPanel()
	{
		super();
	}
	
	public void paintComponent(Graphics g)
	{
		if (robotsWrold != null)
		{
			g.clearRect(0, 0, getWidth(), getHeight());
			int worldSize = robotsWrold.getSize();
			int x0,y0;
			Color c;
			Robot r;
			int[][] World = robotsWrold.getWorld();
			g.setColor(new Color(0,0,0));
			for (int i=0; i<worldSize ;i++)
			{
				for (int j=0;j<worldSize;j++)
				{
					x0 = i*sizeBox + 5;
					y0 = j*sizeBox + 5;
					g.drawRect(x0, y0, sizeBox, sizeBox);
					if (World[i][j] != -1)
					{
						r = robotsWrold.getRobot(new Position(i,j));
						if(r != null)
						{
							g.setColor(cArr[r.getId()]);
							g.fillOval(x0, y0, sizeBox, sizeBox);
							g.setColor(new Color(255,255,255));
							g.drawString(directions[r.direction()],x0+sizeBox/2,y0+sizeBox/2);
							g.setColor(new Color(0,0,0));
						}
					}
				}
			}
		}
	}
	
	public void repaint(RobotsWrold robotsWrold)
	{
		this.robotsWrold = robotsWrold;
		super.repaint();
	}
}
