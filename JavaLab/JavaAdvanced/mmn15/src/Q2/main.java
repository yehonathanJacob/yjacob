package Q2;
import Q2.B.*;
import Q2.C.*;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class main {
    /**
     * Task A: two process work together in the same time. one to get 10 times the position, and second is two set 10 times the position
     * Task B: two process work together in synchronized, so after each move/get there is one get/move.
     * Task C: two type of process, 4 of ech, work in the way that one can be made when ever second dos'nt work. but second can work only when he is alone.
     */
    public static void main(String[] args) {

        System.out.printf("###### Start task A #####%n");
        SharedData sd = new SharedData(0,0);
        Process1 p1 = new Process1(sd);
        Process2 p2 = new Process2(sd);
        ExecutorService executor = Executors.newCachedThreadPool();
        executor.execute(p1);
        executor.execute(p2);
        executor.shutdown();
        try{
            executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
        }catch (InterruptedException e){
            System.out.printf("Error: %s%n",e.getMessage());
        }
        System.out.printf("###### End task A #####%n");


        System.out.printf("###### Start task B #####%n");
        SharedDataB sdB = new SharedDataB(0,0);
        Process1 p1B = new Process1(sdB);
        Process2 p2B = new Process2(sdB);
        executor = Executors.newCachedThreadPool();
        executor.execute(p1B);
        executor.execute(p2B);
        executor.shutdown();
        try{
            executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
        }catch (InterruptedException e){
            System.out.printf("Error: %s%n",e.getMessage());
        }
        System.out.printf("###### End task B #####%n");

        System.out.printf("###### Start task C #####%n");
        SharedDataC sdC = new SharedDataC(0,0);
        executor = Executors.newCachedThreadPool();
        for (int i=0;i<4;i++){
            executor.execute(new Process1(sdC));
            executor.execute(new Process2(sdC));
        }
        executor.shutdown();
        try{
            executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
        }catch (InterruptedException e){
            System.out.printf("Error: %s%n",e.getMessage());
        }
        System.out.printf("###### End task C #####%n");

    }
}
