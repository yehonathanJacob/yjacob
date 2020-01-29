/**
 * All the methods for Maman 14
 *
 * @author Yehonathan Jacob
 * @version 11/06/2017
 */
public class Ex14
{
    /**
     * This method order complexity of time O(n).
     * This method order complexity of space O(1).
     * This method in the worst case run overr the array twice (0 - n).
     * First time it run on the array (0 - n) to find an optional sink, and to check all the variables that under of it.
     * Second time, if there was finded an optional sink, it run (0 - k) to check all the variables on top of the sink.
     * 
     * @param mat - an array int[n][n] that present the mat.
     * @return The index number in the the main diagonal of the sink. if there is not, it will return -1.
     */
    public static int isSink(int [][] mat)
    {
        int k=-1;//value of the index who will return.        
        for(int i=0;i<mat[0].length;i++) //run O(n) to find an optional sink and check all the variables under of it.
        {
            if(k==-1 && mat[i][i] == 0) //if there is not opptional sink so far.
            {
                k=i;
            }            
            if(k!=-1 && k!=i) //posibell that there wasnt an optional sink, so continue to run on the array
            {
                if(mat[k][i] != 0 || mat[i][k] != 1) //if the variables under the optional sink, arent as they supposed to.
                {
                    if(mat[k][i] == 1 || mat[i][k] == 0)//if the variables belong to maby next k.
                    {
                        k=i;
                    }
                    else
                    {
                        k=-1;
                    }                        
                }
            }
        }
        if(k!=-1) //if ther was finded an optioanl sink, now left only to check the variables on top of it.
        {
            for(int i=0;i<k;i++) //run O(n)  0 - k.
            {
                if(mat[k][i] != 0 || mat[i][k] != 1) //if the variables on top of the optional sink arrent as they supposed to.
                    return -1;
            }
        }
        return k;
    }//end of method

    /**
     * This method order complexity of time and space O(Log(n)).
     * This method do O(1) actions but ask for a recursive method that order complexity time and space of O(Log(n)).
     * The recursive method first check the posibility to find the value of given squer int the array.
     * Then, it check in the corners of this squer
     * Else it divide the given squer in the array to four.
     * 
     * @param S - an array int[n][n] that present the mat.
     * @param x - an int that present the looking for- value.
     * @return True if this value is in this array
     */
    public static boolean find(int[][] mat, int x)
    {
        if(x >= mat[0][0] && x <= mat[mat[0].length -1][mat[0].length -1])//check existem in mat
        {
            //Go to a method to find for this value in the array. Order complexity of O(Log(n))
            return checkSquer(mat, x, 0, 0, mat[0].length -1, mat[0].length -1);
        }
        return false;
    }//end of method
    
    private static boolean checkSquer(int[][] mat, int x, int topLeftX, int topLeftY, int bottomRightX, int bottomRightY)
    // The order complexity time of this method is Lon4(n^2) => O(Log(n)).
    // The order complexity space of this method is Lon4(6*n^2) => O(Log(n)).
    {
        //check if it is one of the corner.
        if(mat[topLeftX][topLeftY] == x
        || mat[topLeftX][bottomRightY] == x
        || mat[bottomRightX][topLeftY] == x
        || mat[bottomRightX][bottomRightY] == x)
        {
            return true;
        }
        
        //check quarter1
        if(x >= mat[topLeftX][topLeftY] && x <= mat[((bottomRightX+topLeftX)/2)][((bottomRightY+topLeftY)/2)])//check existem in this quarter of mat
        {            
            return checkSquer(mat, x, topLeftX, topLeftY, ((bottomRightX+topLeftX)/2), ((bottomRightY+topLeftY)/2));
        }
        
        //check quarter2
        if(x >= mat[topLeftX][(bottomRightY+topLeftY)/2+1] && x <= mat[((bottomRightX+topLeftX)/2)][bottomRightY])//check existem in this quarter of mat
        {            
            return checkSquer(mat, x, topLeftX, (bottomRightY+topLeftY)/2+1, ((bottomRightX+topLeftX)/2), bottomRightY);
        }
        
        //check quarter3
        if(x >= mat[(bottomRightX+topLeftX)/2+1][topLeftY] && x <= mat[bottomRightX][((bottomRightY+topLeftY)/2)])//check existem in this quarter of mat
        {            
            return checkSquer(mat, x, (bottomRightX+topLeftX)/2+1, topLeftY, bottomRightX, ((bottomRightY+topLeftY)/2));
        }
        
        //check quarter4
        if(x >= mat[(bottomRightX+topLeftX)/2+1][(bottomRightY+topLeftY)/2+1] && x <= mat[bottomRightX][bottomRightY])//check existem in this quarter of mat
        {            
            return checkSquer(mat, x, (bottomRightX+topLeftX)/2+1, (bottomRightY+topLeftY)/2+1, bottomRightX, bottomRightY);
        }
        
        return false;//have not finde in ANY quarter this x                
    }
    
