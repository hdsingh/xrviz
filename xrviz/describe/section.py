from   jinja2 import Environment, PackageLoader, FileSystemLoader
import panel as pn
import os
import sys
import xarray as xr
from ..sigslot.base import SigSlot


class Describe(SigSlot):
    """
    This section describes the property selected in the Display section.

    Parameters
    ----------
    data: `xarray` instance: `DataSet` or `DataArray`
        datset is used to initialize the DataSelector
    
    Attributes
    ----------
    panel: Displays the generated template

    """
    def __init__(self,data):
        super().__init__()
        self.data = data
        self.panel = pn.pane.HTML(style={'font-size': '12pt'},width = 400) 
        self.panel.object = "Description Area"
        self._template_load_path = os.path.join(os.path.dirname(__file__),"templates")
        self._template_env = Environment(loader=FileSystemLoader(self._template_load_path))
        self._variable_template   = self._template_env.get_template('variable.html')
        self._coordinate_template = self._template_env.get_template('coordinate.html')
        self._dimension_template  = self._template_env.get_template('dimension.html')
        self._attribute_template  = self._template_env.get_template('attribute.html')
    
    def variable_pane(self,var):
        variable_attributes = [(k,v) for k,v in self.data[var].attrs.items()]
        output = self._variable_template.render(variable_attributes = variable_attributes)
        return output
    
    def attribute_pane(self,attr):
        attribute_description = self.data.attrs[attr]
        output = self._attribute_template.render(attribute = attr,attribute_description = attribute_description)
        return output
    
    def coordinate_pane(self,coord):
        output = self._coordinate_template.render(coordinate = coord)
        return output
    
    def dimension_pane(self,dim):
        output = self._dimension_template.render(dimension = dim,count = self.data.dims[dim] )
        return output
    
    def setup(self,selected_property,sub_property):
        if selected_property == 'Attributes':
            if sub_property != None:
                self.panel.object = self.attribute_pane(sub_property)
            else:
                self.panel.object = self._attribute_template.render()
        
        elif selected_property == 'Coordinates':
            if sub_property != None:
                self.panel.object = self.coordinate_pane(sub_property)
            else:
                self.panel.object = self._coordinate_template.render()
                
        elif selected_property == 'Dimensions':
            if sub_property != None:
                self.panel.object = self.dimension_pane(sub_property)
            else:
                self.panel.object = self._dimension_template.render()
        
        elif selected_property == 'Variables':
            if sub_property != None:
                self.panel.object = self.variable_pane(sub_property)
            else:
                self.panel.object = self._variable_template.render()
                
        else:
             self.panel.object = str(selected_property) + " : " + str(sub_property)