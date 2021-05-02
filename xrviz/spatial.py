import panel as pn
from holoviews.plotting import list_cmaps
from xrviz.sigslot import SigSlot


from xrspatial import hillshade, slope, aspect, viewshed
from xrspatial.classify import equal_interval, natural_breaks, quantile
from xrspatial.zonal import regions

TEXT = """
Apply functions for Spatial Analysis. For more information, 
please refer [xarray-spatial](https://github.com/makepath/xarray-spatial/)
"""


class Spatial(SigSlot):
    def __init__(self):
        super().__init__()
        self.getFunc = {'aspect': aspect,
                'equal_interval': equal_interval,
                'hillshade': hillshade,
                'natural_breaks': natural_breaks,
                'quantile': quantile,
                'regions': regions,
                'slope': slope, 
                }
        functionOps = [None, *self.getFunc.keys()]
        self.function = pn.widgets.Select(name='function',options = functionOps)
        self.spatial_inputs = pn.Row()
        self._register(self.function, 'setInputs')
        self.connect('setInputs', self.setup)

        self.panel = pn.Column(
            pn.pane.Markdown(TEXT, margin=(0, 10)),
            pn.Row(self.function),
            self.spatial_inputs,
            name='Spatial'
        )
        self.setup()

    def setup(self, *args):
        self.spatial_inputs.clear()
        if self.function.value == 'hillshade':
            self.azimuth = pn.widgets.IntInput(name='azimuth', value=225)
            self.angle_altitude = pn.widgets.IntInput(name='angle_altitude', value=25)
            self.spatial_inputs.extend([self.azimuth, self.angle_altitude])
        elif self.function.value == 'natural_breaks':
            self.num_sample = pn.widgets.IntInput(name='num_sample', value=1000)
            self.k = pn.widgets.IntInput(name='k', value=15)
            self.spatial_inputs.extend([self.num_sample, self.k]) 
        elif self.function.value == 'regions':
            self.neighborhood = pn.widgets.Select(name='neighborhood', value=4, options = [4,8])
            self.spatial_inputs.extend([self.neighborhood]) 
        elif self.function.value == 'equal_interval' or self.function.value == 'quantile':
            self.k = pn.widgets.IntInput(name='k', value=5)
            self.spatial_inputs.extend([self.k]) 

    def setup_initial_values(self, init_params={}):
        """
        To select initial values for the widgets in this pane.
        """
        for row in self.panel[1:]:
            for widget in row:
                if widget.name in init_params:
                    widget.value = init_params[widget.name]

    @property
    def kwargs(self):
        out = { widget.name: widget.value
               for row in self.panel[1:] for widget in row}
        
        return out
    
    @property
    def spatial_kwargs(self):
        # Inputs for spatial function
        out = { widget.name: widget.value
               for row in self.panel[2:] for widget in row}
        return out