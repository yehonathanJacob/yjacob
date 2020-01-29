package Q_2;
import java.util.*;
import java.io.*;
import java.lang.*;

public class Position {
	private int x;
	private int y;
	
	public Position () {
		x = 0;
		y = 0;
	}
	public Position (int x,int y)
	{
		this.x = x;
		this.y = y;
	}
	public Position (Position p)
	{
		this.x = p.x;
		this.y = p.y;
	}
	
	
	public int getX() {return this.x;}
	public int getY() {return this.y;}
	public void setX(int x) {this.x = x;}
	public void setY(int y) {this.y = y;}
	public void addToX(int dis) {this.x += dis;}
	public void addToY(int dis) {this.y += dis;}
	public String toString() {return "postion x: "+this.x + " y: "+this.y;}
}
