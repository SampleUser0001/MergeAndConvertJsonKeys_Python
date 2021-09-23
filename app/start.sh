#!/bin/bash

export PYTHON_APP_HOME=`pwd`

cd src
python app.py
# 起動引数を渡したい場合は下記。
# python app.py $1 $2 ...
