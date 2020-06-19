"""
 Python Curve Generator
 @Guilherme Trevisan - TrevisanGMW@gmail.com - 2020-01-02
 1.1 - 2020-01-03
 Minor patch.
 
 1.2 - 2020-06-07
 Fixed random window widthHeight issue.
 Updated naming convention to make it clearer. (PEP8)
 Added length checker for selection before running.
 
 1.3 - 2020-06-17
 Changed UI
 Added help menu
 Added icon
 
"""

import maya.cmds as cmds
from decimal import *
from maya import OpenMayaUI as omui

try:
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken import wrapInstance

try:
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide.QtGui import QIcon, QWidget

# Script Name
script_name = "GT - Generate Python Curve"

# Version:
script_version = "1.3"

# Default Settings
close_curve = True
add_import = False

# Function for the "Run Code" button
def run_output_code(out):
    try:
        exec(out)
    except:
        cmds.warning("Something is wrong with your code!")


# Main Form ============================================================================
def build_gui_py_curve():
    window_name = "build_gui_py_curve"
    if cmds.window(window_name, exists =True):
        cmds.deleteUI(window_name)    

    # Main GUI Start Here =================================================================================

    build_gui_py_curve = cmds.window(window_name, title=script_name + "  v" + script_version,\
                          titleBar=True, mnb=False, mxb=False, sizeable =True)
                          
    cmds.window(window_name, e=True, s=True, wh=[1,1])
    
    column_main = cmds.columnLayout() 

    form = cmds.formLayout(p=column_main)

    content_main = cmds.columnLayout(adj = True)


    cmds.separator(h=10, style='none') # Empty Space
    cmds.rowColumnLayout(nc=1, cw=[(1, 270)], cs=[(1, 10)], p=content_main) # Window Size Adjustment
    cmds.rowColumnLayout(nc=3, cw=[(1, 10), (2, 200), (3, 50)], cs=[(1, 10), (2, 0), (3, 0)], p=content_main) # Title Column
    cmds.text(" ", bgc=[0,.5,0]) # Tiny Empty Green Space
    cmds.text(script_name + " v" + script_version, bgc=[0,.5,0],  fn="boldLabelFont", align="left")
    cmds.button( l ="Help", bgc=(0, .5, 0), c=lambda x:build_gui_help_py_curve())
    cmds.separator(h=10, style='none', p=content_main) # Empty Space
    
    # Body ====================
    body_column = cmds.rowColumnLayout(nc=1, cw=[(1, 260)], cs=[(1,10)], p=content_main)
    
    cmds.rowColumnLayout(nc=1, cw=[(1, 260)], cs=[(1,10)])

    settings = cmds.checkBoxGrp(columnWidth2=[150, 1], numberOfCheckBoxes=2, \
                                label1 = 'Add import \"maya.cmds\" ', label2 = "Close Curve", v1 = add_import, v2 = close_curve)
                                
    cmds.rowColumnLayout(nc=1, cw=[(1, 230)], cs=[(1,0)])
    cmds.separator(h=10, style='none') # Empty Space
    cmds.button(l ="Generate", bgc=(.6, .8, .6), c=lambda x:generate_python_curve())
    cmds.separator(h=10, style='none', p=content_main) # Empty Space
    cmds.separator(h=10, p=content_main)
    
    # Bottom ====================
    cmds.rowColumnLayout(nc=1, cw=[(1, 260)], cs=[(1,10)], p=content_main)
    cmds.text(label='Output Python Curve' )
    output_python = cmds.scrollField(editable=True, wordWrap=True)
    cmds.separator(h=10, style='none') # Empty Space
    cmds.button(l ="Run Code", c=lambda x:run_output_code(cmds.scrollField(output_python, query=True, text=True)))
    cmds.separator(h=10, style='none') # Empty Space
    
    def generate_python_curve():
        
        not_curve_error = "Please make sure you selected a Nurbs Curve or a Bezier Curve object before generating it"
        
        if len(cmds.ls(selection=True)) != 0:
            getcontext().prec = 5
            
            shape = cmds.listRelatives(cmds.ls(sl=1)[0],s=1)[0]
            type_checker = str(cmds.objectType(shape))
            

            if "nurbsCurve" in type_checker or "bezierCurve" in type_checker:
                
                cvs = cmds.getAttr(shape+'.cv[*]')
                cvs_list = []
                
                
                for c in cvs:
                    cvs_list.append([float(Decimal("%.3f" % c[0])),float(Decimal("%.3f" % c[1])),float(Decimal("%.3f" % c[2]))])

                if cmds.checkBoxGrp (settings, q=True, value1=True):
                    out = 'import maya.cmds as cmds\n\ncmds.curve(p='
                else:
                    out = 'cmds.curve(p='
                    
                out += '[%s]' % ', '.join(map(str, cvs_list))
                out += ',d='+str(cmds.getAttr(shape+'.degree'))+')'
                
                if cmds.checkBoxGrp (settings, q=True, value2=True):
                    out += '\n\ncmds.closeCurve(ch=False, ps=False, rpo=True)'
                else:
                    pass
                
                print ("#" * 100)
                print out
                print ("#" * 100)
                
                cmds.scrollField(output_python, edit=True, wordWrap=True, text=out ,sl=True)
                cmds.setFocus(output_python)
            else:
                cmds.warning(not_curve_error)
                cmds.scrollField(output_python, edit=True, wordWrap=True, text=not_curve_error ,sl=True)
                cmds.setFocus(output_python)
        else:
            cmds.warning(not_curve_error)

   
    # Show and Lock Window
    cmds.showWindow(build_gui_py_curve)
    cmds.window(window_name, e=True, s=False)
    
    # Set Window Icon
    qw = omui.MQtUtil.findWindow(window_name)
    widget = wrapInstance(long(qw), QWidget)
    icon = QIcon(':/pythonFamily.png')
    widget.setWindowIcon(icon)
    
    # Main GUI Ends Here =================================================================================

