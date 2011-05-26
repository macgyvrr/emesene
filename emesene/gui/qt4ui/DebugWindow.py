# -*- coding: utf-8 -*-

'''This module contains classes needed to the debug window'''

import logging
import time

from PyQt4  import QtGui
#from PyQt4  import QtCore

from gui.qt4ui.Utils import tr

import debugger
#import gui
#from gui.qt4ui import Dialog
#from gui.qt4ui import widgets

log = logging.getLogger('qt4ui.DebugWindow')

class DebugWindow(QtGui.QWidget):
    '''A Window which shows debug messages'''
    NAME = 'Debug Window'
    DESCRIPTION = 'A window which shows debug messages'
    AUTHOR = 'Gabriele "Whisky" Visconti'
    WEBSITE = ''

    def __init__(self, on_close_cb, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self._on_close_cb = on_close_cb
        self._widget_d = {}
        self._setup_ui()
        
        logging.getLogger().addHandler(self._widget_d['text_view'])
        
        
        print (QtGui.QApplication.activeWindow())
        
    
    def _setup_ui(self):
        self._widget_d['filter_edit'] = QtGui.QLineEdit()
        self._widget_d['msg_level_combo'] = QtGui.QComboBox()
        self._widget_d['filter_btn'] = QtGui.QPushButton(tr('Filter'))
        hlay = QtGui.QHBoxLayout()
        hlay.addWidget(self._widget_d['filter_edit'])
        hlay.addWidget(self._widget_d['msg_level_combo'])
        hlay.addWidget(self._widget_d['filter_btn'])
        
        self._widget_d['text_view'] = DebugTextView()
        lay = QtGui.QVBoxLayout()
        lay.addLayout(hlay)
        lay.addWidget(self._widget_d['text_view'])
        self.setLayout(lay)
        
        self.setWindowTitle(tr('Debug'))
        self.resize(800, 600)
        
        
    def closeEvent(self, event):
        # pylint: disable=C0103
        logging.getLogger().removeHandler(self._widget_d['text_view'])
        QtGui.QWidget.closeEvent(self, event)
        self._on_close_cb()
        #event.ignore()
        
    
    def show(self):
        QtGui.QWidget.show(self)
        
    
    def __del__(self):
        print 'CLOSING DEBUG WINDOW'
        self._on_close_cb()
        
        
        
        
        
        
class DebugTextView(QtGui.QTextEdit, logging.Handler):
    '''Debug messages visualization widget'''
    
    def __init__(self, parent=None):
        QtGui.QTextBrowser.__init__(self, parent)
        logging.Handler.__init__(self)
        self._list = []
        self._cursor = QtGui.QTextCursor(self.document())
        queue_handler = debugger.QueueHandler.get()
        for record in queue_handler.get_all():
            self.on_record_added(record)
        
    
    
    def emit(self, record):
        self.on_record_added(record)
        
        
        
    def handle(self, record):
        '''To send the handle message to logging.Handler base class
        instead of QTextEdit'''  
        logging.Handler.handle(self, record)
        
    def on_record_added(self, record):
        self._list.append(record)
        time_string = time.localtime(float(record.created))
        time_string = time.strftime("%H:%M:%S", time_string)
        html = u'<small>(%s): [<b>%s</b>] : '
        html = html % (time_string, record.name)
        try:
            html = html + '%s</small><br />' % record.msg.strip()
        except AttributeError as detail:
            #log.error('Wrong type: %s | value: %s' % (detail, str(record.msg)))
            html = html + '<small><i>&lt;&lt;message insertion failed [%s:%s]&gt;&gt;</i></small><br>' % (type(record.msg), str(record.msg))
        self._cursor.insertHtml(html)
        
