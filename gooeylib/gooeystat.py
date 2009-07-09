# Copyright (C) 2008, 2009  Spencer Herzberg <spencer.herzberg@gmail.com>

# This file is part of GooeyStat

# GooeyStat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time import localtime
from HelperWidgets import *
from string import capwords
import functools,os,sys
from gooeylib import trace
from plugins.helpers.templates import *
from pkg_resources import resource_filename


class GooeyStat(QMainWindow):
    
    def __init__(self,parent=None):
        
        QMainWindow.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setWindowTitle("GooeyStat v0.1")
        
        self.PLUGINPATH = [os.path.join(os.path.dirname(__file__), 'plugins')]
        
        self.setupMenus()
        self.setupDocks()
        self.setupWidgets()
        self.plugins={}
        self.loadPlugins()

        self.setStatus("Ready!")
        
    def setupMenus(self):
        self.setMenuBar(QMenuBar(self))
        
        order = ["file","edit","do","plugins","help"]
        plugins = {}

        self.menus = {  "file":None,
                        "edit":None,
                         "do":None,
                         "plugins":None,
                         "help":None
                        }
        
        actions=[]
        
        actions.append( [    "file",
                            ["&New", self.fileNew, QKeySequence.New, "filenew", "Create new file",False,"triggered()",True],
                            ["&Open...", self.fileOpen, QKeySequence.Open, "fileopen", "Open file",False,"triggered()",True],
                            None,
                            ["&Save", self.fileSave, QKeySequence.Save, "filesave", "Save file",False,"triggered()",True],
                            ["Save &As", self.fileSaveAs, "Ctrl+Shift+s", "filesaveas", "Save file as",False,"triggered()",True]
                            ])
        
        actions.append( [
                            "edit",
                            ["Cu&t",self.cut,QKeySequence.Cut,"editcut","Cut",False,"triggered()",True],
                            ["&Copy",self.copy,QKeySequence.Copy,"editcopy","Copy",False,"triggered()",True],
                            ["&Paste",self.paste,QKeySequence.Paste,"editpaste","Paste",False,"triggered()",True]
                            #None,
                            #["Debugging",self.setDebugging,None,"debugging","Debugging",True,"triggered()",False]
                        ])
        
        
        actions.append( ["do",[]])
        
        actions.append( ["plugins",
                          ["&Reload Plugins", self.loadPlugins,None,"pluginsmanage","Reload Plugins",False,"triggered()",False],
                          None,
                         ["&Manage", self.pluginsManage,None,"pluginsmanage","Manage Plugins",False,"triggered()",False]
                         ])
        
        actions.append( [    "help",
                    ["&About", self.helpAbout, None, "helpabout", "About this application",False,"triggered()",False]
                    ])
        

        for l_actions in actions:
            name = "&"+capwords(l_actions[0])
            self.menus[ l_actions[0][l_actions[0].find(":")+1:] ] = QMenu(name,self)
            menu = self.menus[ l_actions[0] ]
            
            toolbar = None
            for action in l_actions[1:]:
                if action == []:
                    break
                if action == None:
                    menu.addSeparator()
                else:
                    a = self.createAction(action)
                    menu.addAction(a)
                    
                    if action[-1]:
                        if not toolbar:
                            toolbar = self.addToolBar(name[1:])
                        toolbar.addAction(a)
        

        for key in order:
            if key!="k":
                trace.mutter("%s %s %s",key,self.menus[key].title(),type(self.menus[key]))
                self.menuBar().addMenu(self.menus[key])
        
    def setupDocks(self):
        self.logDockWidget = QDockWidget("Log")
        self.logDockWidget.setObjectName("LogDockWidget")
        logMain = QWidget()
        logMain.setLayout(QVBoxLayout())
        
        self.console = Console(self.logDockWidget)#QLineEdit()
        self.connect(self.console,SIGNAL("returnPressed()"),self.getConsole)
        
        logMain.layout().addWidget(self.console)
        self.logDockWidget.setWidget(logMain)
        self.addDockWidget(Qt.RightDockWidgetArea, self.logDockWidget)
        self.logDockWidget.show()

    def setupWidgets(self):
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
    
        self.status = self.statusBar()
        label = QLabel()
