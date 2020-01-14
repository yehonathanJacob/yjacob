package Q_2;
import java.util.*;
import java.io.*;
import java.lang.*;

public class RobotsWrold {
	private int wroldSize;
	private int World[][];
	private ArrayList<Robot> ids;
	private int LastId;
	
	public RobotsWrold(int size) {
		wroldSize = size;
		World = new int[size][size];
		ids = new ArrayList<Robot>();
		LastId = -1;
		for (int i=0;i<wroldSize;i++)
			for (int j=0;j<wroldSize;j++)
				World[i][j] = -1;
	}
	
	public void addRobot(Position p) throws IllegalPosition
	{
		Random rand = new Random();
		if(p.getX() < wroldSize && p.getY() < wroldSize && p.getX() >= 0 && p.getY() >= 0 && World[p.getX()][p.getY()] == -1)
		{
			LastId ++;
			int id = LastId;
			int diretion = rand.nextInt(4);
			ids.add(id, new Robot(id,p,diretion));
			World[p.getX()][p.getY()] = LastId;
		}
		else {
			throw new IllegalPosition();
		}
	}
	
	public Robot removeRobot(Position p)
	{
		if(p.getX()< wroldSize && p.getY() < wroldSize && p.getX() >= 0 && p.getY() >= 0 && World[p.getX()][p.getY()] != -1) {
			int id = World[p.getX()][p.getY()];
			Robot r = ids.remove(id);
			World[p.getX()][p.getY()] = -1;
			return r;
		}
		return null;
	}
	
	public Robot getRobot(Position p)
	{
		if(p.getX()< wroldSize && p.getY() < wroldSize && p.getX() >= 0 && p.getY() >= 0 && World[p.getX()][p.getY()] != -1) {
			int id = World[p.getX()][p.getY()];
			Robot r = ids.get(id);			
			return r;
		}
		return null;
	}
	
	public void moveRobot(Position p) throws IllegalPosition
	{
		int x= p.getX(),y=p.getY();
		if(x < wroldSize && y < wroldSize && x >= 0 && y >= 0 && World[p.getX()][p.getY()] != -1) {
			int id = World[x][y];
			Robot r = ids.get(id);
			switch (r.direction())
			{
				case 0:
					if ( (x -1) < 0 || (World[x -1][y] != -1))
					{System.out.println("Err1"+ p.getX()+"x: "+x);
					throw new IllegalPosition();}
					break;
				case 1:
					if ((y -1) < 0 || (World[x][y - 1] != -1))
					{System.out.println("Err2"+ p.getY()+"y: "+y);
					throw new IllegalPosition();}
					break;
				case 2:
					if ((x +1) >= wroldSize ||  (World[x +1][y] != -1))
					{System.out.println("Err3"+ p.getX()+"x: "+x);
					throw new IllegalPosition();}
					break;
				case 3:
					if ((y +1) >= wroldSize || (World[x][y + 1] != -1))
					{System.out.println("Err4:"+ p.getY()+"y: "+y);
					throw new IllegalPosition();}
					break;
			}
			World[x][y] = -1;
			r.move();
			Position pn = new Position(r.getPosition());
			World[pn.getX()][pn.getY()] = id;
		}
		else
		{
			System.out.println("Err of x: "+x+" y: "+y);
			throw new IllegalPosition();
		}
		
	}
	
	public int getSize() {return wroldSize;}
	public int[][] getWorld(){return World;}
	public ArrayList<Robot> getList(){return ids;}
}
