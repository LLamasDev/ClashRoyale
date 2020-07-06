#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

db = pymysql.connect('localhost', 'root', '', 'bot')
cursor = db.cursor()

try:
   cursor.execute('UPDATE clanes SET spam = "si"')
   db.commit()
except:
   db.rollback()

db.close()