#        label.setFrameStyle(QFrame.Sunken )#QFrame.StyledPanel | )
#        self.status.setSizeGripEnabled(False)
        self.status.addPermanentWidget(label)
    
    def getConsole(self):
        answer = self.console.text() + " = "
        try:
            answer += str(eval(str(self.console.text())))
            
        except:
            answer += "Invalid Equation!"

        self.log(str(answer))
        self.console.clear()

    def createAction(self,text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        if type(text)== type([]):
            l = text
            text = l[0]
            slot = l[1]
            shortcut = l[2]
            icon = l[3]
            tip = l[4]
            checkable = l[5]
            signal = l[6]

        action = QAction(text,self)
        if icon is not None:
            action.setIcon(QIcon(resource_filename(__name__, "icons/%s.png" % icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action,SIGNAL(signal),slot)
        if checkable:
            action.setCheckable(True)

        return action

    #Menu Functions
    #####################################

    def fileNew(self,fileName=None):
        statedit = GooeyEdit()
        if fileName:
            statedit.load(fileName)
            self.setStatus("Opened File: '%s'" %fileName[str(fileName).rfind("/")+1:])
        else:
            self.setStatus("New File...")

        self.addWindow(statedit)
        
        #self.log("Opened a StatEdit")
        
    def fileOpen(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "./", "GooeyEdit Files (*.gef *.csv )")
        if fileName != "":
            self.fileNew(fileName)
        
    def fileSave(self):
        if len(self.mdi.subWindowList()) != 0:
            fileName = self.mdi.currentSubWindow().widget().getFileName()
            if os.path.exists(fileName):
                self.mdi.currentSubWindow().widget().saveAs(fileName)
            else:
                self.fileSaveAs()
        self.setStatus("Saving [%s]..." %fileName)
            
    def fileSaveAs(self):
        if len(self.mdi.subWindowList()) != 0:
            fileName = QFileDialog.getSaveFileName(self, "Save File", "./", "GooeyEdit Files (*.gef )")
            if fileName != "":
                if not fileName.contains(".gef"):
                    fileName+=".gef"
            
                self.mdi.currentSubWindow().widget().saveAs(fileName)
    
    def cut(self):
        self.getCurrWidget().cut()
        
    def copy(self):
        self.getCurrWidget().copy()
        
    def paste(self):
        self.getCurrWidget().paste()

    def pluginsManage(self):
        trace.mutter("Do you really want to manage me?")
    
    def buildMenu(self,dict,menu=None):
        if type(dict) == type([]):
            for action in dict:
                menu.addAction(action)
            return menu
        
        else:
            keys = dict.keys()
            keys.sort()
            keys.reverse()
            for k in keys:
                
                if k == "_actions":
                    tmp=self.buildMenu(dict[k],menu)
                else:
                    tmp = self.buildMenu(dict[k],QMenu(capwords(k),self))
                    menu.addMenu(tmp)
                    
            return menu
    
    def closeEvent(self,event):
        for window in self.mdi.subWindowList():
            try:
                if window.widget().isDirty():
                    msg = QMessageBox()
                    msg.setWindowTitle("Close?!")
                    msg.setText("Close without saving?")
                    answer = msg.exec_()
                    
            except:
                pass
        
    def loadPlugins(self):
        
        menus = {}
        for path in self.PLUGINPATH:
            for f in os.listdir(path):
                if f[0]!="_" and f.find(".py~")==-1  and f[0]!="." and f.find(".py")>=1 and f.find(".pyc")==-1:
                    fname = f[:f.find(".py")]
                    try:
                        reload(self.plugins[fname])
                    except:
                        tmp_string = "gooeylib.plugins.%s" %fname
                        tmp = __import__(tmp_string)
                        trace.mutter(sys.modules[tmp_string])
                        self.plugins[fname]=sys.modules[tmp_string]
            
    #                menus = {}
                    module = self.plugins[fname]
    
                    for plugin in dir(module):
                        
                        if plugin.startswith("plugin_"):
                            trace.mutter("\tName: %s",plugin)
                            plugin = eval( "self.plugins['"+fname+"']."+ plugin +"()" )
                            
                            menuloc = plugin.MENU_LOC.split(":")
                            loc=menus
                            for key in menuloc:
                                if loc.has_key( key ):
                                    loc=loc[ key ]
                                else:
                                    loc[ key ] = {}
                                    loc=loc[key]
                                    loc["_actions"] = []
                            
                            
                            
                            
                            myfunc=functools.partial( self.runPlugin, plugin )
                            loc["_actions"].append( self.createAction(plugin.getTitle(), myfunc, None, None, None, False, "triggered()") )
                            plugin=None
                            
        trace.mutter("menus: %s",menus)
        qmenus={}
        keys = menus.keys()
        trace.mutter("keys: %s",keys)
        self.menus["do"].clear()
        for k in keys:
            self.menus["do"].addMenu(self.buildMenu( menus[k],QMenu(capwords(k),self) ) )
#            self.menus[k] = self.buildMenu( menus[k],QMenu(capwords(k),self) ) 
            #            menus[k].addMenu( self.buildMenu(menus[k],QMenu(capwords(k),self)) )

            qmenus[k] = self.buildMenu(menus[k],QMenu(capwords(k),self))
    
    def runPlugin(self,plugin):
        my = plugin
        my.setGooeyEdit( self.getCurrWidget() )
        
        if my.exec_():
            text,graph = my.run()
            trace.mutter("DONE with plugin...")
            
            if not text: text="Nothing to do..."
            self.log( text )
        else:
            pass
     
        self.loadPlugins()
        
    def helpAbout(self):
        self.log("GooeyStat was created by spencer.herzberg@gmail.com\n\nMore information can be found at code.google.com/p/mathapp/")

    def log(self,text=None):
        if self.console:
            if text is not None:
                t = localtime()
                text = "[%d %d %d, %d:%d]:" %(t[1],t[2],t[0],t[3],t[4])+ "\n" + text
                self.console.log(text+"\n")
            else:
                self.console.log("")

    def clearLog(self):
        self.logWidget.clear()
        self.logWidget.selectAll()

    def setStatus(self,msg,t=5000):
        self.status.showMessage(msg,t)

    def getCurrWindow(self):
        sub_window = self.mdi.currentSubWindow()
        if sub_window is None:
            return self.mdi.subWindowList()[0]
        else:
            return sub_window

    def getCurrWidget(self):
        w = self.getCurrWindow()
        if w is None:
            return 
        else:
            return w.widget()

    def addWindow(self,what=None):
        if not what:
            what = Qwidget()
        self.mdi.addSubWindow(what)
        if len( self.mdi.subWindowList() ) == 1:
            what.showMaximized()
        else:
            what.show()

    def setDebugging(self):
        trace.mutter("Yes")
