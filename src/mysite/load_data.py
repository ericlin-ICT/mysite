#-*- encoding: utf-8 -*-
import xlrd
from pandas.core.frame import DataFrame

def load_data(file_path):
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

  df = DataFrame(data)
  print df
  return df

if __name__ == '__main__':
  file_path = 'C:/Users/ericlin/Desktop/20140122.xlsx'
  load_data(file_path)