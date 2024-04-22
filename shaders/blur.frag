#version 430 core
uniform sampler2D tex;
uniform vec2 resolution;
uniform float r = 10;
uniform float pixel = 1;
uniform bool blur;
uniform int type = 1;
in vec2 uvs;

out vec4 f_colour;
void main()
{          
    if (type == 1){
       
        //blur + bloom
        vec2 pos = uvs*2-vec2(1,1);
        float x,y,xx,yy,rr=r*r,dx,dy,w,w0;
        w0=0.3780/pow(r,1.975);
        vec2 p;
        vec4 col=vec4(0.0,0.0,0.0,0.0);
        for (dx=1.0/resolution.x,x=-r,p.x=0.5+(pos.x*0.5)+(x*dx);x<=r;x++,p.x+=dx){ xx=x*x;
        for (dy=1.0/resolution.y,y=-r,p.y=0.5+(pos.y*0.5)+(y*dy);y<=r;y++,p.y+=dy){ yy=y*y;
        if (xx+yy<=rr)
            {
            w=w0*exp((-xx-yy)/(2.0*rr));
            float e = 1.3;
            col.rgb+=vec3(
                pow((texture2D(tex,p+vec2(0.001,-0.00097)*4)*w).r,e)*10,
                pow((texture2D(tex,p+vec2(-0.00075,-0.00099)*4)*w).g,e)*10,
                pow((texture2D(tex,p+vec2(-0.002,0.002)*4)*w).b,e)*10
            );
            }}}

        f_colour.rgb = vec3(
                (texture2D(tex,uvs+vec2(0.001,-0.00097)*2)).r,
                (texture2D(tex,uvs+vec2(-0.00075,-0.00099)*2)).g,
                (texture2D(tex,uvs+vec2(-0.002,0.002)*2)).b
            )*1.3;
        f_colour+=(col*1.3)/2;
        if (blur){
            //f_colour=texture2D(tex,floor(uvs*pixel)/pixel);
            f_colour = col;
        }
        f_colour.a=1;
    }
    else{
        //blur + bloom
        vec2 pos = (uvs)*2;

        pos = pos*2;
        float x,y,xx,yy,rr=r*r,dx,dy,w,w0;
        if ((pos.x > 1) && (pos.y > 1) && (pos.x < 3) && (pos.y < 3)&&(texture2D(tex,uvs*2+vec2(0.5)).r != 1)){

            w0=0.3780/pow(r,1.975);
            vec2 p;
            vec4 col=vec4(0.0,0.0,0.0,0.0);
            pos = pos/2+vec2(0.5);
            
            f_colour.rgb = vec3(
            (texture2D(tex,pos))
            )*1.3;
            f_colour= f_colour*1.5;
            f_colour.a=1;}
    
        else{
        f_colour = vec4(1.0, 1.0, 1.0, 0.0);
        }
    
    }
    
    

}