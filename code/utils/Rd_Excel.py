##!/usr/bin/env python
#coding=gbk

import xlrd
import cPickle as pkl
Dic=[]
w_a_t=[]

def read_excel(src_path, dst_path):
  # OPEN FILE
  workbook = xlrd.open_workbook(src_path)
  # ��ȡ����sheet
  print workbook.sheet_names() # [u'sheet1', u'sheet2']
  sheet1_name = workbook.sheet_names()[0]
  # ����sheet�����������ƻ�ȡsheet����
  sheet1 = workbook.sheet_by_index(0) # sheet������0��ʼ
  sheet1 = workbook.sheet_by_name('Sheet1')
  # sheet�����ƣ�����������
  print sheet1.name,sheet1.nrows,sheet1.ncols
  # ��ȡ���к����е�ֵ�����飩
  for i in xrange (1017):
      print i
      w_t=[]
      w_t1=[]
      w_t.append(sheet1.cell_value(i+1,1).encode('utf-8'))
      print w_t[0],len(sheet1.cell_value(i+1,1))

      for world in sheet1.cell_value(i+1,1):
          m=0
          for j in xrange (10):
             if type(sheet1.cell_value(i+1,j+2)) is unicode :
                 a=sheet1.cell_value(i+1,j+2)
             else: a=str(sheet1.cell_value(i+1,j+2)).decode('utf-8')
             l=len(a)
             for o in xrange(l):
                 if world==a[o]:
                     m=1,
                     n=j
          if m:
            w_t1.append(n)
          else: w_t1.append(10)
      w_t.append(w_t1)
      w_a_t.append(w_t)
      print w_a_t[i][0]

  with open(dst_path,'w') as f:
    pkl.dump(w_a_t, f)

