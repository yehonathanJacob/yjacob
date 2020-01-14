package Q_2;
import java.util.*;
import java.awt.Color;
import java.io.*;
import java.lang.*;

public class Robot {
	public static final int LEFT=0,UP=1,RIGHT=2,DOWN=3;// ALL FOUR POSIBEL DIRECTIONS
	private int id;//robot id 
	private Position p1;//position of robot
	private int direction;//direction of robot
	
	public int getId() {return id;}
	public Position getPosition() {return p1;}
	public int direction() {return direction;}
	
	public Robot(int id, Position p, int direction) throws IllegalArgumentException
	{
		if (!(direction>=LEFT && direction<=DOWN)) {
			throw new IllegalArgumentException();
		}
		this.id = id;
		this.p1 = new Position(p);
		this.direction = direction;
	}
	
	public void move() {
		switch(direction)
		{
			case LEFT:
				this.p1.addToX(-1);
				break;
			case RIGHT:
				this.p1.addToX(1);
				break;
			case DOWN:
				this.p1.addToY(1);
				break;
			case UP:
				this.p1.addToY(-1);
				break;
		}
	}
	
	public void turnLeft() {
		direction -=1;
		if (direction<0)
			direction +=4;
	}
	public void turnRight() {
		direction +=1;
		if (direction>3)
			direction -=4;
	}
	public String toString() {return "Robot "+this.id;}
}
