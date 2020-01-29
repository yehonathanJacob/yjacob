
public class StudentTester {

    public static void main(String[] args) 
    {   
        checknumPaths();
        
        checkIsSumOf();
        
        checkIsSink();
        
        checkFind();
        //int a1 = foo(3,4);
        //int a2 = foo(4,5);        
    }

    private static void checknumPaths() {
        int[][] mat4 = {
                {1,   2,  3,  4},
                {5,   6,  7,  8},
                {9,  10, 11, 12},
                {16, 15, 14, 13}};
        
        int x1 = 0,  y1 = 0, x2 = 3, y2 = 3;
        System.out.println(Ex14.numPaths(mat4, x1, y1, x2, y2));

        //if(0 != Ex14.numPaths(mat4, x1, y1, x2, y2))
        //  System.out.println("checknumPaths() is failed");
        
    }

    private static void checkIsSumOf() {
        if(Ex14.isSumOf(new int[] {4,5}, 11) || !Ex14.isSumOf(new int[] {4,5}, 13))
            System.out.println("checkIsSumOf() is failed");
        System.out.println(Ex14.isSumOf(new int[] {3,4,5,11}, 11));
        System.out.println(Ex14.isSumOf(new int[] {11}, 0));
        System.out.println(Ex14.isSumOf(new int[] {4,5,7}, 13));
        System.out.println(Ex14.isSumOf(new int[] {3,5,7}, 16));
        System.out.println(Ex14.isSumOf(new int[] {3,5,7}, 17));
    }

    private static void checkFind() {
        int[][] mat = {
                {1, 2},
                {3, 4}};
        if(!Ex14.find(mat, 1))
            System.out.println("checkFind() is failed");
        int[][] mat1 = {
                {-4,-2, 5, 9},
                { 2, 5,12,13},
                {13,20,25,25},
                {22,24,49,57}};
        if(!Ex14.find(mat, 1))
            System.out.println("checkFind() is failed");
        System.out.println("-6: "+Ex14.find(mat1, -6));
        System.out.println("60: "+Ex14.find(mat1, 60));
        System.out.println("23: "+Ex14.find(mat1, 23));
        System.out.println("-4: "+Ex14.find(mat1, -4));
        System.out.println("-2: "+Ex14.find(mat1, -2));
        System.out.println("25: "+Ex14.find(mat1, 25));
        System.out.println("24: "+Ex14.find(mat1, 24));
        System.out.println("13: "+Ex14.find(mat1, 13));
        System.out.println("22: "+Ex14.find(mat1, 22));
        
    }

    private static void checkIsSink() {
        int[][] mat1 = {
                {0, 1},
                {0, 0}};
        
        int[][] mat2 = { 
                {0, 1, 1},
                {0, 1, 1},
                {0, 0, 0}};
                
        int[][] mat3 = { 
                {0, 1, 1, 0},
                {0, 1, 1, 1},
                {0, 0, 0, 0},
                {0, 1, 1, 1}};
                
        int[][] mat4 = { 
                {0, 1, 1, 0},
                {0, 1, 1, 1},
                {1, 0, 0, 0},
                {0, 1, 1, 1}};
        
        int[][] mat5 = { 
                {0, 1, 1, 1},
                {0, 1, 1, 1},
                {1, 0, 0, 1},
                {0, 0, 0, 0}};
                
        System.out.println(Ex14.isSink(mat1));
        System.out.println(Ex14.isSink(mat2));
        System.out.println(Ex14.isSink(mat3));
        System.out.println(Ex14.isSink(mat4));
        System.out.println(Ex14.isSink(mat5));
        
        //if(Ex14.isSink(mat1) != 1 || Ex14.isSink(mat2) != 2)
          //  System.out.println("isSink() is failed");

        
    }
    
    
    public static int foo (int a, int b) 
    {
        if (a>3)
        {
            return 2 + foo (b-1, a+1);
        }
        if (b<=4)
        {
            return 1 + foo (a-1, b+1);
        }
        return 0;
    }
}
