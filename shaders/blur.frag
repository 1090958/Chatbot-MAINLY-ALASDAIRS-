#version 430 core
uniform sampler2D tex;
uniform vec2 resolution;
uniform float r = 10;
in vec2 uvs;

out vec4 f_colour;
void main()
{             
    //blur
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
        col.rgb+=vec3(
            (texture2D(tex,p+vec2(0.001,-0.00097)*4)*w).r,
            (texture2D(tex,p+vec2(-0.00075,-0.00099)*4)*w).g,
            (texture2D(tex,p+vec2(-0.002,0.002)*4)*w).b*2
        );
        }}}

    f_colour.rgb = vec3(
            (texture2D(tex,uvs+vec2(0.001,-0.00097)*2)).r,
            (texture2D(tex,uvs+vec2(-0.00075,-0.00099)*2)).g,
            (texture2D(tex,uvs+vec2(-0.002,0.002)*2)).b
        )*1.3;
    f_colour+=(col*1.3)/2;
    

}