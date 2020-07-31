#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Helper functions

"""
import os
from abc import abstractmethod

from Path import Path, inkex, simplestyle

class Pattern(inkex.Effect):
    """ Class that inherits inkex.Effect and further specializes it for different
    Patterns generation

    Attributes
    ---------
    styles_dict: dict
            defines styles for every possible stroke. Default values are:
            styles_dict = {'m' : mountain_style,
                           'v' : valley_style,
                           'e' : edge_style}

    topgroup: inkex.etree.SubElement
            Top Inkscape group element

    path_tree: nested list 
        Contains "tree" of Path instances, defining new groups for each
        sublist

    translate: 2 sized tuple
        Defines translation to be added when drawing to Inkscape (default: 0,0)

    Methods
    ---------
    effect(self)
        Main function, called when the extension is run.

    create_styles_dict(self)
        Get stroke style parameters and use them to create the styles dictionary.

    calc_unit_factor(self)
        Return the scale factor for all dimension conversions

    add_text(self, node, text, position, text_height=12)
        Create and insert a single line of text into the svg under node.

    get_color_string(self, longColor, verbose=False)
        Convert the long into a #RRGGBB color value

    Abstract Methods
    ---------
    __init__(self)
        Parse all options

    generate_path_tree(self)
        Generate nested list of Path


    """
    
    @abstractmethod
    def generate_path_tree(self):
        """ Generate nested list of Path instances 
        Abstract method, must be defined in all child classes
        """
        pass

    @abstractmethod
    def __init__(self):
        """ Parse all common options 
        
        Must be reimplemented in child classes to parse specialized options
        """

        inkex.Effect.__init__(self)  # initialize the super class
        
        # backwards compatibility
        try:
            self.add_argument = self.arg_parser.add_argument
            self.str = str
            self.int = int
            self.float = float
            self.bool = inkex.Boolean
        except:
            self.add_argument = self.OptionParser.add_option
            self.str = "string"
            self.int = "int"
            self.float = "float"
            self.bool = "inkbool"

        # Two ways to get debug info:
        # OR just use inkex.debug(string) instead...
        try:
            self.tty = open("/dev/tty", 'w')
        except:
            self.tty = open(os.devnull, 'w')  # '/dev/null' for POSIX, 'nul' for Windows.
            # print >>self.tty, "gears-dev " + __version__

        self.add_argument("-u", "--units",
                         action="store", type=self.str,
                         dest="units", default='mm',
                         help="Units this dialog is using")
                                     
        # self.add_argument("-a", "--add_attachment",
        #                              action="store", type="inkbool", 
        #                              dest="add_attachment", default=False,
        #                              help="command line help")

        # self.add_argument("", "--accuracy", # note no cli shortcut
        #                              action="store", type="int",
        #                              dest="accuracy", default=0,
        #                              help="command line help")

        # --------------------------------------------------------------------------------------------------------------
        # mountain options
        self.add_argument('-m', '--mountain_stroke_color', action='store',
                         type=self.str, dest='mountain_stroke_color',
                         default=4278190335,  # Red
                         help='The mountain creases color.')
        self.add_argument('--mountain_stroke_width', action='store',
                         type=self.float, dest='mountain_stroke_width',
                         default=0.1,
                         help='Width of mountain strokes.')
        self.add_argument('--mountain_dashes_len', action='store',
                         type=self.float, dest='mountain_dashes_len',
                         default=1.0,
                         help='Mountain dash + gap length.')
        self.add_argument('--mountain_dashes_duty', action='store',
                         type=self.float, dest='mountain_dashes_duty',
                         default=0.5,
                         help='Mountain dash duty cycle.')
        self.add_argument('--mountain_dashes_bool', action='store',
                         type=self.bool, dest='mountain_dashes_bool',
                         default=True,
                         help='Dashed strokes?')
        self.add_argument('--mountain_bool', action='store',
                         type=self.bool, dest='mountain_bool',
                         default=True,
                         help='Draw mountains?')

        # --------------------------------------------------------------------------------------------------------------
        # valley options
        self.add_argument('-v', '--valley_stroke_color', action='store',
                         type=self.str, dest='valley_stroke_color',
                         default=65535,  # Blue---------
                         help='The valley creases color.')
        self.add_argument('--valley_stroke_width', action='store',
                         type=self.float, dest='valley_stroke_width',
                         default=0.1,
                         help='Width of valley strokes.')
        self.add_argument('--valley_dashes_len', action='store',
                         type=self.float, dest='valley_dashes_len',
                         default=1.0,
                         help='Valley dash + gap length.')
        self.add_argument('--valley_dashes_duty', action='store',
                         type=self.float, dest='valley_dashes_duty',
                         default=0.25,
                         help='Valley dash duty cycle.')
        self.add_argument('--valley_dashes_bool', action='store',
                         type=self.bool, dest='valley_dashes_bool',
                         default=True,
                         help='Dashed strokes?')
        self.add_argument('--valley_bool', action='store',
                         type=self.bool, dest='valley_bool',
                         default=True,
                         help='Draw valleys?')

        # --------------------------------------------------------------------------------------------------------------
        # edge options
        self.add_argument('-e', '--edge_stroke_color', action='store',
                         type=self.str, dest='edge_stroke_color',
                         default=255,  # Black
                         help='The mountain creases color.')
        self.add_argument('--edge_stroke_width', action='store',
                         type=self.float, dest='edge_stroke_width',
                         default=0.1,
                         help='Width of edge strokes.')
        self.add_argument('--edge_dashes_len', action='store',
                         type=self.float, dest='edge_dashes_len',
                         default=1.0,
                         help='Edge dash + gap length.')
        self.add_argument('--edge_dashes_duty', action='store',
                         type=self.float, dest='edge_dashes_duty',
                         default=0.25,
                         help='Edge dash duty cycle.')
        self.add_argument('--edge_dashes_bool', action='store',
                         type=self.bool, dest='edge_dashes_bool',
                         default=False,
                         help='Dashed strokes?')
        self.add_argument('--edge_bool', action='store',
                         type=self.bool, dest='edge_bool',
                         default=True,
                         help='Draw edges?')
        self.add_argument('--edge_single_path', action='store',
                         type=self.bool, dest='edge_single_path',
                         default=True,
                         help='Edges as single path?')

        # --------------------------------------------------------------------------------------------------------------
        # universal crease options
        self.add_argument('--universal_stroke_color', action='store',
                         type=self.str, dest='universal_stroke_color',
                         default=4278255615,  # Magenta
                         help='The universal creases color.')
        self.add_argument('--universal_stroke_width', action='store',
                         type=self.float, dest='universal_stroke_width',
                         default=0.1,
                         help='Width of universal strokes.')
        self.add_argument('--universal_dashes_len', action='store',
                         type=self.float, dest='universal_dashes_len',
                         default=1.0,
                         help='Universal dash + gap length.')
        self.add_argument('--universal_dashes_duty', action='store',
                         type=self.float, dest='universal_dashes_duty',
                         default=0.25,
                         help='Universal dash duty cycle.')
        self.add_argument('--universal_dashes_bool', action='store',
                         type=self.bool, dest='universal_dashes_bool',
                         default=False,
                         help='Dashed strokes?')
        self.add_argument('--universal_bool', action='store',
                         type=self.bool, dest='universal_bool',
                         default=True,
                         help='Draw universal creases?')

        # --------------------------------------------------------------------------------------------------------------
        # semicrease options
        self.add_argument('--semicrease_stroke_color', action='store',
                         type=self.str, dest='semicrease_stroke_color',
                         default=4294902015,  # Yellow
                         help='The semicrease creases color.')
        self.add_argument('--semicrease_stroke_width', action='store',
                         type=self.float, dest='semicrease_stroke_width',
                         default=0.1,
                         help='Width of semicrease strokes.')
        self.add_argument('--semicrease_dashes_len', action='store',
                         type=self.float, dest='semicrease_dashes_len',
                         default=1.0,
                         help='Semicrease dash + gap length.')
        self.add_argument('--semicrease_dashes_duty', action='store',
                         type=self.float, dest='semicrease_dashes_duty',
                         default=0.25,
                         help='Semicrease dash duty cycle.')
        self.add_argument('--semicrease_dashes_bool', action='store',
                         type=self.bool, dest='semicrease_dashes_bool',
                         default=False,
                         help='Dashed strokes?')
        self.add_argument('--semicrease_bool', action='store',
                         type=self.bool, dest='semicrease_bool',
                         default=True,
                         help='Draw semicreases?')

        # --------------------------------------------------------------------------------------------------------------
        # cut options
        self.add_argument('--cut_stroke_color', action='store',
                         type=self.str, dest='cut_stroke_color',
                         default=16711935,  # Green
                         help='The cut creases color.')
        self.add_argument('--cut_stroke_width', action='store',
                         type=self.float, dest='cut_stroke_width',
                         default=0.1,
                         help='Width of cut strokes.')
        self.add_argument('--cut_dashes_len', action='store',
                         type=self.float, dest='cut_dashes_len',
                         default=1.0,
                         help='Cut dash + gap length.')
        self.add_argument('--cut_dashes_duty', action='store',
                         type=self.float, dest='cut_dashes_duty',
                         default=0.25,
                         help='Cut dash duty cycle.')
        self.add_argument('--cut_dashes_bool', action='store',
                         type=self.bool, dest='cut_dashes_bool',
                         default=False,
                         help='Dashed strokes?')
        self.add_argument('--cut_bool', action='store',
                         type=self.bool, dest='cut_bool',
                         default=True,
                         help='Draw cuts?')

        # --------------------------------------------------------------------------------------------------------------
        # vertex options
        self.add_argument('--vertex_stroke_color', action='store',
                         type=self.str, dest='vertex_stroke_color',
                         default=255,  # Black
                         help='Vertices\' color.')
        self.add_argument('--vertex_stroke_width', action='store',
                         type=self.float, dest='vertex_stroke_width',
                         default=0.1,
                         help='Width of vertex strokes.')
        self.add_argument('--vertex_radius', action='store',
                         type=self.float, dest='vertex_radius',
                         default=0.1,
                         help='Radius of vertices.')
        self.add_argument('--vertex_bool', action='store',
                         type=self.bool, dest='vertex_bool',
                         default=True,
                         help='Draw vertices?')

        # here so we can have tabs - but we do not use it directly - else error
        self.add_argument('--active-tab',
                         action="store", type=self.str,
                         dest="active_tab", default='title',  # use a legitimate default
                         help="Active tab.")

        self.path_tree = []
        self.edge_points = []
        self.translate = (0, 0)

    def effect(self):
        """ Main function, called when the extension is run.
        """
        # construct dictionary containing styles
        self.create_styles_dict()

        # get paths for selected origami pattern
        self.generate_path_tree()

        # ~ accuracy = self.options.accuracy
        # ~ unit_factor = self.calc_unit_factor()
        # what page are we on
        # page_id = self.options.active_tab # sometimes wrong the very first time

        # Translate according to translate attribute
        g_attribs = {inkex.addNS('label', 'inkscape'): '{} Origami pattern'.format(self.options.pattern),
                       # inkex.addNS('transform-center-x','inkscape'): str(-bbox_center[0]),
                       # inkex.addNS('transform-center-y','inkscape'): str(-bbox_center[1]),
                     inkex.addNS('transform-center-x', 'inkscape'): str(0),
                     inkex.addNS('transform-center-y', 'inkscape'): str(0),
                     'transform': 'translate(%s,%s)' % self.translate}

        # add the group to the document's current layer
        if type(self.path_tree) == list and len(self.path_tree) != 1:
            self.topgroup = inkex.etree.SubElement(self.get_layer(), 'g', g_attribs)
        else:
            self.topgroup = self.get_layer()

        if len(self.edge_points) == 0:
            Path.draw_paths_recursively(self.path_tree, self.topgroup, self.styles_dict)
        elif self.options.edge_single_path:
            edges = Path(self.edge_points, 'e', closed=True)
            Path.draw_paths_recursively(self.path_tree + [edges], self.topgroup, self.styles_dict)
        else:
            edges = Path.generate_separated_paths(self.edge_points, 'e', closed=True)
            Path.draw_paths_recursively(self.path_tree + edges, self.topgroup, self.styles_dict)

        # self.draw_paths_recursively(self.path_tree, self.topgroup, self.styles_dict)

    # compatibility hack, "affect()" is replaced by "run()"
    def draw(self):
        try:
            self.run() # new
        except:
            self.affect() # old

    # compatibility hack
    def get_layer(self):
        try:
            return self.svg.get_current_layer() # new
        except:
            return self.current_layer # old

    def create_styles_dict(self):
        """ Get stroke style parameters and use them to create the styles dictionary, used for the Path generation
        """
        unit_factor = self.calc_unit_factor()
        
        # define colour and stroke width
        mountain_style = {'draw': self.options.mountain_bool,
                          'stroke': self.get_color_string(self.options.mountain_stroke_color),
                          'fill': 'none',
                          'stroke-width': self.options.mountain_stroke_width*unit_factor}

        valley_style = {'draw': self.options.valley_bool,
                        'stroke': self.get_color_string(self.options.valley_stroke_color),
                        'fill': 'none',
                        'stroke-width': self.options.valley_stroke_width*unit_factor}

        universal_style = {'draw': self.options.universal_bool,
                           'stroke': self.get_color_string(self.options.universal_stroke_color),
                           'fill': 'none',
                           'stroke-width': self.options.universal_stroke_width*unit_factor}

        semicrease_style = {'draw': self.options.semicrease_bool,
                            'stroke': self.get_color_string(self.options.semicrease_stroke_color),
                            'fill': 'none',
                            'stroke-width': self.options.semicrease_stroke_width*unit_factor}

        cut_style = {'draw': self.options.cut_bool,
                     'stroke': self.get_color_string(self.options.cut_stroke_color),
                     'fill': 'none',
                     'stroke-width': self.options.cut_stroke_width*unit_factor}

        edge_style = {'draw': self.options.edge_bool,
                      'stroke': self.get_color_string(self.options.edge_stroke_color),
                      'fill': 'none',
                      'stroke-width': self.options.edge_stroke_width*unit_factor}

        vertex_style = {'draw': self.options.vertex_bool,
                        'stroke': self.get_color_string(self.options.vertex_stroke_color),
                        'fill': 'none',
                        'stroke-width': self.options.vertex_stroke_width*unit_factor}

        # check if dashed option selected
        if self.options.mountain_dashes_bool:
            dash = self.options.mountain_dashes_len*self.options.mountain_dashes_duty*unit_factor
            gap = abs(dash - self.options.mountain_dashes_len*unit_factor)
            mountain_style['stroke-dasharray'] = "{},{}".format(dash, gap)
        if self.options.valley_dashes_bool:
            dash = self.options.valley_dashes_len * self.options.valley_dashes_duty*unit_factor
            gap = abs(dash - self.options.valley_dashes_len*unit_factor)
            valley_style['stroke-dasharray'] = "{},{}".format(dash, gap)
        if self.options.edge_dashes_bool:
            dash = self.options.edge_dashes_len * self.options.edge_dashes_duty*unit_factor
            gap = abs(dash - self.options.edge_dashes_len*unit_factor)
            edge_style['stroke-dasharray'] = "{},{}".format(dash, gap)
        if self.options.universal_dashes_bool:
            dash = self.options.universal_dashes_len * self.options.universal_dashes_duty*unit_factor
            gap = abs(dash - self.options.universal_dashes_len*unit_factor)
            universal_style['stroke-dasharray'] = "{},{}".format(dash, gap)
        if self.options.semicrease_dashes_bool:
            dash = self.options.semicrease_dashes_len * self.options.semicrease_dashes_duty*unit_factor
            gap = abs(dash - self.options.semicrease_dashes_len*unit_factor)
            semicrease_style['stroke-dasharray'] = "{},{}".format(dash, gap)
        if self.options.cut_dashes_bool:
            dash = self.options.cut_dashes_len * self.options.cut_dashes_duty*unit_factor
            gap = abs(dash - self.options.cut_dashes_len*unit_factor)
            cut_style['stroke-dasharray'] = "{},{}".format(dash, gap)

        self.styles_dict = {'m': mountain_style,
                            'v': valley_style,
                            'u': universal_style,
                            's': semicrease_style,
                            'c': cut_style,
                            'e': edge_style,
                            'p': vertex_style}

    def get_color_string(self, longColor, verbose=False):
        """ Convert the long into a #RRGGBB color value
            - verbose=true pops up value for us in defaults
            conversion back is A + B*256^1 + G*256^2 + R*256^3
        """
        # compatibility hack, no "long" in Python 3
        try:
            longColor = long(longColor)
            if longColor < 0: longColor = long(longColor) & 0xFFFFFFFF
            hexColor = hex(longColor)[2:-3]
        except:
            longColor = int(longColor)
            hexColor = hex(longColor)[2:-2]
            inkex.debug = inkex.utils.debug

        hexColor = '#' + hexColor.rjust(6, '0').upper()
        if verbose: inkex.debug("longColor = {}, hex = {}".format(longColor,hexColor))

        return hexColor
    
    def add_text(self, node, text, position, text_height=12):
        """ Create and insert a single line of text into the svg under node.
        """
        line_style = {'font-size': '%dpx' % text_height, 'font-style':'normal', 'font-weight': 'normal',
                     'fill': '#F6921E', 'font-family': 'Bitstream Vera Sans,sans-serif',
                     'text-anchor': 'middle', 'text-align': 'center'}
        line_attribs = {inkex.addNS('label','inkscape'): 'Annotation',
                       'style': simplestyle.formatStyle(line_style),
                       'x': str(position[0]),
                       'y': str((position[1] + text_height) * 1.2)
                       }
        line = inkex.etree.SubElement(node, inkex.addNS('text','svg'), line_attribs)
        line.text = text

           
    def calc_unit_factor(self):
        """ Return the scale factor for all dimension conversions.

            - The document units are always irrelevant as
              everything in inkscape is expected to be in 90dpi pixel units
        """
        # namedView = self.document.getroot().find(inkex.addNS('namedview', 'sodipodi'))
        # doc_units = self.getUnittouu(str(1.0) + namedView.get(inkex.addNS('document-units', 'inkscape')))
        # backwards compatibility
        try:
            return self.svg.unittouu(str(1.0) + self.options.units)
        except:
            try:
                return inkex.unittouu(str(1.0) + self.options.units)
            except AttributeError:
                return self.unittouu(str(1.0) + self.options.units)



