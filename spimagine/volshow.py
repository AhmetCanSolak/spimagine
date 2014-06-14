import sys
import numpy as np

from PyQt4 import QtCore,QtGui

from collections import OrderedDict
from spimagine.gui_mainwindow import MainWindow

from spimagine.data_model import DataModel, DemoData, NumpyData


def createApp():
    app = QtCore.QCoreApplication.instance()
    if app == None:
        app = QtGui.QApplication(sys.argv)
    if not hasattr(app,"volfigs"):
        app.volfigs = OrderedDict()
    return app

def volfig(num=None):
    app = createApp()
    #filter the dict
    app.volfigs =  OrderedDict((n,w) for n,w in app.volfigs.iteritems() if w.isVisible())

    if not num:
        if len(app.volfigs.keys())==0:
            num = 1
        else:
            num = max(app.volfigs.iterkeys())+1

    if app.volfigs.has_key(num):
        window = app.volfigs[num]
        app.volfigs.pop(num)
    else:
        window = MainWindow()
        window.show()

    #make num the last window
    app.volfigs[num] = window
    window.raise_()
    return window


def volshow(data, scale = True, stackUnits = [.1,.1,.1]):
    app = createApp()

    try:
        num,window = [(n,w) for n,w in app.volfigs.iteritems()][-1]
    except:
        num = 1

    window = volfig(num)

    if scale:
        ma,mi = np.amax(data), np.amin(data)
        data = 16000.*(data-mi)/(ma-mi)

    m = DataModel(NumpyData(data))
    window.glWidget.setModel(m)

    window.glWidget.transform.reset(np.amax(data),stackUnits)



def volshow2(data, win = None, scale = True, stackUnits = [.1,.1,.1]):
    app = createApp()

    if not win:
        window = MainWindow()
        window.show()
        window.raise_()
        win = window.glWidget
        if not hasattr(app,"volfigs"):
            print "no figs"
            app.volfigs = set()
        app.volfigs  = set([w for w in app.volfigs if w.isVisible()])
        app.volfigs.add(window)

    if scale:
        ma,mi = np.amax(data), np.amin(data)
        data = 16000.*(data-mi)/(ma-mi)

    m = DataModel(NumpyData(data))
    win.setModel(m)


    win.transform.reset(np.amax(data),stackUnits)
    return win


if __name__ == '__main__':

    app = createApp()


    # data = DemoData(50)[0]

    d = np.linspace(0,100,20*10**3).reshape((20,10,10,10))

    volfig(1)

    volshow2(d)

    volfig(2)

    volshow2(d)


    if app:
        sys.exit(app.exec_())
