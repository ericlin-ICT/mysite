#-*- encoding: utf-8 -*-
import xlrd
from pandas.core.frame import DataFrame
import re
from clouddesktop.core.query import AsyncQuery
from clouddesktop.core.add import Add

def load_data(file_path, server, port, user_email, pwd, dc):
  data = xlrd.open_workbook(file_path)
  table = data.sheet_by_name(u'新一代用户申请表')
  begin_index = 5
  index = begin_index
  first_cell = table.row_values(index)[0]
  data = []
  while first_cell is not '':
    data.append(table.row_values(index))
    index = index + 1
    first_cell = table.row_values(index)[0]

  print type(server), server
  print type(user_email), user_email
  print type(pwd), pwd
  print type(dc), dc
  print type(port), port
  as_query = AsyncQuery(server,user_email,pwd,dc = dc, port=port)

  for i in range(0, len(data)):
    record = data[i]
    logon_name = record[3]
    desk_name = record[5]
    group = record[6]
    work_group = record[7]
    print str(record)
    # get ad group
    ad_group = assign_group(desk_name, group, work_group)
    record.append(ad_group)
    # get add status
    add_status = verify_data(as_query, user_email, pwd, logon_name, ad_group)
    record.append(add_status)
    
    data[i] = record
  
  #print DataFrame(data)
  return data
    
def verify_data(as_query, user_email, pwd, logon_name, ad_groups):
  groups = as_query.async_get_group(logon_name) 
  #print groups
  if groups is None:
    return 'No User'
  elif groups is '':
    return 'Good'
  else:
    groups = groups[1]
    #print 'groups', groups
    #print 'ad_groups', ad_groups
    gps = re.findall(r'CN=(.*?),', str(groups))
    #print 'gps', gps
    for ad_group in ad_groups:
      for gp in gps:
        if gp == ad_group:
          return 'Duplicate group'
    else:
      return 'Good'

'''
def assign_group(desk_name, group, work_group):
  ad_group = None
  if desk_name == '业务评审应用':
    ad_group = ['GP_XA_TrainingUsers']
    return ad_group
  
  if group == '业务组_行内':
    ad_group = ['GP_01_YEWU']
  elif group == '业务组_行外':
    ad_group = ['GP_02_YEWU']
  elif group == '技术组_行内':
    ad_group = ['GP_03_JISHU']
  elif group == '技术组_行外':
    ad_group = ['GP_04_JISHU']
  elif group == '数据组_行内':
    ad_group = ['GP_05_SHUJU']
  elif group == '数据组_行外':
    ad_group = ['GP_06_SHUJU']
  elif group == '流程组_行内':
    ad_group = ['GP_07_LIUCHENG']
  elif group == '流程组_行外':
    ad_group = ['GP_08_LIUCHENG']
  elif group == '技术评价组':
    ad_group = ['GP_09_PINGJIA']
  elif group == '新一代一期项目组_行内':
    ad_group = ['GP_29_Project']
    if desk_name == '建模桌面':
      ad_group.append('GP_29_Project_EM')
    elif desk_name == '开发测试桌面':
      ad_group.append('GP_29_Project_RD')
  elif group == '新一代一期项目组_行外':
    ad_group = ['GP_30_Project_V']
    if desk_name == '建模桌面':
      ad_group.append('GP_30_Project_V_RD')
    elif desk_name == '开发测试桌面':
      ad_group.append('GP_30_Project_V_EM')
  else:
    ad_group = None
  
  return ad_group
'''
  
def assign_group(desk_name, group, work_group):
  ad_group = None
  if desk_name == '业务评审应用':
    ad_group = ['GP_XA_TrainingUsers']
    return ad_group
  
  if group == '业务组':
    if work_group == '行内':
      ad_group = ['GP_01_YEWU']
    if work_group == '行外':
      ad_group = ['GP_02_YEWU_V']
  elif group == '技术组':
    if work_group == '行内':
      ad_group = ['GP_03_JISHU']
    if work_group == '行外':
      ad_group = ['GP_04_JISHU_V']
  elif group == '数据组':
    if work_group == '行内':
      ad_group = ['GP_05_SHUJU']
    if work_group == '行外':
      ad_group = ['GP_06_SHUJU_V']
  elif group == '流程组':
    if work_group == '行内':
      ad_group = ['GP_07_LIUCHENG']
    if work_group == '行外':
      ad_group = ['GP_08_LIUCHENG_V']
  elif group == '技术评价组':
    ad_group = ['GP_09_PINGJIA']
  elif group == '项目组' or group == '其他':
    if work_group == '行内':
      ad_group = ['GP_29_Project']
      if desk_name == '建模桌面':
        ad_group.append('GP_29_Project_EM')
      elif desk_name == '开发测试桌面':
        ad_group.append('GP_29_Project_RD')
    if work_group == '行外':
      ad_group = ['GP_30_Project_V']
      if desk_name == '建模桌面':
        ad_group.append('GP_30_Project_V_RD')
      elif desk_name == '开发测试桌面':
        ad_group.append('GP_30_Project_V_EM')
  else:
    ad_group = None
  
  return ad_group

def assign_resource(data,server, port, user_email, pwd, dc):
  adder = Add(server, user_email,pwd,dc,port)
  as_query = AsyncQuery(server,user_email,pwd,dc = dc, port=port)
  for record in data:
    logon_name = record[3]
    gps = record[13]
    flag = record[14]
    if flag is 'Good':
      user_dn = as_query.async_get_dn(logon_name)
      for gp in gps:
        gp_dn = as_query.async_get_dn(gp)
        print 'gp', gp_dn
        print 'user', user_dn.decode('utf-8')
        print adder.add_group(str(gp_dn.decode('utf-8')), str(user_dn.decode('utf-8')))

if __name__ == '__main__':
  file_path = unicode('D:/工作内容/云桌面/云桌面运维/用户添加/201402/20140214新一代开发测试桌面云用户服务申请表20131219.xls', 'utf-8')
  print file_path
  server = '128.192.214.251'
  port = 389
  user_email = 'lxhadmin@lxhtest.com'
  pwd = '123'
  dc = 'dc=lxhtest,dc=com'
  
  '''
  server = '128.192.214.21'
  port = 389
  user_email = 'linxianghui.zh@ccbkfcs.com'
  pwd = 'kse20711666'
  dc = 'dc=ccbkfcs,dc=com'
  '''
  
  data = load_data(file_path, server, port, user_email, pwd, dc)
  assign_resource(data, server, port, user_email, pwd, dc)
  desk_name = ''
  group = '业务组_行内'
  work_group = ''
  #print assign_group(desk_name, group, work_group)