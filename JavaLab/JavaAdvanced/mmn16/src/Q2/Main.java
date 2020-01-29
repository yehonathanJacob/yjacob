package Q2;

import Q2.ServerSide.ServerGUI;


public class Main {
    /**
     * create a srever to send news, over port 777 and a default address
     * @param args
     */
    public static void main(String[] args) {
        ServerGUI sp = new ServerGUI(7777,"230.0.0.1");
    }
}
