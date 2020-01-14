package Q1.ServerSide;

import Q1.ClientSide.ClientListener;
import Q1.ClientSide.ClientPanel;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * class of the server GUI and all the functionality on it.
 */
public class ServerPanel extends JFrame {
    //instance variable
    private ServerSocket serverSocket = null;
    private boolean listening = false;
    private int port;
    private Map<PrintWriter,String> allUser;
    private TextArea serverLog;

    /**
     * Default constructor for server GUI
     */
    public ServerPanel(){
        super("Server");
        while(!listening){
            port = (int)(Math.random()*1000)+1023;
            try{
                serverSocket = new ServerSocket(port);
                listening = true;
            }catch (IOException e){}
        }
        JPanel header = new JPanel();
        header.setLayout(new BorderLayout());
        header.add(new JLabel("Add new user: "),BorderLayout.NORTH);
        TextField Input = new TextField("");
        JButton AddUser = new JButton(" Add New User");
        AddUser.addActionListener(new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                addUser(Input.getText());
            }
        });
        header.add(AddUser,BorderLayout.WEST);
        Input.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));

        header.add(new JLabel("Server log: "),BorderLayout.SOUTH);
        header.add(Input,BorderLayout.CENTER);
        add(header,BorderLayout.NORTH);

        setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        addWindowListener(new java.awt.event.WindowAdapter() {
            @Override
            public void windowClosing(java.awt.event.WindowEvent windowEvent) {
                exitFunction();
            }
        });

        JButton closeServer = new JButton("Close Server");
        closeServer.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                exitFunction();
            }
        });
        add(closeServer ,BorderLayout.SOUTH);

        serverLog = new TextArea("Server is ready over port:"+port+"\n");
        serverLog.setEditable(false);
        serverLog.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        serverLog.setBackground(Color.darkGray);
        serverLog.setForeground(Color.white);
        add(serverLog,BorderLayout.CENTER);
        allUser = new HashMap<PrintWriter, String>();
        new ServerListener(serverSocket,allUser).start();
        setSize(400,400);
    }

    /**
     * a fnction to create new User GUI
     * @param Username
     */
    private void addUser(String Username){
        String message = "New user is entering: "+Username;
        printMessage(message);
        ClientPanel newClient = new ClientPanel(Username,port);
        newClient.setVisible(true);
    }

    /**
     * function to turn of the server and exit the System
     */
    private void exitFunction(){
        int res = JOptionPane.showConfirmDialog(null,
                "Are you sure you want to close the server?", "Close Window?",
                JOptionPane.YES_NO_CANCEL_OPTION,
                JOptionPane.QUESTION_MESSAGE);
        if (res == JOptionPane.YES_OPTION){
            listening = false;
            try{
                printMessage("Shutting down");
                printMessage(null);
                serverSocket.close();
                System.exit(0);
            }catch (IOException e ){}
        }

    }

    /**
     * the server listener that wait for new user
     */
    private class ServerListener extends Thread{
        private ServerSocket serverSocket = null;
        private Map<PrintWriter,String> allUser;
        public ServerListener(ServerSocket serverSocket,Map<PrintWriter,String> allUser){
            this.serverSocket = serverSocket;
            this.allUser = allUser;
        }

        @Override
        public void run() {
            Socket socket = null;
            while (listening){
                synchronized (serverSocket){
                    try{
                        socket = serverSocket.accept();
                        new EchoThread(socket,allUser).start();
                    }catch (IOException e){
                        if (listening)
                            serverLog.append("Accept faild");
                    }

                }
            }
        }
    }

    /**
     * the function that print out the message to all user that again to the server
     * @param message
     */
    private void printMessage(String message){
        if(message != null)
            serverLog.append(message+"\n");
        for (PrintWriter key: allUser.keySet()){
            key.println(message);
        }
    }

    /**
     * the listener that wait for new message from clients
     */
    private  class EchoThread extends Thread{
        private Socket socket = null;
        PrintWriter out;
        BufferedReader in;
        Map<PrintWriter,String> allUser;
        public EchoThread(Socket socket,Map<PrintWriter,String> allUser){
            this.socket = socket;
            allUser = allUser;
            try{
                out = new PrintWriter(socket.getOutputStream(), true);
                in = new BufferedReader(new InputStreamReader(
                        socket.getInputStream()));
                String name = in.readLine();
                String curently_log="";
                for (PrintWriter key:allUser.keySet())
                    curently_log+=allUser.get(key);
                out.println(curently_log);
                allUser.put(out,name);
            }catch(IOException e){
                serverLog.append("couldn't open I/O on connection");
            }
        }
        public void run(){
            String inputLine;
            try{

                while ((inputLine = in.readLine()) != null && inputLine!= "null") {
                    printMessage(inputLine);
                }
                out.close();
                in.close();
                socket.close();
            }catch(IOException e){
                System.out.println("couldn't read from connection");
            }
        }
    }

}
