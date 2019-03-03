# -*- coding: utf-8 -*-
# Created by Administrator on 2017/11/13
import unittest
import sys
sys.path.append("./test_demo")
from count import Count


class CountAddTest(unittest.TestCase):

    def setUp(self):
        self.count = Count()

    def tearDown(self):
        pass

    # 必须以“test”开头
    def test_case1(self):
        result = self.count.add(3, 5)
        self.assertEqual(result, 8)

    # 必须以“test”开头
    def test_case2(self):
        result = self.count.add(30, 50)
        self.assertEqual(result, 80)


if __name__ == "__main__":
    #unittest.main()
    # 添加测试用例到测试套件
    suit = unittest.TestSuite()
    suit.addTest(CountAddTest("test_case1"))
    suit.addTest(CountAddTest("test_case2"))
    # 执行测试套件里面的用例
    runner = unittest.TextTestRunner()
    runner.run(suit)