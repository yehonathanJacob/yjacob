package Q1.ClientSide;

import java.awt.*;
import java.io.BufferedReader;
import java.io.IOException;

/**
 * class that run as a thread to listen to new message from servers
 */
public class ClientListener extends Thread {
    //instance variable
    private BufferedReader ServerInput;
    private TextArea ClientOutput;
    private String ClientStart;

    /**
     * Comstactor to set in Input and the Output of the client to transfer the data from server
     * @param Input
     * @param txtOutput
     * @param ClientName
     */
    public ClientListener(BufferedReader Input, TextArea txtOutput,String ClientName){
        ServerInput = Input;
        ClientOutput = txtOutput;
        ClientStart = ""+ClientName+": ";
    }

    @Override
    public synchronized void run() {
        try{
            String ServetMessage;
            while ((ServetMessage = ServerInput.readLine()) != null)
            {
                synchronized (ServetMessage){
                    if (ServetMessage.indexOf(ClientStart) < 0){
                        ClientOutput.append(ServetMessage+"\n");
                    }else{
                        ClientOutput.append(ServetMessage.replace(ClientStart,"You:")+"\n");
                    }
                }
            }
        }catch (IOException e){}
    }
}
