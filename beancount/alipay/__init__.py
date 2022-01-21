import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]
print(rootPath)
sys.path.append(rootPath)

sys.path.append("/beancount")