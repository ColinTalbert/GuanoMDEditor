#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard(pymdwizard) software was developed by the
U.S. Geological Survey Fort Collins Science Center.
See: https://github.com/usgs/fort-pymdwizard for current project source code
See: https://usgs.github.io/fort-pymdwizard/ for current user documentation
See: https://github.com/usgs/fort-pymdwizard/tree/master/examples
    for examples of use in other scripts

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Module contains a variety of miscellaneous functions


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intented to be
    used independently.  All pymdwizard package requirements are needed.
    
    See imports section for external packages used in this script as well as
    inter-package dependencies


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
This software has been approved for release by the U.S. Geological Survey (USGS).
Although the software has been subjected to rigorous review, 
the USGS reserves the right to update the software as needed pursuant to 
further analysis and review. No warranty, expressed or implied, is made by 
the USGS or the U.S. Government as to the functionality of the software and 
related material nor shall the fact of release constitute any such warranty. 
Furthermore, the software is released on condition that neither the USGS nor 
the U.S. Government shall be held liable for any damages resulting from 
its authorized or unauthorized use.

Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.
------------------------------------------------------------------------------
"""

import sys
import os
import traceback
import pkg_resources
import re

try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings


def set_text(widget, text):
    """
    set the text of a widget regardless of it's base type

    Parameters
    ----------
    widget : QtGui:QWidget
            This widget is a QlineEdit or QPlainText edit
    text : str
            The text that will be inserted
    Returns
    -------
    None

    """
    if isinstance(widget, QLineEdit):
        widget.setText(text)
        widget.setCursorPosition(0)

    if isinstance(widget, QPlainTextEdit):
        widget.setPlainText(text)

    if isinstance(widget, QTextBrowser):
        widget.setText(text)

    if isinstance(widget, QComboBox):
        index = widget.findText(text, Qt.MatchFixedString)
        if index >= 0:
            widget.setCurrentIndex(index)
        else:
            widget.setEditText(text)


def launch_widget(Widget, title="", **kwargs):
    """
    run a widget within it's own application
    Parameters
    ----------
    widget : QWidget
    title : str
            The title to use for the application

    Returns
    -------
    None
    """

    try:
        app = QApplication([])
        app.title = title
        widget = Widget(**kwargs)
        print('blah')
        widget.setWindowTitle(title)
        widget.show()
        sys.exit(app.exec_())
        # return widget
    except:
        e = sys.exc_info()[0]
        print('problem encountered', e)
        print(traceback.format_exc())


# def get_resource_path(fname):
#     """
#
#     Parameters
#     ----------
#     fname : str
#             filename that you would like to find
#
#     Returns
#     -------
#             the full file path to the resource specified
#     """
#
#     if getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
#
#         return pkg_resources.resource_filename('guanoeditor',
#                                                'DATA/{}'.format(fname))
#     else:
#         return pkg_resources.resource_filename('guanoeditor',
#                                                'resources/{}'.format(fname))

def set_window_icon(widget, remove_help=True):
    """
    Add our default ducky icon to a widget

    Parameters
    ----------
    widget : PyQt widget
    remove_help : Bool
                  Whether to show the help question mark icon.
    Returns
    -------
    None
    """
    icon = QIcon(get_resource_path('icons/Ducky.ico'))
    widget.setWindowIcon(icon)
    if remove_help:
        widget.setWindowFlags(Qt.Window |
                              Qt.CustomizeWindowHint |
                              Qt.WindowTitleHint |
                              Qt.WindowCloseButtonHint |
                              Qt.WindowStaysOnTopHint)


def get_setting(which, default=None):
    """
    return a pymdwizard application setting

    Parameters
    ----------
    which: str
            name of setting to return

    Returns
    -------
        setting in native format, string, integer, etc

    """
    settings = QSettings('USGS', 'guanoeditor')
    if default is None:
        return settings.value(which)
    else:
        return settings.value(which, default)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        relative_path = relative_path.split('/')[-1]
        return os.path.join(sys._MEIPASS, f"DATA/{relative_path}")
    else:
        return os.path.join(os.path.abspath('.'), relative_path)


def read_namespace(fname):
    namespace_df = pd.read_csv(fname)

    namespace_df = namespace_df[['tag', 'description', 'required', 'data_type', 'picklist']]
    # namespace_df = namespace_df[namespace_df.tag.str.startswith('NABat|')]
    namespace_df.picklist = namespace_df.picklist.fillna('')
    namespace_dict = namespace_df.to_dict('records')

    for thing in namespace_dict:
        if thing['picklist']:
            thing['picklist'] = thing['picklist'].split('|')

    return namespace_dict


def clean_name(fname):
    if isinstance(fname, Path):
        fname = str(fname)

    f = Path(fname)
    name = f.stem
    extension = f.suffix

    # Step 1: remove anything in square brackets
    name = re.sub("\[.*\]", '', name)
    # Step 2: replace any non word characters with underscores
    name = re.sub("\W", '_', name)
    # Step 3: replace multiple underscores with a single
    name = re.sub("_+", '_', name)
    # Step 4: replace underscore separated single digits
    name = re.sub("_[0-9]_", '_', name)
    # Step 5: remove non digit characters at the begining of the file
    name = re.sub("^\D+", '', name)
    # Step 6: remove trailing _000, _001, _005, _0001 etc.
    name = re.sub("_[0-9]{3,4}$", '', name)

    return name + extension
