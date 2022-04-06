class PlotParams():

    # The canonical input parameters that will drive all of our plotting routines

    def __init__(self, input_dict=None):
        # eventually we will look for non-default values
        self.scale = "linear"
        self.xax = []
        self.yax = []
        self.xlabel = "x label"
        self.ylabel = "y label"
        self.title = "title"
        self.xlim = None
        self.ylim = None
