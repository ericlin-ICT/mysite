#-*- encoding: utf-8 -*-
'''
Created on 2013年12月16日

@author: ericlin
'''

import ldap
import logging
from ldap.ldapobject import LDAPObject

class Add(object):
  '''
  Description: 
    --------------------------------------------------------
    Add a user to a group
    --------------------------------------------------------
  '''

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
    self.ldap_obj = LDAPObject(self.uri)
    self.ldap_obj.protocol_version = ldap.VERSION3
    self.ldap_obj.set_option(ldap.OPT_REFERRALS,0)
    self.ldap_obj.simple_bind_s(self.user_email, self.pwd)
  
  def __disconnect(self):
    self.ldap_obj.unbind_ext_s()  
  
  def add_group(self, gp_dn, user_dn):
    self.__connect()
    attrib = ([(ldap.MOD_ADD,'member', user_dn)])
    success = False
    print type(gp_dn), gp_dn
    print type(user_dn), user_dn
    try:
      self.ldap_obj.modify_s(gp_dn, attrib)
      success = True
    except Exception, e:
      print e
    finally:
      self.__disconnect()
      return success
  
  def delete_group(self, gp_dn, user_dn):
    self.__connect()
    attrib = ([(ldap.MOD_DELETE,'member', user_dn)])
    success = False
    
    try:
      self.ldap_obj.modify_s(gp_dn, attrib)
      success = True
    except Exception, e:
      print e
    finally:
      self.__disconnect()
      return success
    
if __name__=='__main__':
  server = '128.192.214.251'
  port = 389
  user_email = 'lxhadmin@lxhtest.com'
  pwd = '123'
  dc = 'dc=lxhtest,dc=com'
  sAMAccountName= 'lxhadmin'
  user_dn = 'CN=张慧民,OU=ccb,OU=User Accounts,DC=lxhtest,DC=com'
  gp_dn = 'CN=GP_01_YEWU,OU=Citrix Admins,OU=User Accounts,DC=lxhtest,DC=com'
  add = Add(server,user_email,pwd,dc = dc, port=ldap.PORT )
  add.add_group(gp_dn, user_dn)
  #add.delete_group(gp_dn, user_dn)
  #res = q.find_gourp_by_aAMAccountName(sAMAccountName)
  #print res
  
  #conn = ldap.initialize('ldap://128.192.214.251:389')
  #conn.simple_bind(user_email, pwd)
      # do search
 
  
  