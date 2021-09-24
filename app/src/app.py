# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG
import os
import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum
import importenv as setting
import json
import glob

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(PYTHON_APP_HOME + '/config/log_config.json')
config.dictConfig(log_conf)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

def get_keys(dic):
  return_list = []

  for key in dic.keys():
    item = dic[key]
    return_list.append(key)
    if isinstance(item, dict):
      return_list.append(get_keys(item))

  return return_list

def merge(dic, origin):
  logger.debug('before origin keys : {}'.format(get_keys(origin)))
  logger.debug('before    dic keys : {}'.format(get_keys(dic)))
  origin.update(dic)
  logger.debug('after  origin keys : {}'.format(get_keys(origin)))

  for key in dic.keys():
    # originを戻す想定。originになくて、dicにあるものをマージしたい。
    # 型判定する。dictを持っていた場合再帰呼び出しする。
    dic_item = dic[key]
    if isinstance(dic_item, dict):
      origin[key] = merge(dic_item, origin[key])

  logger.debug('return origin keys : {}'.format(get_keys(origin)))
  return origin

if __name__ == '__main__':
  # .envの取得
  # setting.ENV_DIC[ImportEnvKeyEnum.importenvに書いた値.value]
  
  # 起動引数の取得
  # args = sys.argv
  # args[0]はpythonのファイル名。
  # 実際の引数はargs[1]から。

  merged_dict = {}
  key_list = []
  for file in [p for p in glob.glob(PYTHON_APP_HOME + '/input/*' , recursive=True) if os.path.isfile(p) and os.path.splitext(p)[1][1:] != 'gitkeep' ]:
    logger.info(file)

    with open(file, mode='r') as f:
      merged_dict = merge(json.load(f), merged_dict)

  logger.info(merged_dict)
  with open(PYTHON_APP_HOME + '/output/result.json', mode='w', encoding='utf8') as f:
    f.write(json.dumps(merged_dict))
