package Q2.ServerSide;

import Q2.ClientSide.ClientGUI;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.net.*;

/**
 * class that contain all the server GUI, and the functionality
 */
public class ServerGUI extends JFrame {
    //instance variable
    private InetAddress address;
    private int port;
    private DatagramSocket socket;
    private JTextArea Output;

    /**
     * Constructor for the GUI + set the socket to send the message to
     * @param port the port of the server.
     * @param ComputerName the IP address to be set on
     */
    public ServerGUI(int port,String ComputerName){
        super(ComputerName);

        try{
            byte[] buf = new byte[256];
            this.port = port;
            address = InetAddress.getByName(ComputerName);
            socket = new DatagramSocket();
            DatagramPacket packet = new DatagramPacket(buf,buf.length,address,port);
            socket.send(packet);
            System.out.printf("Server is ready%n");
        } catch (SocketException e) {
            e.printStackTrace();
            System.exit(1);
        } catch (UnknownHostException e) {
            e.printStackTrace();
            System.exit(1);
        } catch (IOException e) {
            e.printStackTrace();
        }

        JPanel header = new JPanel();
        header.setLayout(new BorderLayout());
        JButton sendBt = new JButton("Send");
        header.add(sendBt,BorderLayout.WEST);
        TextField Input = new TextField();
        Input.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        header.add(Input,BorderLayout.CENTER);
        add(header,BorderLayout.NORTH);
        sendBt.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                sendMessage(Input.getText());
            }
        });

        Output = new JTextArea("Server Log:\nServer ready over port"+this.port+"\n");
        Output.setEditable(false);
        Output.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        Output.setBackground(Color.darkGray);
        Output.setForeground(Color.white);
        add(Output,BorderLayout.CENTER);

        JButton addUser = new JButton("Add User");
        addUser.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                createUser();
            }
        });
        add(addUser,BorderLayout.SOUTH);

        setVisible(true);
        setSize(400,400);
        setMinimumSize(new Dimension(getWidth(),getHeight()));
        setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        addWindowListener(new java.awt.event.WindowAdapter() {
            @Override
            public void windowClosing(java.awt.event.WindowEvent windowEvent) {
                exitFunction();
            }
        });

    }

    /**
     * function to send message.
     * The packet is getting sent to over the port is set, and from the address is set.
     * Every client who listen to this port, and accept packet from this address will get the packet.
     * @param message The message in String.
     */
    private void sendMessage(String message){
        DatagramPacket packet;
        byte[] buf;
        buf = message.getBytes();
        try{
            packet = new DatagramPacket(buf,buf.length,address,port);
            socket.send(packet);
            Output.append("Sent: "+message+"\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * function to log off the server and the socket of it.
     */
    private void exitFunction(){
        sendMessage("Shutting server down");
        socket.close();
        setVisible(false);
        dispose();
    }

    /**
     * A function just to create a new client frame with this serer's port + address as default.
     */
    private void createUser(){
        ClientGUI cp = new ClientGUI(7777,address);
    }

}
