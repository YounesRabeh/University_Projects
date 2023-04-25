#!/usr/bin/env python
import sys
import os
# Add the parent directory of the 'app' folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.graphics.gui import *

app = TkinterApp()
app.mainloop()
