package com.example.l.watch;

import android.graphics.Color;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.TextView;
import java.text.DecimalFormat;
import android.support.wearable.activity.WearableActivity;

public class MainActivity extends WearableActivity implements View.OnClickListener, SensorEventListener {

    private SensorManager aManager;
    private Sensor aSensor;
    private SensorManager gManager;
    private Sensor gSensor;
    private float dx, dy, dz, temX, temY, temZ;
    private float ax, ay, az;
    private float gx, gy, gz;

    private Button btn_start;
    private int flag=0, Flag=0;

    private TextView dX;
    private TextView dY;
    private TextView dZ;
    private TextView order;
    private RelativeLayout Layout;

    private float q0 = 1, q1 = 0, q2 = 0, q3 = 0;
    private float exInt = 0, eyInt = 0, ezInt = 0;

    private int i=0;//i==300 传一次数据
    private int time=0;//2s 后确定设备
    private int device;
    private int[] Device;

    private TCP tcp;
    private Position man = new Position(50,75,75);
    private Position screen = new Position(0,150,75);
    private Position light = new Position(0,0,190);
    private Position car = new Position(0,0,0);

    @Override
    protected void onCreate(Bundle savedInstanceState) {


        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);   //应用运行时，保持屏幕高亮，不锁屏
        //accelerometer
        aManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        aSensor = aManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        aManager.registerListener(this, aSensor, SensorManager.SENSOR_DELAY_GAME);
        //gyroscope
        gManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        gSensor = gManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        gManager.registerListener(this, gSensor, SensorManager.SENSOR_DELAY_GAME);
        bindViews();
    }

    @Override
    protected void onDestroy() {
        tcp.stop();
        super.onDestroy();
        aManager.unregisterListener(this);
        gManager.unregisterListener(this);
    }

    @Override
    protected void onStop() {
        super.onStop();
        onDestroy();
    }


    private void bindViews() {
        btn_start = (Button) findViewById(R.id.btn_start);
        Layout = (RelativeLayout) findViewById(R.id.layout);
        dX = (TextView) findViewById(R.id.dx);
        dY = (TextView) findViewById(R.id.dy);
        dZ = (TextView) findViewById(R.id.dz);
        order = (TextView) findViewById(R.id.order);
        btn_start.setOnClickListener(this);
        Device = new int[100];
        tcp = new TCP();
        tcp.connect();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            if(Math.abs(ax - event.values[0])>5||Math.abs(ay - event.values[1])>5||Math.abs(az - event.values[2])>5){
                btn_start.setText("STOP");
                flag=1;
            }

            ax = event.values[0];
            ay = event.values[1];
            az = event.values[2];
        }
        else if (event.sensor.getType() == Sensor.TYPE_GYROSCOPE) {
            gx = event.values[0];
            gy = event.values[1];
            gz = event.values[2];
        }

        IMUupdate(gx, gy, gz, ax, ay, az);

        if(flag==1) {
            if(Flag==0){
                Log.v("infon",String.valueOf(Device[75]));
                tcp.send(String.valueOf(Device[75])+" \n");
                Flag=1;
            }

            DecimalFormat decimalFormat=new DecimalFormat(".00");
            String sax=decimalFormat.format(ax);
            String say=decimalFormat.format(ay);
            String saz=decimalFormat.format(az);
            String sgx=decimalFormat.format(gx);
            String sgy=decimalFormat.format(gy);
            String sgz=decimalFormat.format(gz);

            if(i<=294) {
                tcp.send(sax+' '+say+' '+saz+' '+sgx+' '+sgy+' '+sgz+" \n");
                i+=6;
            }
            else if(i==300){
                flag=0;
                Flag=0;
                i=0;
                try{Thread.sleep(200);}
                catch(InterruptedException e){};
                order.setText("order:"+tcp.res);
                btn_start.setText("START");
                Log.v("errorMain",tcp.res);
            }
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
    }

    @Override
    public void onClick(View v) {
        btn_start.setText("CONNECT");
        try{
            tcp.socket.close();
            tcp.connect();
        }
        catch(Exception e){
            Log.v("info","tcp error!");
        }
        flag=0;
        Flag=0;
        i=0;
    }

    void IMUupdate(float gx, float gy, float gz, float ax, float ay, float az) {

        float Kp = 2f;
        float Ki = 0.001f;
        float halfT = 0.01f;

        float norm;
        float vx, vy, vz;
        float ex, ey, ez;
        float temq0, temq1, temq2, temq3;

        //加速度传感器单位向量化
        norm = (float) Math.sqrt(ax * ax + ay * ay + az * az);
        ax = ax / norm;
        ay = ay / norm;
        az = az / norm;

        //陀螺仪积分得到的重力单位向量
        vx = 2 * (q1 * q3 - q0 * q2);
        vy = 2 * (q0 * q1 + q2 * q3);
        vz = q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3;

        //连个重力向量的叉积
        ex = (ay * vz - az * vy);
        ey = (az * vx - ax * vz);
        ez = (ax * vy - ay * vx);

        exInt = exInt + ex * Ki;
        eyInt = eyInt + ey * Ki;
        ezInt = ezInt + ez * Ki;

        gx = gx + Kp * ex + exInt;
        gy = gy + Kp * ey + eyInt;
        gz = gz + Kp * ez + ezInt;

        temq0 = q0;
        temq1 = q1;
        temq2 = q2;
        temq3 = q3;
        q0 = temq0 + (-temq1 * gx - temq2 * gy - temq3 * gz) * halfT;
        q1 = temq1 + (temq0 * gx + temq2 * gz - temq3 * gy) * halfT;
        q2 = temq2 + (temq0 * gy - temq1 * gz + temq3 * gx) * halfT;
        q3 = temq3 + (temq0 * gz + temq1 * gy - temq2 * gx) * halfT;

        norm = (float) Math.sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3);
        q0 = q0 / norm;
        q1 = q1 / norm;
        q2 = q2 / norm;
        q3 = q3 / norm;

        dz = (float)Math.atan2(2 * (q1 * q2 + q0 * q3),q0 * q0 + q1 * q1 - q2 * q2 - q3 * q3)* 57.3f; // yaw
        dz = dz/2;
        dy = (float)Math.asin(-2 * q1 * q3 + 2 * q0* q2)* 57.3f; // pitch
        dx = (float)Math.atan2(2 * q2 * q3 + 2 * q0 * q1, -2 * q1 * q1 - 2 * q2* q2 + 1)* 57.3f; // roll