# Creates Help GUI
def build_gui_help_py_curve():
    window_name = "build_gui_help_py_curve"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)

    cmds.window(window_name, title= script_name + " Help", mnb=False, mxb=False, s=True)
    cmds.window(window_name, e=True, s=True, wh=[1,1])

    cmds.columnLayout("main_column", p= window_name)
   
    # Title Text
    cmds.separator(h=12, style='none') # Empty Space
    cmds.rowColumnLayout(nc=1, cw=[(1, 310)], cs=[(1, 10)], p="main_column") # Window Size Adjustment
    cmds.rowColumnLayout(nc=1, cw=[(1, 300)], cs=[(1, 10)], p="main_column") # Title Column
    cmds.text(script_name + " Help", bgc=[0,.5,0],  fn="boldLabelFont", align="center")
    cmds.separator(h=10, style='none', p="main_column") # Empty Space

    # Body ====================
    cmds.rowColumnLayout(nc=1, cw=[(1, 300)], cs=[(1,10)], p="main_column")
    cmds.text(l='This script generates the Python code necessary to create', align="left")
    cmds.text(l='a selected curve.', align="left")
    cmds.separator(h=10, style='none') # Empty Space
    cmds.text(l='Make sure you delete the curve\'s history before ', align="left")
    cmds.text(l='generating the code.', align="left")
    cmds.separator(h=15, style='none') # Empty Space
    cmds.text(l='Add import "maya.cmds":', align="left", fn="boldLabelFont")
    cmds.text(l='Adds a line that imports Maya\'s API. This is necessary', align="left")
    cmds.text(l='when running python scripts.', align="left")
    cmds.separator(h=15, style='none') # Empty Space
    cmds.text(l='Close Curve: ', align="left", fn="boldLabelFont")
    cmds.text(l='Adds a line to close the curve after creating it.', align="left")
    cmds.separator(h=15, style='none') # Empty Space
    cmds.text(l='"Generate" button:', align="left", fn="boldLabelFont")
    cmds.text(l='Outputs the python code necessary to create the curve', align="left")
    cmds.text(l='inside the "Output PYthon Curve" box.', align="left")
    cmds.separator(h=15, style='none') # Empty Space
    cmds.text(l='Run Code:', align="left", fn="boldLabelFont")
    cmds.text(l='Attempts to run the code (or anything written) inside ', align="left")
    cmds.text(l='"Output Python Curve" box', align="left")  
    cmds.separator(h=15, style='none') # Empty Space
    cmds.rowColumnLayout(nc=2, cw=[(1, 140),(2, 140)], cs=[(1,10),(2, 0)], p="main_column")
    cmds.text('Guilherme Trevisan  ')
    cmds.text(l='<a href="mailto:trevisangmw@gmail.com">TrevisanGMW@gmail.com</a>', hl=True, highlightColor=[1,1,1])
    cmds.rowColumnLayout(nc=2, cw=[(1, 140),(2, 140)], cs=[(1,10),(2, 0)], p="main_column")
    cmds.separator(h=15, style='none') # Empty Space
    cmds.text(l='<a href="https://github.com/TrevisanGMW">Github</a>', hl=True, highlightColor=[1,1,1])
    cmds.separator(h=7, style='none') # Empty Space
    
    # Close Button 
    cmds.rowColumnLayout(nc=1, cw=[(1, 300)], cs=[(1,10)], p="main_column")
    cmds.separator(h=10, style='none')
    cmds.button(l='OK', h=30, c=lambda args: close_help_gui())
    cmds.separator(h=8, style='none')
    
    # Show and Lock Window
    cmds.showWindow(window_name)
    cmds.window(window_name, e=True, s=False)
    
    # Set Window Icon
    qw = omui.MQtUtil.findWindow(window_name)
    widget = wrapInstance(long(qw), QWidget)
    icon = QIcon(':/question.png')
    widget.setWindowIcon(icon)
    
    def close_help_gui():
        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name, window=True)


#Start current "Main"
build_gui_py_curve()