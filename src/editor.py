from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.Qsci import *

import keyword
import pkgutil
from pathlib import Path
from lexer import PyCustomLexer
from autcompleter import AutoCompleter

# import resource

class Editor(QsciScintilla):

  def __init__(self, parent=None, path: Path = None, is_python_file=True):
    super(Editor, self).__init__(parent)
    self.path = path
    self.full_path = self.path.absolute()
    self.is_python_file = is_python_file

    self.cursorPositionChanged.connect(self._cusorPositionChanged)

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

    if self.is_python_file:
      # Lexer for syntax highlighting
      self.pylexer = PyCustomLexer(self)
      self.pylexer.setDefaultFont(self.window_font)

      self.__api = QsciAPIs(self.pylexer)

      self.auto_completer = AutoCompleter(self.full_path, self.__api)
      self.auto_completer.finished.connect(self.loaded_autocomplete) # you can use this callback to do something

      self.setLexer(self.pylexer)
    else:
      self.setPaper(QColor("#232136"))
      self.setColor(QColor("#e0def4"))

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

  def _cusorPositionChanged(self, line: int, index: int) -> None:
    if self.is_python_file:
      self.auto_completer.get_completions(line+1, index, self.text())

  def loaded_autocomplete(self):
    pass