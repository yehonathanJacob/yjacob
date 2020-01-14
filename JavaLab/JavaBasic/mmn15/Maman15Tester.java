
public class Maman15Tester {
    /**
     * @param args
     */
    public static void main(String[] args) {

        Polygon polygon = new Polygon();
        polygon.addVertex(new Point(2, 1), 1);
        polygon.addVertex(new Point(5, 0), 1);
        polygon.addVertex(new Point(7, 5), 2);
        polygon.addVertex(new Point(5, 5), 1);
        polygon.addVertex(new Point(4, 4), 4);
        System.out.println("polygon.addVertex:  -- Add Vertex");
        System.out.println(polygon.toString());

        boolean a  = polygon.addVertex(new Point(10, 4), 2);
        if (a ) 
            System.out.println("\t OK - expected true actual=  "+a+" --- polygon.addVertex(new Point(10, 4), 2))");
        else
            System.out.println("\t ERROR - expected true actual=  "+a+" --- polygon.addVertex(new Point(10, 4), 2))");
        System.out.println(polygon.toString());


        boolean a1 = polygon.addVertex(new Point(1, 4), 5);
        if (a1) 
            System.out.println("\t OK - expected true actual=  "+a1+" --- polygon.addVertex(new Point(1, 4), 5))");
        else
            System.out.println("\t ERROR - expected true actual=  "+a1+" --- polygon.addVertex(new Point(1, 4), 5))");
        System.out.println(polygon.toString());
        
        boolean a2 = polygon.addVertex(new Point(1, 4), 10);
        if (a2) 
            System.out.println("\t ERROR - expected true actual=  "+a2+" --- polygon.addVertex(new Point(1, 4), 10))");
        else
            System.out.println("\t OK - expected false actual= "+a2+" --- polygon.addVertex(new Point(1, 4), 10))");        
        System.out.println(polygon.toString());
        System.out.println("-------------------------------------------------------------------------------");
        System.out.println("polygon1.toString()");
        Polygon polygon1 = new Polygon();
        System.out.println(polygon1.toString());
        polygon1.addVertex(new Point(2, 1), 1);
        System.out.println(polygon1.toString());
        polygon1.addVertex(new Point(5, 0), 2);
        System.out.println(polygon1.toString());
        polygon1.addVertex(new Point(7, 5), 3);
        System.out.println(polygon1.toString());
        polygon1.addVertex(new Point(4, 6), 4);
        System.out.println(polygon1.toString());
        polygon1.addVertex(new Point(2, 4), 5);
        System.out.println(polygon1.toString());
        polygon1.addVertex(new Point(5, 8), 6);
        System.out.println(polygon1.toString());
        polygon1.addVertex(new Point(7, 312), 7);
        System.out.println(polygon1.toString());
        polygon1.addVertex(new Point(4, 64), 8);
        System.out.println(polygon1.toString());
        polygon1.addVertex(new Point(22, 6), 9);    
        System.out.println(polygon1.toString());
        polygon1.addVertex(new Point(22, 256), 10); 
        System.out.println( polygon1.toString());
            
        
        Polygon polygon22 = new Polygon(); 
        polygon22.addVertex(new Point(2, 1), 1); 
        polygon22.addVertex(new Point(5, 0), 2); 
        polygon22.addVertex(new Point(7, 5), 3); 
        polygon22.addVertex(new Point(4, 6), 4); 
        polygon22.addVertex(new Point(1, 4), 5);  
        
        
        double sumPerimeter = new Point(2,1).distance(new Point(5,0)) 
                            + new Point(5,0).distance(new Point(7,5))
                            + new Point(7,5).distance(new Point(4,6))
                            + new Point(4,6).distance(new Point(1,4))
                            + new Point(1,4).distance(new Point(2,1));
                            
        System.out.println("-------------------------------------------------------------------------------");

        System.out.println("polygon.calcPerimeter:");
        if (sumPerimeter == polygon22.calcPerimeter())
            {System.out.println("\t OK - expected "+ sumPerimeter +" actual= " + polygon22.calcPerimeter());}
        else
            {System.out.println("\t ERROR - expected "+ sumPerimeter +" actual= " + polygon22.calcPerimeter());}
            
          
        System.out.println("-------------------------------------------------------------------------------");
        System.out.println("polygon.findVertex:");
        int f = polygon1.findVertex(new Point(22, 256));
        int f1 = polygon1.findVertex(new Point(5, 8));
        int f2 = polygon1.findVertex(new Point(115, 118));
        if ( f == 10)
            System.out.println("\t OK - expected 10 actual= " + f+"  polygon1.findVertex(new Point(22.0, 256.0))=" + f);
        else
            {System.out.println("\t ERROR - expected 10 actual= " + f +"  polygon1.findVertex(new Point(22.0, 256.0)) =" + f);}
        
        if (f1 == 6)
            System.out.println("\t OK - expected 6 actual= " + f1+"  polygon1.findVertex(new Point(5, 8)))=" + f1);
        else
            System.out.println("\t ERROR - expected 6 actual= " + f1 +"  polygon1.findVertex(new Point(5, 8)) =" + f1);


        if ( f2 == -1)
            System.out.println("\t OK - expected -1 actual= " + f2+"  polygon1.findVertex(new Point(115, 118)))=" + f2);
        else
            System.out.println("\t ERROR - expected -1 actual= " + f2 +"  polygon1.findVertex(new Point(115, 118)) =" + f2);



        
        System.out.println("-------------------------------------------------------------------------------");
        System.out.println("polygon.getNextVertex:");
        if (!polygon1.getNextVertex(new Point(22, 256)).equals(new Point(2, 1)))
            System.out.println("\t ERROR - expected (2.0, 1.0) actual= " + polygon1.getNextVertex(new Point(22.0, 256.0))+"  polygon1.getNextVertex(new Point(22.0, 256.0)) =" + polygon1.getNextVertex(new Point(22, 256)));
        else
            System.out.println("\t OK - expected (2.0, 1.0) actual= " + polygon1.getNextVertex(new Point(22, 256))+"  polygon1.getNextVertex(new Point(22.0, 256.0))=" + polygon1.getNextVertex(new Point(22, 256)));

        if (!polygon1.getNextVertex(new Point(4, 6)).equals(new Point(2, 4)))
            System.out.println("\t ERROR - expected (2.0, 4.0) actual= " + polygon1.getNextVertex(new Point(4, 6))+"  polygon1.getNextVertex(new Point(4, 6)) =" + polygon1.getNextVertex(new Point(4, 6)));
        else
            System.out.println("\t OK - expected (2.0, 4.0) actual= " + polygon1.getNextVertex(new Point(4, 6))+"  polygon1.getNextVertex(new Point(4, 6))=" + polygon1.getNextVertex(new Point(4, 6)));
        
        if (!polygon1.getNextVertex(new Point(2, 1)).equals(new Point(5, 0)))
            System.out.println("\t ERROR - expected (5.0, 0.0) actual= " + polygon1.getNextVertex(new Point(2, 1)) + "  polygon1.getNextVertex(new Point(4, 6)) =" + polygon1.getNextVertex(new Point(4, 6)));
        else
            System.out.println("\t OK - expected (5.0, 0.0) actual= " + polygon1.getNextVertex(new Point(2, 1)) + "  polygon1.getNextVertex(new Point(4, 6))=" + polygon1.getNextVertex(new Point(4, 6)));

     
        System.out.println("-------------------------------------------------------------------------------");
        
        
        Polygon polygon1111 = new Polygon(); 
        polygon1111.addVertex(new Point(2, 1), 1); 
        polygon1111.addVertex(new Point(5, 0), 2); 
        polygon1111.addVertex(new Point(7, 5000), 3); 
        polygon1111.addVertex(new Point(4, 6), 4); 
        polygon1111.addVertex(new Point(2, 4), 5); 
        polygon1111.addVertex(new Point(5, 8), 6); 
        polygon1111.addVertex(new Point(7, 312), 7); 
        polygon1111.addVertex(new Point(4, 64), 8); 
        polygon1111.addVertex(new Point(22, 6), 9);  
        polygon1111.addVertex(new Point(22, 256), 10);   
        
        
        System.out.println("polygon.highestVertex:");

        Point p = polygon.highestVertex();
        if (p.equals(new Point(4,6)))
            System.out.println("\t OK - expected (4.0,6.0) actual= " + p.toString()+"  polygon.highestVertex() = " + p.toString());
        else
            System.out.println("\t ERROR - expected (4.0,6.0) actual= " + p.toString()+"  polygon.highestVertex() = " + p.toString());

        p = polygon1111.highestVertex();
        if (p.equals(new Point(7, 5000)))
            System.out.println("\t OK - expected (7, 5000) actual= " +p.toString()+"  polygon1.highestVertex() = " + p.toString());
        else
            System.out.println("\t ERROR - expected (7, 5000) actual= " + p.toString()+"  polygon1.highestVertex() = " + p.toString());




    

        polygon22 = new Polygon(); 
        polygon22.addVertex(new Point(2, 1), 1); 
        polygon22.addVertex(new Point(5, 0), 2); 
        polygon22.addVertex(new Point(7, 5), 3); 
        polygon22.addVertex(new Point(4, 6), 4); 
        polygon22.addVertex(new Point(1, 4), 5);  
        
        
        sumPerimeter = new Point(2,1).distance(new Point(5,0)) 
                     + new Point(5,0).distance(new Point(7,5))
                     + new Point(7,5).distance(new Point(4,6))
                     + new Point(4,6).distance(new Point(1,4))
                     + new Point(1,4).distance(new Point(2,1));
        System.out.println("-------------------------------------------------------------------------------");

        System.out.println("polygon.calcPerimeter:");
        if (sumPerimeter == polygon22.calcPerimeter())
            System.out.println("\t OK - expected "+ sumPerimeter +" actual= " + polygon22.calcPerimeter());
        else
            System.out.println("\t ERROR - expected "+ sumPerimeter +" actual= " + polygon22.calcPerimeter());

 
        
        double sumArea = 22.499999999999990;
        double sumArea2 = 22.500000000000009;
        System.out.println("-------------------------------------------------------------------------------");

        System.out.println("polygon.calcArea:");
        if (polygon22.calcArea() >= sumArea &&  polygon22.calcArea() <= sumArea2)
            System.out.println("\t OK - expected "+ 22.499999999999990 +" - " +22.500000000000009 +" actual= " + polygon22.calcArea());
        else
            System.out.println("\t ERROR - expected "+ 22.49999999999999 +" - " +22.500000000000009 +" actual= " +  polygon22.calcArea());

        //      
        

    
        Polygon polygon0 = new Polygon();
        System.out.println("-------------------------------------------------------------------------------");

        System.out.println("polygon0.toString()"); 
        System.out.println(polygon0.toString());

        System.out.println("polygon.findVertex:");
        if ( polygon0.findVertex(new Point(22, 256)) == -1)
            System.out.println("\t OK - expected -1 actual= " + polygon0.findVertex(new Point(22, 256))+"  polygon0.findVertex(new Point(22.0, 256.0))=" + polygon0.findVertex(new Point(22, 256)));
        else
            System.out.println("\t ERROR - expected -1 actual= " + polygon0.findVertex(new Point(22.0, 256))+"  polygon0.findVertex(new Point(22.0, 256.0)) =" + polygon0.findVertex(new Point(22, 256)));

    
        System.out.println("polygon.highestVertex():");
        if (!(polygon0.highestVertex() == null))
            System.out.println("\t ERROR - expected null actual= " + polygon0.highestVertex()+"  polygon0.highestVertex() =" + polygon0.highestVertex());
        else
            System.out.println("\t OK - expected null actual= " + polygon0.highestVertex()+"  polygon0.highestVertex()=" + polygon0.highestVertex());

        
        System.out.println("polygon.getNextVertex:");
        if (!(polygon0.getNextVertex(new Point(22, 256)) == null))
            System.out.println("\t ERROR - expected null actual= " + polygon0.getNextVertex(new Point(22.0, 256.0))+"  polygon0.getNextVertex(new Point(22.0, 256.0)) =" + polygon0.getNextVertex(new Point(22, 256)));
        else
            System.out.println("\t OK - expected null actual= " + polygon0.getNextVertex(new Point(22, 256))+"  polygon0.getNextVertex(new Point(22.0, 256.0))=" + polygon0.getNextVertex(new Point(22, 256)));

        
        
        System.out.println("polygon.getBoundingBox:");
        if (polygon0.getBoundingBox() != null)
            System.out.println("\t ERROR - expected null actual= " + polygon0.getBoundingBox( )+"  polygon0.getBoundingBox( ) =" + polygon0.getBoundingBox( ));
        else
            System.out.println("\t OK - expected null actual= " + polygon0.getBoundingBox( )+"  polygon0.getBoundingBox( )=" + polygon0.getBoundingBox( ));

    
        System.out.println("polygon0.calcPerimeter():");
        if (!(polygon0.calcPerimeter() == 0))
            System.out.println("\t ERROR - expected 0 actual= " + polygon0.calcPerimeter()+" polygon0.calcPerimeter() =" + polygon0.calcPerimeter());
        else
            System.out.println("\t OK - expected 0 actual= " + polygon0.calcPerimeter()+" polygon0.calcPerimeter()=" + polygon0.calcPerimeter());

    
        System.out.println("polygon0.calcArea():");
        if (!(polygon0.calcArea() == 0))
            System.out.println("\t ERROR - expected 0 actual= " + polygon0.calcArea()+" polygon0.calcArea() =" + polygon0.calcArea());
        else
            System.out.println("\t OK - expected 0 actual= " + polygon0.calcArea()+" polygon0.calcArea()=" + polygon0.calcArea());

        


        System.out.println("-------------------------------------------------------------------------------");
        polygon0.addVertex(new Point(2, 1), 1);

        System.out.println("polygon0.toString()"); 
        System.out.println(polygon0.toString());

        System.out.println("polygon.getNextVertex:");
        if (!polygon0.getNextVertex(new Point(2.0, 1.0)).equals(new Point(2.0, 1.0)))
            System.out.println("\t ERROR - expected (2.0, 1.0) actual= " + polygon0.getNextVertex(new Point(2.0, 1.0))+"  polygon0.getNextVertex(new Point(2.0, 1.0)) =" + polygon0.getNextVertex(new Point(2.0, 1.0)));
        else
            System.out.println("\t OK - expected (2.0, 1.0) actual= " + polygon0.getNextVertex(new Point(2.0, 1.0))+"  polygon0.getNextVertex(new Point(2.0, 1.0))=" + polygon0.getNextVertex(new Point(2.0, 1.0)));

        

        System.out.println("polygon.highestVertex():");
        if (!polygon0.highestVertex().equals(new Point(2, 1)))
            System.out.println("\t ERROR - expected (2.0, 1.0) actual= " + polygon0.highestVertex()+"  polygon0.highestVertex() =" + polygon0.highestVertex());
        else
            System.out.println("\t OK - expected (2.0, 1.0) actual= " + polygon0.highestVertex()+"  polygon0.highestVertex()=" + polygon0.highestVertex());

        
        System.out.println("polygon.getBoundingBox:");
        if (polygon0.getBoundingBox() != null)
            System.out.println("\t ERROR - expected null actual= " + polygon0.getBoundingBox( )+"  polygon0.getBoundingBox( ) =" + polygon0.getBoundingBox( ));
        else
            System.out.println("\t OK - expected null actual= " + polygon0.getBoundingBox( )+"  polygon0.getBoundingBox( )=" + polygon0.getBoundingBox( ));

        
        System.out.println("polygon0.calcPerimeter():");
        if (!(polygon0.calcPerimeter() == 0))
            System.out.println("\t ERROR - expected 0 actual= " + polygon0.calcPerimeter()+" polygon0.calcPerimeter() =" + polygon0.calcPerimeter());
        else
            System.out.println("\t OK - expected 0 actual= " + polygon0.calcPerimeter()+" polygon0.calcPerimeter()=" + polygon0.calcPerimeter());

        
        
        System.out.println("polygon0.calcArea():");
        if (!(polygon0.calcArea() == 0))
            System.out.println("\t ERROR - expected 0 actual= " + polygon0.calcArea()+" polygon0.calcArea() =" + polygon0.calcArea());
        else
            System.out.println("\t OK - expected 0 actual= " + polygon0.calcArea()+" polygon0.calcArea()=" + polygon0.calcArea());

    
        System.out.println("-------------------------------------------------------------------------------");
        


        polygon0.addVertex(new Point(7, 4), 2);


        System.out.println("polygon0.toString()"); 
        System.out.println(polygon0.toString());

        System.out.println("polygon.getNextVertex:");
        if (!polygon0.getNextVertex(new Point(2.0, 1.0)).equals(new Point(7.0, 4.0)))
            System.out.println("\t ERROR - expected (7.0, 4.0) actual= " + polygon0.getNextVertex(new Point(2.0, 1.0))+"  polygon0.getNextVertex(new Point(2.0, 1.0)) =" + polygon0.getNextVertex(new Point(2.0, 1.0)));
        else
            System.out.println("\t OK - expected (7.0, 4.0) actual= " + polygon0.getNextVertex(new Point(2.0, 1.0))+"  polygon0.getNextVertex(new Point(2.0, 1.0))=" + polygon0.getNextVertex(new Point(2.0, 1.0)));
        

        System.out.println("polygon.highestVertex():");
        if (!polygon0.highestVertex().equals(new Point(7, 4)))
            System.out.println("\t ERROR - expected (7.0, 4.0) actual= " + polygon0.highestVertex()+"  polygon0.highestVertex() =" + polygon0.highestVertex());
        else
            System.out.println("\t OK - expected (7.0, 4.0) actual= " + polygon0.highestVertex()+"  polygon0.highestVertex()=" + polygon0.highestVertex());
        

        if (!polygon0.getNextVertex(new Point(7.0, 4.0)).equals(new Point(2.0, 1.0)))
            System.out.println("\t ERROR - expected (2.0, 1.0) actual= " + polygon0.getNextVertex(new Point(7.0, 4.0))+"  polygon0.getNextVertex(new Point(7.0, 4.0)) =" + polygon0.getNextVertex(new Point(7.0, 4.0)));
        else
            System.out.println("\t OK - expected (2.0, 1.0) actual= " + polygon0.getNextVertex(new Point(7.0, 4.0))+"  polygon0.getNextVertex(new Point(7.0, 4.0))=" + polygon0.getNextVertex(new Point(7.0, 4.0)));

        System.out.println("polygon.getBoundingBox:");
        if (polygon0.getBoundingBox() != null)
            System.out.println("\t ERROR - expected null actual= " + polygon0.getBoundingBox( )+"  polygon0.getBoundingBox( ) =" + polygon0.getBoundingBox( ));
        else
            System.out.println("\t OK - expected null actual= " + polygon0.getBoundingBox( )+"  polygon0.getBoundingBox( )=" + polygon0.getBoundingBox( ));
        

        System.out.println("polygon0.calcPerimeter():");
        if (!(polygon0.calcPerimeter() ==  5.830951894845301 ))
            System.out.println("\t ERROR - expected  5.830951894845301  actual= " + polygon0.calcPerimeter()+" polygon0.calcPerimeter() =" + polygon0.calcPerimeter());
        else
            System.out.println("\t OK - expected 5.830951894845301  actual= " + polygon0.calcPerimeter()+" polygon0.calcPerimeter()=" + polygon0.calcPerimeter());

        System.out.println("polygon0.calcArea():");
        if (!(polygon0.calcArea() == 0))
            System.out.println("\t ERROR - expected 0 actual= " + polygon0.calcArea()+" polygon0.calcArea() =" + polygon0.calcArea());
        else
            System.out.println("\t OK - expected 0 actual= " + polygon0.calcArea()+" polygon0.calcArea()=" + polygon0.calcArea());

    

        System.out.println("-------------------------------------------------------------------------------");

        polygon0.addVertex(new Point(10, 14), 3);
        System.out.println("polygon0.toString()"); 
        System.out.println(polygon0.toString());

        System.out.println("polygon.getNextVertex:");
        if (!polygon0.getNextVertex(new Point(7.0, 4.0)).equals(new Point(10.0, 14.0)))
            System.out.println("\t ERROR - expected (10.0, 14.0) actual= " + polygon0.getNextVertex(new Point(7.0, 4.0))+"  polygon0.getNextVertex(new Point(7.0, 4.0)) =" + polygon0.getNextVertex(new Point(7.0, 4.0)));
        else
            System.out.println("\t OK - expected (10.0, 14.0) actual= " + polygon0.getNextVertex(new Point(7.0, 4.0))+"  polygon0.getNextVertex(new Point(7.0, 4.0))=" + polygon0.getNextVertex(new Point(7.0, 4.0)));


        System.out.println("polygon.highestVertex():");
        if (!polygon0.highestVertex().equals(new Point(10, 14)))
            System.out.println("\t ERROR - expected (10.0, 14.0) actual= " + polygon0.highestVertex()+"  polygon0.highestVertex() =" + polygon0.highestVertex());
        else
            System.out.println("\t OK - expected (10.0, 14.0) actual= " + polygon0.highestVertex()+"  polygon0.highestVertex()=" + polygon0.highestVertex());
        
        
        System.out.println("polygon.getBoundingBox:");
        System.out.println("The polygon has 4 vertices:\n((2.0,1.0),(10.0,1.0),(10.0,14.0),(2.0,14.0))");
        System.out.println(polygon0.getBoundingBox().toString());
        
    
        System.out.println("polygon0.calcPerimeter():");
        if (!(polygon0.calcPerimeter() == 31.535595926229597))
            System.out.println("\t ERROR - expected 31.535595926229597 actual= " + polygon0.calcPerimeter()+" polygon0.calcPerimeter() =" + polygon0.calcPerimeter());
        else
            System.out.println("\t OK - expected 31.535595926229597 actual= " + polygon0.calcPerimeter()+" polygon0.calcPerimeter()=" + polygon0.calcPerimeter());


        System.out.println("polygon0.calcArea():");
        double calcArea =20.49999999999999 , calcArea1 =20.5000000000005 ;
        if (!(polygon0.calcArea() < calcArea1 && polygon0.calcArea() > calcArea))
            System.out.println("\t ERROR - expected aprox 20.499999999999993 actual= " + polygon0.calcArea()+" polygon0.calcArea() =" + polygon0.calcArea());
        else
            System.out.println("\t OK - expected aprox 20.499999999999993 actual= " + polygon0.calcArea()+" polygon0.calcArea()=" + polygon0.calcArea());
        
        System.out.println("-------------------------------------------------------------------------------");

        polygon0.addVertex(new Point(6, 8), 4);
        System.out.println("polygon0.toString()"); 
        System.out.println(polygon0.toString());

        System.out.println("polygon.getNextVertex:");
        if (!polygon0.getNextVertex(new Point(10.0, 14.0)).equals(new Point(6.0, 8.0)))
            System.out.println("\t ERROR - expected (6.0, 8.0) actual= " + polygon0.getNextVertex(new Point(10.0, 14.0))+"  polygon0.getNextVertex(new Point(10.0, 14.0)) =" + polygon0.getNextVertex(new Point(10.0, 14.0)));
        else
            System.out.println("\t OK - expected (6.0, 8.0) actual= " + polygon0.getNextVertex(new Point(10.0, 14.0))+"  polygon0.getNextVertex(new Point(10.0, 14.0))=" + polygon0.getNextVertex(new Point(10.0, 14.0)));


        System.out.println("polygon.highestVertex():");
        if (!polygon0.highestVertex().equals(new Point(10, 14)))
            System.out.println("\t ERROR - expected (10.0, 14.0) actual= " + polygon0.highestVertex()+"  polygon0.highestVertex() =" + polygon0.highestVertex());
        else
            System.out.println("\t OK - expected (10.0, 14.0) actual= " + polygon0.highestVertex()+"  polygon0.highestVertex()=" + polygon0.highestVertex());

        
        System.out.println("polygon.getBoundingBox:");
        System.out.println("The polygon has 4 vertices:\n((2.0,1.0),(10.0,1.0),(10.0,14.0),(2.0,14.0))");
        System.out.println(polygon0.getBoundingBox().toString());

        
        System.out.println("polygon0.calcPerimeter():");
        if (!(polygon0.calcPerimeter() == 31.54461870298238))
            System.out.println("\t ERROR - expected 31.54461870298238 actual= " + polygon0.calcPerimeter()+" polygon0.calcPerimeter() =" + polygon0.calcPerimeter());
        else
            System.out.println("\t OK - expected 31.54461870298238 actual= " + polygon0.calcPerimeter()+" polygon0.calcPerimeter()=" + polygon0.calcPerimeter());

        
        System.out.println("polygon0.calcArea():");
        
        calcArea =22.4999999999999 ;
        calcArea1 =22.5000000000005 ;
        if (!(polygon0.calcArea() < calcArea1 && polygon0.calcArea() > calcArea))
            System.out.println("\t ERROR - expected aprox 22.499999999999993 actual= " + polygon0.calcArea()+" polygon0.calcArea() =" + polygon0.calcArea());
        else
            System.out.println("\t OK - expected aprox 22.499999999999993 actual= " + polygon0.calcArea()+" polygon0.calcArea()=" + polygon0.calcArea());



     
    }

}
