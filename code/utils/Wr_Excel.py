# -*- coding: utf-8 -*-
import xlrd
import xlwt


def set_style(name,height,bold=False):
  style = xlwt.XFStyle() # 初始化样式
  font = xlwt.Font() # 为样式创建字体
  font.name = name # 'Times New Roman'
  font.bold = bold
  font.color_index = 4
  font.height = height
  style.font = font
  return style


#写excel
def write_excel(rows):
    filename=xlwt.Workbook()
    sheet1=filename.add_sheet("my_sheet")
    row0 = [u'业务描述',u'业务品种',u'方向',u'期限',u'利率',u'金额',u'类型',u'交易对手',u'评级',u'债券发行人',u'备注']
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
    for i in xrange (len(rows)):
        sheet1.write(i+1,0,rows[i][0][0])
        for j in xrange(len(rows[i][1])):
            sheet1.write(i+1,j+1,rows[i][1][j])
    filename.save('output.xls')


if __name__ == '__main__':
    rows=[]
    workbook = xlrd.open_workbook(r'1.xlsx')
    print workbook.sheet_names() # [u'sheet1', u'sheet2']
    sheet1_name = workbook.sheet_names()[0]
    # 根据sheet索引或者名称获取sheet内容
    sheet1 = workbook.sheet_by_index(0) # sheet索引从0开始
    sheet1 = workbook.sheet_by_name('Sheet1')
    # sheet的名称，行数，列数
    print sheet1.name,sheet1.nrows,sheet1.ncols
    N_row=sheet1.nrows
    # 获取整行和整列的值（数组）
    for i in xrange (N_row):
        rows_v0=[]
        rows0=[]
        rows_v=sheet1.row_values(i)
        rows_v0.append(rows_v[1])
        rows_v1=rows_v[2:]
        print type(rows_v1),len(rows_v0),len(rows_v1),len(rows_v)
        rows0.append(rows_v0)
        rows0.append(rows_v1)
        rows.append(rows0)
        print len(rows[i][0]),len(rows[i][1])
    write_excel(rows)
