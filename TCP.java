package com.example.l.watch;

import android.util.Log;
import android.widget.Button;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.UnknownHostException;


public class TCP {

    private String IP="192.168.43.232";
    private int PORT=2334;
    public Socket socket;
    private int correct=0;
    public String res=" ";

    public int connect() {
        new Thread() {
            @Override
            public void run() {
                try {
                    socket = new Socket();
                    socket.connect(new InetSocketAddress(IP, PORT), 5000);
                    correct=1;
                }
                catch (UnknownHostException e) {
                    e.printStackTrace();
                }
                catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }.start();
        return 1;
    }

    public String send(final String msg) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    //获取输出流，通过这个流发送消息
                    DataOutputStream out = new DataOutputStream(socket.getOutputStream());
                    //发送文字消息
                    byte[] bytes = msg.getBytes();
                    out.write(bytes);
                    InputStream istream=socket.getInputStream();
                    byte b[]=new byte[10];
                    istream.read(b);
                    res = new String(b);

                    Log.v("info",res);

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();
        return res;
    }

    public void stop() {
        try {
            socket.close();
        }
        catch(IOException e){
            return;
        }
    }
}