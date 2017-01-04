from PySide import QtCore
from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class RequestNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph, colors=Colors):
        super(RequestNode, self).__init__(name, graph)
        AGNode.__init__(self, name, graph)
        self.input = self.add_input_port('input', AGPortDataTypes.tAny)
        self.colors = colors
        self.looper = QtCore.QTimer()
        self.spin_box = QtGui.QSpinBox()
        self.cb = QtGui.QCheckBox()
        pb = QtGui.QPushButton('request')
        self.looper.timeout.connect(self.compute)

        lyt = self.add_layout()
        lyt2 = self.add_layout()

        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(5000)
        self.spin_box.setValue(100)
        prx_sb_delta_time = QtGui.QGraphicsProxyWidget()
        prx_sb_delta_time.setWidget(self.spin_box)

        pb.clicked.connect(self.compute)
        prx_btn = QtGui.QGraphicsProxyWidget()
        prx_btn.setWidget(pb)

        self.cb.stateChanged.connect(lambda: self.startEval(self.spin_box.value()))
        prx_cb = QtGui.QGraphicsProxyWidget()
        prx_cb.setWidget(self.cb)

        lyt2.addItem(prx_cb)
        lyt2.addItem(prx_btn)
        lyt.addItem(prx_sb_delta_time)
        lyt.setAlignment(lyt.itemAt(0), QtCore.Qt.AlignCenter)

    @staticmethod
    def get_category():
        return 'Util'

    def startEval(self, deltatime):
        if self.cb.isChecked():
            self.looper.start(deltatime)
        else:
            self.looper.stop()

    def kill(self, call_connection_functions=False):
        BaseNode.Node.kill(self, call_connection_functions)
        if self.looper.isActive():
            self.looper.stop()

    def compute(self):



        # check if any dirty nodes before connected port.
        # randint for example
        # if so push forward and recompute

        behind_dirty_ports = [p for p in find_ports_behind(self.input) if p.dirty == True]
        shouldRecalc = (not len(behind_dirty_ports) == 0)
        if shouldRecalc:
            # push from dirty ports
            # request data
            for p in behind_dirty_ports:
                push(p)

        data = self.input.get_data()
        print(data)
        self.graph.write_to_console(str(data), True)
