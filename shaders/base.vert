#version 430 core

in vec2 vert;
in vec2 texcoord;
out vec3 fragCoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    fragCoord = vec3(vert, 0.0);
    gl_Position = vec4(vert, 0.0, 1.0);
}