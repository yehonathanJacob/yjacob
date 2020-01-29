package Q2.ClientSide;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.net.InetAddress;
import java.net.MulticastSocket;
import java.net.UnknownHostException;

/**
 * Class that present the Client GUI
 */
public class ClientGUI extends JFrame {
    //Instance variable
    private InetAddress address;
    private int port;
    private MulticastSocket socket;
    private JTextArea Output;
    private ClientListener cl;

    /**
     * default and only contractor
     * set the defult group the client is listening to.
     * @param port the default port to be connected to.
     * @param host the default address to be connected to.
     */
    public ClientGUI(int port,InetAddress host){
        super("Client");

        try{
            this.port = port;
            this.address = host;
            socket = new MulticastSocket(this.port);
            System.out.printf("Adrres: "+host.toString()+"%n");
            socket.joinGroup(host);
        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        JPanel header = new JPanel();
        header.add(new JLabel("Set Server: port:"));
        JTextField portInput = new JTextField(null,4);
        portInput.setText(port+"");
        portInput.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        header.add(portInput);
        header.add(new JLabel("server:"));
        JTextField serverInput = new JTextField(null,20);
        serverInput.setText(address.toString());
        serverInput.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        header.add(serverInput);
        JButton setListen = new JButton("set");
        setListen.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                SetListen(portInput.getText(),serverInput.getText());
            }
        });
        header.add(setListen);
        add(header,BorderLayout.NORTH);

        Output = new JTextArea("News:\n");
        Output.setEditable(false);
        Output.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        add(Output,BorderLayout.CENTER);

        JButton clear = new JButton("clear");
        clear.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                Output.setText("");
            }
        });

        add(clear,BorderLayout.SOUTH);

        setVisible(true);
        pack();
        setMinimumSize(new Dimension(getWidth(),getHeight()));
        setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        addWindowListener(new java.awt.event.WindowAdapter() {
            @Override
            public void windowClosing(java.awt.event.WindowEvent windowEvent) {
                exitFunction();
            }
        });

        cl = new ClientListener(socket,Output);
        cl.start();

    }

    /**
     * function to be called when want to terminate the function
     */
    private void exitFunction(){
        try{
            cl.isAlive=false;
            cl.interrupt();
            socket.leaveGroup(address);
        } catch (IOException e) {
            e.printStackTrace();
        }
        socket.close();
        setVisible(false);
        dispose();

    }


    /**
     * fucntion to change where the client is listening to
     * first leave old group, and then enter to new group
     * @param port
     * @param addrres
     */
    private void SetListen(String port,String addrres){
        try{
            cl.isAlive = false;
            cl.interrupt();
            socket.leaveGroup(this.address);
        } catch (IOException e) {
        }
        try{
            this.address = InetAddress.getByName(addrres.replaceAll("/",""));
            this.port = Integer.parseInt(port);
            socket = new MulticastSocket(this.port);
            socket.joinGroup(address);
            cl = new ClientListener(socket,Output);
            cl.start();
        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
