from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode
import math

DESC = '''in radians
'''

class Sin(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(Sin, self).__init__(name, graph, w=150, colors=Colors, spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.inp0 = self.add_input_port('in', AGPortDataTypes.tNumeric)
        self.out0 = self.add_output_port('out', AGPortDataTypes.tNumeric)
        portAffects(self.inp0, self.out0)

    @staticmethod
    def get_category():
        return 'Math'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        data = self.inp0.get_data()
        try:
            self.out0.set_data(math.sin(data), False)
        except Exception as e:
            print(e)
