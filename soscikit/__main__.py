# -*- coding: utf-8 -*-
# system libraries
import os.path
import sys
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(parent, "soscikit"))
print(os.path.join(parent, "soscikit"))
from run import main
import threading, webbrowser
url = "http://127.0.0.1:5555/"
threading.Timer(10.0, lambda: webbrowser.open(url)).start()
#Disable debugging to remove the browser opening twice
#main()

if __name__ == "__main__":
    main()