    /**
     * Check if it is possibel to build number n with variables of an array.
     * 
     * @param S - an array int[n].
     * @param n - a number to look for.
     * @return If the number can be build by the variables of the array.
     */
    public static boolean isSumOf(int[] s,int n)
    //checking the posibility to build n with variables from s
    {
        if(n==0)
        {
            return true;
        }
        if( n<0)
        {
            return false;
        }
        return tryLess(s,n,0);//try to build n from s.
    }
    
    private static boolean tryLess(int[] s,int n,int index)
    //checking if you can build n with varibels from the array from index to s.length
    {
        if(index<s.length)
        {
            if(isSumOf(s,n-s[index]))// try to build smaler value
            {
                return true;
            }
            else
            {
                return tryLess(s,n,index+1);//continue with trying next value
            }
        }
        else
        {
            return false;
        }
    }
    
    
    /**
     * Count the number of ways between one way to enother.
     * This method call for a recursive method that have the standing point, and the arivel point.
     * It try to arive to the arivel point by by mooving to any where posibel.
     * In each moovment, the method put -1 value t rember that it have stepd to ther.
     * When it arive to the arivel point, it return all the way back +1 to the number of ways between too point.
     * Otherwise, it return 0 to the number of ways.
     * Every time it gose back, it re-put the right value in every point.
     * 
     * @param mat - an array int[n][n] that pressent the mat
     * @param x1 - value of x cordinate of starting point
     * @param y1 - value of y cordinate of starting point
     * @param x2 - value of x cordinate of destination point
     * @param y2 - value of x cordinate of destination point
     * @return Numbers of way to go.
     */
    public static int numPaths(int[][] mat,int x1, int y1, int x2, int y2)
    //checking number of moovment posibel betwin (x1,y1) to (x2,y2)
    {
        int sum = 0;
        if(x1!=x2 || y1!=y2)
        {
            boolean blocked = true;
            int go;
            int original = mat[x1][y1];
            mat[x1][y1] = -1;
            
            if(canMoov(mat,x1-1,y1))
            {
                go = numPaths(mat,x1-1,y1,x2,y2);//try all the ways after goint 1 step up
                if (go!=-1)
                {
                    sum += go;
                    blocked = false;
                }
            }
            if(canMoov(mat,x1,y1-1))
            {
                go = numPaths(mat,x1,y1-1,x2,y2);//try all the ways after goint 1 step left
                if (go!=-1)
                {
                    sum += go;
                    blocked = false;
                }
            }
            if(canMoov(mat,x1+1,y1))
            {
                go = numPaths(mat,x1+1,y1,x2,y2);//try all the ways after goint 1 step down
                if (go!=-1)
                {
                    sum += go;
                    blocked = false;
                }
            }
            if(canMoov(mat,x1,y1+1))
            {
                go = numPaths(mat,x1,y1+1,x2,y2);//try all the ways after goint 1 step right
                if (go!=-1)
                {
                    sum += go;
                    blocked = false;
                }
            }
            mat[x1][y1] = original; 
            if(blocked)//check if it has atlist one time arived to the arivel point.
            {
                return -1;
            }
        }
        else
        {
            //meens we have ariived to our destination
            return 1;
        }
        return sum;
    }
    
    private static boolean canMoov(int[][] mat ,int x2,int y2)
    //check if we can moov the way to the this point.
    {
        return (y2>=x2) && y2>=0 && x2>=0 && y2 < mat[0].length && mat[x2][y2] != -1;
    }
}//end of class