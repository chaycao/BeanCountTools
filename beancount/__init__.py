#!~/workspace/PycharmProjects/BeanCountTools/bin/python

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
print(curPath)
print(rootPath)
sys.path.append(rootPath)
sys.path.append(os.path.split(rootPath)[0])