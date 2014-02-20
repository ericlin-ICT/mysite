#-*- encoding: utf-8 -*-
'''
Created on 2014年2月14日

@author: ericlin
'''
import logging
import ldap.resiter
from pandas.core.frame import DataFrame
import re

class Query(ldap.resiter.ResultProcessor):
  '''
  Description: 
    --------------------------------------------------------
    perform ad query operation
    --------------------------------------------------------
  '''

  def __init__(self, 
               server,
               user_email,
               password,
               dc,
               port = 389 ):
    '''
    Description: 
      --------------------------------------------------------
      Constructor
      --------------------------------------------------------
    Args:
      --------------------------------------------------------
      dc      string    domain control string(like 'DC=testlxh,DC=com')
      handle  SimpleLDAPObject  connection handle, default null
      ---------------------------------------------------------
    Exception:
      ---------------------------------------------------------
      throw QueryException 
      ---------------------------------------------------------
    '''
    
    self.dc = dc
    self.server = server
    self.port = port
    self.user_email = user_email
    self.pwd = password
    self.logger = logging.getLogger("ADQueryLogger")
    self.conn = ldap.initialize('ldap://128.192.214.251:389')
    self.conn.simple_bind(user_email, pwd)
  
  def get_group(self, sAMAccountName=''):
    '''
    Description:
      --------------------------------------------------------
      Use aAMAccountName as condition to search user's group info
      --------------------------------------------------------
    Args:
      --------------------------------------------------------
      sAMAccountName      string   user name in ccb(like linxianghui.zh) 
      ---------------------------------------------------------
    Return:
      ---------------------------------------------------------
      json string with "username:memberof", None if failed
      ---------------------------------------------------------
    '''
    
    # construct search condition 
    option    = ldap.SCOPE_SUBTREE
    condition = 'sAMAccountName=%s' % (sAMAccountName)
    attrs     = ['sAMAccountName','memberOf']
    
    res = None
    #try:
    # Asynchronous search method

      # do search
    #s = conn.search_s(self.dc, option, condition, attrs)
    msg_id = self.conn.search(self.dc, option, condition, attrs)
    for item in self.allresults(msg_id):
      print item
  
  
   
  def get_dn(self, sAMAccountName=''):
    '''
    Description:
      --------------------------------------------------------
      get distinguished name by sAMAccountName
      --------------------------------------------------------
    Args:
      ----------------------------------------------------------
      sAMAccountName  string  Object's flpm id
      ----------------------------------------------------------
    Return:
      ----------------------------------------------------------
      distinguished name of the obj, None if failed
      ----------------------------------------------------------
    '''
   
    # construct search condition 
    option    = ldap.SCOPE_SUBTREE
    condition = 'sAMAccountName=%s' % (sAMAccountName)
    attrs     = ['distinguishedName']
    
    # do search
    try:
      # search AD
      res = self.handle.search_s(self.dc, option, condition, attrs)
    except ldap.error, e :
      res = None
      self.logger.debug(e)
      self.logger.error("查询  %s 失败" % sAMAccountName)
    except Exception, e:
      res = None
      self.logger.debug(e)
      self.logger.error("查询  %s 失败" % sAMAccountName)
    
    finally:
      return res
   
class InnerLDAPObject(ldap.ldapobject.LDAPObject,ldap.resiter.ResultProcessor):
  pass

class AsyncQuery(object):
  def __init__(self,
               server,
               user_email,
               password,
               dc,
               port = 389):
    self.dc = dc
    self.server = server
    self.port = port
    self.user_email = user_email
    self.pwd = password
    self.logger = logging.getLogger("ADQueryLogger")
    self.uri = 'ldap://' + self.server + ':' + str(self.port)

  def __connect(self):
    self.ldap_obj = InnerLDAPObject(self.uri)
    self.ldap_obj.protocol_version = ldap.VERSION3
    self.ldap_obj.set_option(ldap.OPT_REFERRALS,0)
    self.ldap_obj.simple_bind_s(self.user_email, self.pwd)
  
  def __disconnect(self):
    self.ldap_obj.unbind_ext_s()
    #print 'disconnect'
  
  def async_get_dn(self, sAMAccountName):
    self.__connect()
    option    = ldap.SCOPE_SUBTREE
    condition = 'sAMAccountName=%s' % (sAMAccountName)
    attrs     = ['distinguishedName'] 
    try:
      msg_id = self.ldap_obj.search(self.dc, option, condition, attrs)
      
      s = ''
      res = None
      for i in self.ldap_obj.allresults(msg_id, 10):
        s = i[1]
        break
      #print 's:', s
      # not find user, return None
      if str(s).find('distinguishedName') == -1:
        return None
      
      df_tmp = DataFrame(s, columns=['user', 'attrs'])
      # get first record attrs dict
      attrs = df_tmp['attrs'][0]
      #print 'attr:', attrs
      # find memberOf attr
      if 'distinguishedName' in attrs.keys():
        dn = attrs['distinguishedName']
        #print str(dn)
        res = dn[0]
        print 'res', res
        print 'typs', type(res)
    except Exception, e:
      print e
    finally:
      self.__disconnect()
      return res
      
  def async_get_group(self, sAMAccountName): # Asynchronous search method
    self.__connect()
    option    = ldap.SCOPE_SUBTREE
    condition = 'sAMAccountName=%s' % (sAMAccountName)
    attrs     = ['sAMAccountName', 
                 'memberOf',] 
    
    res = None
    try:
      msg_id = self.ldap_obj.search(self.dc, option, condition, attrs)
    
      s = ''
      for i in self.ldap_obj.allresults(msg_id, 10):
        s = i[1]
        break
      
      # not find user, return None
      if str(s).find('sAMAccountName') == -1:
        return None
      
      if str(s).find('memberOf') == -1:
        res = ''
      
      #print s
      df_tmp = DataFrame(s, columns=['user', 'attrs'])
      # get first record attrs dict
      attrs = df_tmp['attrs'][0]
      # find memberOf attr
      if 'memberOf' in attrs.keys():
        memberof = attrs['memberOf']
        res = (sAMAccountName, memberof)
      
      return res
    
    except Exception,e:
      print e
    finally:
      self.__disconnect()
   
if __name__=='__main__':
  server = '128.192.214.251'
  port = 389
  user_email = 'lxhadmin@lxhtest.com'
  pwd = '123'
  dc = 'dc=lxhtest,dc=com'
  
  #q = query(server,user_email,pwd,dc = dc, port=ldap.PORT )
  
  sAMAccountName= 'lxhadmin'
  
  #res = q.find_gourp_by_aAMAccountName(sAMAccountName)
  #print res
  
  #conn = ldap.initialize('ldap://128.192.214.251:389')
  #conn.simple_bind(user_email, pwd)
      # do search
  option    = ldap.SCOPE_SUBTREE
  condition = 'sAMAccountName=%s' % (sAMAccountName)
  attrs     = ['sAMAccountName','memberOf']
  #s = conn.search_s(dc, option, condition, attrs)
  #print s
  aQuery = AsyncQuery(server,user_email,pwd,dc = dc, port=ldap.PORT )
  print aQuery.async_get_group(sAMAccountName)
  #print aQuery.async_get_dn(sAMAccountName)
  




'''
  # Asynchronous search method
  msg_id = conn.search(dc, option, condition)
  ldap.ldapobject.LDAPObject
  for item in conn.allresults(msg_id):
    print item
'''

#for res_type,res_data,res_msgid,res_controls in conn.allresults(msg_id):
  
  
  
  
  
  
  