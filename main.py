import collections

from kivy import app, properties
from kivy.uix import label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Line
import kivy.utils

MapCoords = collections.namedtuple('MapCoords', ['row', 'col'])


class StrategyGame(FloatLayout):
    main_map = properties.ObjectProperty(None)
    map_rows = properties.NumericProperty(0)
    map_cols = properties.NumericProperty(0)

    def __init__(self, **kwargs):
        super(StrategyGame, self).__init__(**kwargs)

        number_of_regions = self.map_rows * self.map_cols
        for region in xrange(0, number_of_regions):
            row = region / self.map_cols
            col = region % self.map_cols

            # Add hex cells to make up the map.
            hex_cell = HexMapCell()
            self.main_map.add_widget(hex_cell)

            # Add overlay conditionally.
            if (row % 6 == 1 and col % 2 == 1) or (row % 6 == 4 and col % 2 == 0):
                print('({}, {})'.format(row, col))

                # Determine size of the hexagon cell.
                radius = 2 * hex_cell.height
                solid_x = hex_cell.x - hex_cell.height*2
                solid_y = hex_cell.y - hex_cell.height*2
                solid_size = (4*hex_cell.height, 4*hex_cell.height)

                with hex_cell.canvas.after:

                    # Create the outline of hexagon.
                    Color(1, 0, 1, 1)
                    hex_cell.ell = Line(circle=(hex_cell.x, hex_cell.y, radius, 0, 360, 6), width=2)

                    # Create the solid background for the hexagon.
                    Color(*kivy.utils.get_random_color(alpha=.5))
                    hex_cell.solid = Ellipse(pos=(solid_x, solid_y), size=solid_size, segments=6)
                hex_cell.bind(pos=hex_cell.update_pos, size=hex_cell.update_pos)


class HexMapCell(label.Label):
    def __init__(self, row=0, col=0, **kwargs):
        super(HexMapCell, self).__init__(**kwargs)
        self.coords = MapCoords(row, col)

    def update_pos(self, instance, value):

        # Determine size of the hexagon cell.
        radius = 2 * self.height
        solid_x = self.x - self.height*2
        solid_y = self.y - self.height*2
        solid_size = (4*self.height, 4*self.height)

        # Resize the outline of the cell.
        self.ell.circle = (self.x, self.y, radius, 0, 360, 6)

        # Resize the actual cell.
        self.solid.pos = (solid_x, solid_y)
        self.solid.size = solid_size


class StrategyGameApp(app.App):
    def build(self):
        return StrategyGame()

if __name__ == '__main__':
    StrategyGameApp().run()
