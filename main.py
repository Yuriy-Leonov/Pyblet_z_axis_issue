import pyglet


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.position = [0, 0, 300.0]
        self.vertices_list = []

        # BLUE rect
        self.add_rect("blue.png", x=40, y=40, z=0)
        # RED rect
        self.add_rect("red.png", x=50, y=50, z=10)
        # Expects RED will be in front of BLUE, but it isn't
        # BLUE on top regardless of z value. I tried -10/10, etc.

    def add_rect(self, file_name, x, y, z):
        image = pyglet.image.load(file_name)
        image_grid = pyglet.image.ImageGrid(image, 1, 1)
        texture_grid = image_grid.get_texture_sequence()
        texture_group = pyglet.graphics.TextureGroup(texture_grid)
        x_ = (texture_group.texture.width + x)
        y_ = (texture_group.texture.height + y)
        tex_coords = ('t3f', texture_grid[0].texture.tex_coords)

        vert_list = self.batch.add(
            4, pyglet.gl.GL_QUADS,
            texture_group,
            ('v3f', (x, y, z,
                     x_, y, z,
                     x_, y_, z,
                     x, y_, z)),
            tex_coords)
        self.vertices_list.append(vert_list)

    def set_3d(self):
        width, height = self.get_size()
        pyglet.graphics.glEnable(pyglet.graphics.GL_BLEND)
        pyglet.graphics.glBlendFunc(
            pyglet.graphics.GL_SRC_ALPHA,
            pyglet.graphics.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.graphics.glViewport(0, 0, width, height)
        pyglet.graphics.glMatrixMode(pyglet.graphics.GL_PROJECTION)
        pyglet.graphics.glLoadIdentity()
        pyglet.graphics.gluPerspective(90, width / height, 0.1, 6000.0)
        pyglet.graphics.glMatrixMode(pyglet.graphics.GL_MODELVIEW)
        pyglet.graphics.glLoadIdentity()
        x, y, z = self.position
        pyglet.graphics.glTranslatef(x, y, -z)

    def on_draw(self):
        self.clear()
        self.set_3d()
        self.batch.draw()


if __name__ == '__main__':
    window = Window(width=1400, height=800, caption='Pyglet', resizable=True)
    window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()
