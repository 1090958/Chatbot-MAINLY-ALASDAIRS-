#version 430 core

uniform sampler2D tex;
uniform float CURVATURE = 4.2;
uniform float BLUR = 0.0;
uniform float CA_AMT = 1.01;
uniform vec2 resolution;
uniform float r=5;     

in vec2 uvs;
in vec3 fragCoord;
out vec4 f_colour;

vec4 samplecrt(in vec2 uv, in sampler2D texture, out vec4 result){
        //curving
        vec2 crtUV=uv*2.-1.;
        vec2 offset=crtUV.yx/CURVATURE;
        crtUV+=crtUV*offset*offset;
        crtUV=crtUV*.5+.5;
        
        vec2 edge=smoothstep(0., BLUR, crtUV)*(1.-smoothstep(1.-BLUR, 1., crtUV));
        
        //chromatic abberation
        result.rgb = vec3(
            texture(tex, (crtUV-.5)*CA_AMT+.5).r*0.9,
            texture(tex, crtUV).g,
            texture(tex, (crtUV-.5)/CA_AMT+.5).b*1.75
        )*edge.x*edge.y;
        return result;
    }
void main() {


    
    
    
    
    //blur
    //vec2 uv=vec2(uvs.x*2-1, uvs.y*2-1);
    //float x,y,xx,yy,rr=r*r,dx,dy,w,w0;
    //w0=0.3780/pow(r,1.975);
    //vec2 p;
    //vec4 col=vec4(0.0,0.0,0.0,0.0);
    //for (dx=1.0/resolution.x,x=-r,p.x=0.5+(uv.x*0.5)+(x*dx);x<=r;x++,p.x+=dx){ xx=x*x;
    //for (dy=1.0/resolution.y,y=-r,p.y=0.5+(uv.y*0.5)+(y*dy);y<=r;y++,p.y+=dy){ yy=y*y;
    //if (xx+yy<=rr)
    //{
    //w=w0*exp((-xx-yy)/(2.0*rr));
    //col+=samplecrt(p.xy,tex);
    //}}}
    //vec3 blur=col.rgb;
    //f_colour.rgb+=blur;
    f_colour = vec4(0,0,0,0);

    
}