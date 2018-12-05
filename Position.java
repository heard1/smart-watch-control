package com.example.l.watch;

public class Position {
    public double x,y,z;

    public Position(double x0, double y0, double z0){
        x=x0;
        y=y0;
        z=z0;
    }

    public boolean compare(Position Device, double a, double b, double c){
        boolean isRight=false;
        double vx=Device.x-x;
        double vy=Device.y-y;
        double vz=Device.z-z;
        double norm = Math.sqrt(vx * vx + vy * vy + vz * vz);
        vx = vx / norm;
        vy = vy / norm;
        vz = vz / norm;
        if( vx/a<1.2 && vx/a>0.8 && vy/b<1.2 && vy/b>0.8 && vz/c<1.2 && vz/c>0.8 ) isRight=true;
        return isRight;
    }
}
