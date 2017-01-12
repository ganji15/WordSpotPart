##!/usr/bin/env python
## coding=utf-8

from utils.tools import formatDataset
from utils.Rd_Excel import read_excel

if __name__ == '__main__':
    read_excel(u'同业群信息汇总5.17.xlsx', 'w_a_t')
    formatDataset('w_a_t')