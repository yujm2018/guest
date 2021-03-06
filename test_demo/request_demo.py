# -*- coding: utf-8 -*-
# @Time     : 2018/3/3 19:51
# @Author   : yujianming
# @File     : request_demo.py
# @Software : PyCharm Community Edition
import  requests
import unittest

class GuestTest(unittest.TestCase):

    def test_get_event_list(self):

        r=requests.get("http://127.0.0.1:8000/api/get_event_list",params={"eid":21})

        print(r.json())


    def test_add_event(self):
        event_data={"eid":21,"name":"新建发布会","limit":2000,"address":"北京","start_time":"2017-11-07"}
        r=requests.post("http://127.0.0.1:8000/api/add_event/",data=event_data)
        print(r.json())

if __name__ == '__main__':
    unittest.main()