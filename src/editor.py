from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.Qsci import *

import keyword
import pkgutil
from lexer import PyCustomLexer

# import resource

class Editor(QsciScintilla):

  def __init__(self, parent=None):

    super(Editor, self).__init__(parent)

    # Enconding
    self.setUtf8(True)

    # Font
    self.window_font = QFont("JetBrains Mono") # Font needs to be installed in your computer if its not use somenthing else
    self.window_font.setPointSize(10)
    self.setFont(self.window_font)

    # Brace matching
    self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

    # Indentation
    self.setIndentationGuides(True)
    self.setTabWidth(4)
    self.setIndentationsUseTabs(False)
    self.setAutoIndent(True)

    # Autocomplete
    self.setAutoCompletionSource(QsciScintilla.AcsAll)
    self.setAutoCompletionThreshold(1)
    self.setAutoCompletionCaseSensitivity(False)
    self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

    # Caret
    self.setCaretForegroundColor(QColor("#e0def4"))
    self.setCaretLineVisible(True)
    self.setCaretWidth(2)
    self.setCaretLineBackgroundColor(QColor("#33304A"))

    # EOL
    self.setEolMode(QsciScintilla.EolWindows)
    self.setEolVisibility(False)

    # Lexer for syntax highlighting
    self.pylexer = PyCustomLexer(self)
    self.pylexer.setDefaultFont(self.window_font)

    # Api (you can add autocompletion using this)
    self.api = QsciAPIs(self.pylexer)
    for key in keyword.kwlist + dir(__builtins__): # Adding builtin functions and keywords
      self.api.add(key)

    for _, name, _ in pkgutil.iter_modules(): # Adding all modules names from current interpreter
      self.api.add(name)

    # For test purposes
    # You can add custom function with its parametars and QsciScintilla will handle it for example
    self.api.add("addition(a: int, b: int)")


    self.api.prepare()

    self.setLexer(self.pylexer)

    # Line numbers
    self.setMarginType(0, QsciScintilla.NumberMargin)
    self.setMarginWidth(0, "000")
    self.setMarginsForegroundColor(QColor("#817c9c"))
    self.setMarginsBackgroundColor(QColor("#232136"))
    self.setMarginsFont(self.window_font)

    # Key press
    # self.keyPressEvent = self.handle_editor_press

def keyPressEvent(self, e: QKeyEvent) -> None:
  if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Space:
    self.autoCompleteFromAll()
  else:
    return super().keyPressEvent(e)