#-*- encoding: utf-8 -*-
'''
Created on 2013年11月18日

@author: ericlin
'''
import pandas as pd
import logging
from pandas.core.index import Index

class UserLoader(object):
  '''
  Description:
    --------------------------------------------------------
    Load user information from the csv file
    --------------------------------------------------------
  '''

  def __init__(self, filename):
    '''
    Description:
      Constructor
    Args:
      --------------------------------------------------------
      filename  string  full path of the csv file
      --------------------------------------------------------
    '''
    self.filename = filename
    self.logger = logging.getLogger("UserLoaderLogger")
    
  def load_csv(self):
    '''
    Description:
      load csv file
    Return:
      --------------------------------------------------------
      df  DataFram  padas df with colums ['organization','user_name',
                    'logon_name','apply_type','desk_name','group',
                    'work_group','desc','date','repeat_time','ad_group']
                    ,None if failed.
      --------------------------------------------------------
    '''
    #df = DataFrame.from_csv(path=self.filename, sep=',')
    df = None
    
    try:
      # load file
      df = pd.read_csv(self.filename)
      col_lst = ['organization','user_name',
                 'logon_name','apply_type',
                 'desk_name','group',
                 'work_group','desc',
                 'date','repeat_time',
                 'ad_group']
      std_colunms = Index(col_lst)
      # check format
      if df.columns != std_colunms:
        df = None
        self.logger.error("文件: %s 格式错误" % self.filename)
        
    except Exception,e:
      df = None
      self.logger.debug(e)
      self.logger.error("加载文件: %s 失败. %s" % (self.filename, e))
      
    finally:
      return df
  
# module test
if __name__ == '__main__':
  import time
  localtime = time.localtime()
  logfile = '%s%s%s.log' % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
  logging.basicConfig(level=logging.DEBUG,
                format='[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='log/%s' % (logfile) )

  filename = './experiment/user.csv'
  loader = UserLoader(filename)
  df = loader.load_csv()
  if df is not None:
    print df.columns
    print df['user_name']
    print df['logon_name']
    print df['organization']
  print df