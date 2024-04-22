import moderngl, array
ctx = moderngl.create_context()
ctx.enable(moderngl.BLEND)
quad_buffer = ctx.buffer(data=array.array('f', [
    # position (x, y), uv coords (x, y)
    -1.0, 1.0, 0.0, 0.0,  # topleft
    1.0, 1.0, 1.0, 0.0,   # topright
    -1.0, -1.0, 0.0, 1.0, # bottomleft
    1.0, -1.0, 1.0, 1.0,  # bottomright
]))

def import_shader(name):
    vertex = open(f'shaders/{name}.vert').read()
    fragment = open(f'shaders/{name}.frag').read()
    return ctx.program(vertex,fragment)

def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex