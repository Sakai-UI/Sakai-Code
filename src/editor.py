from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.Qsci import *


class Editor(QsciScintilla):

  def __init__(self, parent=None):
    super(Editor, self).__init__(parent)