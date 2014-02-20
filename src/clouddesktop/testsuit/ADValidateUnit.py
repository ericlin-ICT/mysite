#-*- encoding: utf-8 -*-
'''
Created on 2013年11月12日

@author: ericlin
'''
import unittest
from ADValidate import ADValidate
import ldap
import CloudException



class ADValidateUnit(unittest.TestCase):
  '''
  Description:
    Unit test of class Validate
  '''

  def setUp(self):
    
    self.server = '128.192.214.253'
    self.user_email = 'administrator@testlxh.com'
    self.user_name = self.user_email.split('@')[0]
    self.user_pwd = 'Linxianghui@!@#$%^' 
    self.base = 'DC=testlxh,DC=com'
    
    self.ad_validate = ADValidate(server = self.server,
                   port=389, 
                   user_email=self.user_email, 
                   user_pwd=self.user_pwd, 
                   base=self.base,
                   scope=ldap.SCOPE_SUBTREE)
    
    self.dc             = 'DC=testlxh,DC=com' 
    self.ou             = 'ou=Myou1,ou=Myou'
    self.base_dn        = '%s,%s' % (self.ou, self.dc)
    self.option         = ldap.SCOPE_SUBTREE
    self.sAMAccountName = 'yaobingxiong.co'
    self.condition      = 'sAMAccountName=%s' % (self.sAMAccountName)
    self.attrs          = ['memberOf']

  def test_login(self):
    conn = self.ad_validate.validate(self.user_name, self.user_pwd)
 
    s = conn.search_s(self.base_dn, self.option, self.condition, self.attrs)
    print s

  def test_name_and_pwd(self):
    '''
    Description:
      Test name and pwd with the exception CloudException.AUTH_ERROR_BLANK_PARAMETER. 
      Test cases are (name, pwd) = [00,10,01,11]
    '''
    # init var
    res = None
    conn = None
    # 1. (name, pwd) is (0, 1)
    try:
      conn = self.ad_validate.validate(None, self.user_pwd)
    except CloudException.AUTH_ERROR_BLANK_PARAMETER:
      if conn is not None:
        conn.unbind()
      res = True
    # assert 
    self.assertTrue(res == True)
    # 2. (name, pwd) is (1, 0) 
    try:
      conn = self.ad_validate.validate(self.user_name, None)
    except CloudException.AUTH_ERROR_BLANK_PARAMETER:
      if conn is not None:
        conn.unbind()
      res = False
    # assert
    self.assertTrue(res == False)
    # 3. (name, pwd) is (0, 0)
    try:
      conn = self.ad_validate.validate(None, None)
    except CloudException.AUTH_ERROR_BLANK_PARAMETER:
      if conn is not None:
        conn.unbind()
      res = True
    # assert 
    self.assertTrue(res == True)
    # 4. (name, pwd) is (1, 1)
    try:
      conn = self.ad_validate.validate(self.user_name, self.user_pwd)
      res = False
    except CloudException.AUTH_ERROR_BLANK_PARAMETER:
      if conn is not None:
        conn.unbind()
    # assert
    self.assertTrue(res == False)

if __name__ == "__main__":
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()