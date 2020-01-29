package Q1.ClientSide;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.WindowEvent;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.*;
import java.util.Map;

/**
 * Client class to create the GUI and all the function of it
 */
public class ClientPanel extends JFrame {
    //instance variable
    private Socket echoSocket = null;
    private PrintWriter out = null;
    private BufferedReader in = null;
    private String host="localhost";
    private String ClientName;

    /**
     * Constructor to create the GUI and all the function in it
     * @param name name of the client
     * @param port port to listen to, the address of the host will be the "localhost"
     */
    public ClientPanel(String name, int port)
    {
        super(name);
        ClientName = name;
        String curuntly_log="curuntly log: ";
        try{
            echoSocket = new Socket(host, port);
            out = new PrintWriter(echoSocket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(
                    echoSocket.getInputStream()));
            out.println(name);
            curuntly_log += in.readLine();
        }
        catch (IOException e) {
            System.out.println("Couldn't get I/O for the connection to: "+host);
            dispatchEvent(new WindowEvent(this, WindowEvent.WINDOW_CLOSING));
        }

        JPanel header = new JPanel();
        header.setLayout(new BorderLayout());
        header.add(new JLabel("Input:"), BorderLayout.NORTH);
        TextField Input = new TextField("");
        Input.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        JButton sendBt = new JButton("Send");
        sendBt.addActionListener(new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                sendMessage(Input.getText());
            }
        });
        header.add(sendBt,BorderLayout.WEST);
        header.add(Input,BorderLayout.CENTER);
        add(header,BorderLayout.NORTH);

        JPanel body = new JPanel();
        body.setLayout(new BorderLayout());
        body.add(new JLabel("Output: "),BorderLayout.NORTH);
        TextArea Output = new TextArea("");
        Output.setFont(new Font(Font.SANS_SERIF,Font.PLAIN,18));
        Output.setEditable(false);
        body.add(Output,BorderLayout.CENTER);
        add(body,BorderLayout.CENTER);

        JButton exitBtn = new JButton("Log Out");
        exitBtn.addActionListener(new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                exitFunction();
            }
        });

        setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        addWindowListener(new java.awt.event.WindowAdapter() {
            @Override
            public void windowClosing(java.awt.event.WindowEvent windowEvent) {
                exitFunction();
            }
        });

        Output.append(curuntly_log+"\n");

        ClientListener cl = new ClientListener(in,Output,ClientName);
        cl.start();
        setSize(400,400);
    }

    /**
     * a function to send a message to the server thought the port
     * @param message
     */
    private void sendMessage(String message)
    {
        if (message != null && message.length() > 0)
            out.println(ClientName+": "+ message);
        else if(message == null) {
            out.println(ClientName+" is left");
            out.println(message);
            try{
                out.close();
                in.close();
                echoSocket.close();
                setVisible(false);
                dispose();
            }catch (IOException e){ }finally {
            }

        }
        else
            JOptionPane.showMessageDialog(null, "You can't send empty messamge","Bad Input",JOptionPane.ERROR_MESSAGE);
    }

    /**
     * function to log of from the server and to close GUI
     */
    private void exitFunction(){
        int res = JOptionPane.showConfirmDialog(null,
                "Would you like to log out?", "Close Window?",
                JOptionPane.YES_NO_CANCEL_OPTION,
                JOptionPane.QUESTION_MESSAGE);
        if (res == JOptionPane.YES_OPTION){
            //sendMessage("Client is leeving: "+ClientName);
            sendMessage(null);
        }

    }
}
