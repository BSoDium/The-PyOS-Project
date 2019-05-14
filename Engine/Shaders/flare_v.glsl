//GLSL
#version 140
in vec4 p3d_Vertex;
uniform mat4 p3d_ModelViewProjectionMatrix;
out vec2 uv;

void main()
    {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex; 
    uv=gl_Position.xy*0.5+0.5;
}