//        dz = 2*(q1*q3-q0*q2);
//        dy = 2*(q1*q2+q0*q3);
//        dx = q1*q1+q0*q0-q3*q3-q2*q2;

        device = getDevice(dx, dy, dz);
        for(int i=0; i<99; i++){
            Device[i]=Device[i+1];
        }
        Device[99]=device;
        //Log.v("info",String.valueOf(device));
        String str0 = "dX: " + dx;
        String str1 = "dY: " + dy;
        String str2 = "dZ: " + dz;
        dX.setText(str0);
        dY.setText(str1);
        dZ.setText(str2);

    }


    public int GetDevice(float x, float y, float z){
        int temDevice=0;
        double a=Math.cos(y)*Math.cos(z)+Math.sin(y)*Math.sin(x)*Math.sin(z);
        double b=Math.cos(x)*Math.sin(z);
        double c=-Math.sin(y)*Math.cos(z)+Math.cos(y)*Math.sin(x)*Math.sin(z);
        if(time == 0 || time==1) {
            temX = x;
            temY = y;
            temZ = z;
        }
        if(time >= 50) {
            if (man.compare(light,a,b,c)){
                Layout.setBackgroundColor(Color.GREEN);
                temDevice = 1;
            }
            else if(man.compare(car,a,b,c)){
                Layout.setBackgroundColor(Color.GRAY);
                temDevice = 2;
            }
            else if(man.compare(screen,a,b,c)){
                Layout.setBackgroundColor(Color.BLUE);
                temDevice = 3;
            }
            else {
                time = 0;
                temDevice = 0;
                Layout.setBackgroundColor(Color.BLACK);
            }
        }
        time++;
        return temDevice;
    }














    public int getDevice(float x, float y, float z){
        int temDevice=0;
        if(time == 0 || time==1) {
            temX = x;
            temY = y;
            temZ = z;
        }
        if(time >= 50) {
            if (y <= -25 ){
                Layout.setBackgroundColor(Color.GREEN);
                temDevice = 1;
            }
            else if(y >= 25){
                Layout.setBackgroundColor(Color.GRAY);
                temDevice = 2;
            }
            else if(y < 25 && y > -25 ){
                Layout.setBackgroundColor(Color.BLUE);
                temDevice = 3;
            }
            else {
                time = 0;
                temDevice = 0;
                Layout.setBackgroundColor(Color.BLACK);
            }
        }
        time++;
        return temDevice;
    }

}
