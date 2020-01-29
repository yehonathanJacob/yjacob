package Q2.ClientSide;

import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.MulticastSocket;
import java.util.Date;

/**
 * after the group is getting set. this class work in a thread to wait for new News
 */
public class ClientListener extends Thread {
    //instace variable
    public boolean isAlive;
    private MulticastSocket socket;
    private DatagramPacket packet;
    private JTextArea Output;

    /**
     * Contractor of the listener
     * @param socket the socket to listening to.
     * @param Output where to output the received data
     */
    public ClientListener(MulticastSocket socket, JTextArea Output){
        this.socket = socket;
        isAlive =true;
        this.Output = Output;
    }

    @Override
    public void run() {
        byte[] buf = new byte[256];
        String message;
        while (isAlive){
            synchronized (this){
                try {
                    packet = new DatagramPacket(buf,buf.length);
                    socket.receive(packet);
                    buf = packet.getData();
                    message = (new String(buf)).substring(0,packet.getLength());
                    message = new Date().toString() +": "+ message;
                    Output.append(message+"\n");
                } catch (IOException e) {
                    if (! socket.isClosed())
                        e.printStackTrace();
                }
            }
        }
    }
}
