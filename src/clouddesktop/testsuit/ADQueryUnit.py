#-*- encoding: utf-8 -*-
'''
Created on 2013年11月12日

@author: ericlin
'''
import unittest
import ldap
from src.clouddesktop.core import ADValidate, ADQuery


class ADQueryUnit(unittest.TestCase):


  def setUp(self):
    self.server = '128.192.214.253'
    self.user_email = 'administrator@testlxh.com'
    self.user_name = self.user_email.split('@')[0]
    self.user_pwd = 'Linxianghui@123456' 
    self.base = 'DC=testlxh,DC=com'
    self.ad_validate = ADValidate(server = self.server,
                   port=389, 
                   user_email=self.user_email, 
                   user_pwd=self.user_pwd, 
                   base_dc=self.base,
                   scope=ldap.SCOPE_SUBTREE)
    self.handle = self.ad_validate.validate(self.user_name, self.user_pwd)
    dc = 'DC=testlxh,DC=com' 
    self.ad_query = ADQuery(dc, self.handle)

  def tearDown(self):
    pass


  def test_find_name(self):
    res = self.ad_query.find_gourp_by_aAMAccountName('tanhao.zh')
    self.assertTrue( '' == res)
  
  def test_find_names(self):
    names = ['jizhaohui.zh','yaobingxiong.co', 'yaoyanjie.co', 'jjj.zh', 'tanhao.zh','jizhaohui.zh' ]
    res = self.ad_query.find_group_by_aAMAccountNames(names)
    size = res.index.size
    self.assertTrue(6 == size)
  
    print res.index
    print res


if __name__ == "__main__":
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()