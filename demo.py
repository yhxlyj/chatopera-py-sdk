#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright (c) 2018 <> All Rights Reserved
#
#
# File: /Users/hain/chatopera/chatopera-py-sdk/test.py
# Author: Hai Liang Wang
# Date: 2019-03-11:20:03:56
#
#===============================================================================

"""
   
"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2018 . All Rights Reserved"
__author__    = "Hai Liang Wang"
__date__      = "2019-03-11:20:03:56"


import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir + '/app')

if sys.version_info[0] < 3:
    # raise "Must be using Python 3"
    pass
else:
    unicode = str

# Get ENV
ENVIRON = os.environ.copy()

from absl import flags   #absl-py
from absl import logging #absl-py
from absl import app #absl-py

from chatopera import Chatbot

FLAGS = flags.FLAGS
flags.DEFINE_string('bot_ip', '127.0.0.1', 'Chatopera Superbrain Service IP')
flags.DEFINE_integer('bot_port', 8003, 'Chatopera Superbrain Service Port')
flags.DEFINE_string('bot_id', 'test1', 'Connect to which Chatbot in Superbrain')

import unittest

# run testcase: python /Users/hain/chatopera/chatopera-py-sdk/test.py Test.testExample
class Test(unittest.TestCase):
    '''
    
    '''
    def setUp(self):
        self.bot = Chatbot(FLAGS.bot_ip, FLAGS.bot_port, FLAGS.bot_id)

    def tearDown(self):
        pass

    def test_conversation(self):
        logging.info("test_conversation %s:%d/api/v1/chatbot/%s", FLAGS.bot_ip, FLAGS.bot_port, FLAGS.bot_id)
        resp = self.bot.conversation("py", "今天北京天气怎么样")
        logging.info("rc: %s", resp["rc"])
        logging.info("conversation: service provider [%s], logic_is_unexpected %s, logic_is_fallback %s", \
                     resp["data"]["service"]["provider"], \
                     resp["data"]["logic_is_unexpected"], \
                     resp["data"]["logic_is_fallback"])

        assert resp["data"]["service"]["provider"] == "mute"
        assert resp["data"]["logic_is_unexpected"] == False

        logging.info(resp["data"]["string"])

        logging.info("faq: %d", len(resp["data"]["faq"]))
        if resp["rc"] == 0:
            for x in resp["data"]["faq"]:
                logging.info("%f match: %s, reply: %s", x["score"], x["post"], x["reply"])


    def test_faq(self):
        logging.info("test_faq %s:%d/api/v1/chatbot/%s", FLAGS.bot_ip, FLAGS.bot_port, FLAGS.bot_id)
        
        resp = self.bot.faq("py", "利息")
        logging.info("rc: %s", resp["rc"])
        if resp["rc"] == 0:
            for x in resp["data"]:
                logging.info("%f match: %s, reply: %s", x["score"], x["post"], x["reply"])


    def test_mute(self):
        logging.info("test_mute")
        self.bot.mute("py")
        resp = self.bot.conversation("py", "今天北京天气怎么样")
        logging.info("rc: %s", resp["rc"])
        logging.info("conversation: service provider [%s], logic_is_unexpected %s", \
                     resp["data"]["service"]["provider"], \
                     resp["data"]["logic_is_unexpected"])

        assert resp["data"]["service"]["provider"] == "mute"
        assert resp["data"]["logic_is_unexpected"] == False
        logging.info(resp["data"]["string"])

    def test_unmute(self):
        logging.info("test_unmute")
        self.bot.unmute("py")
        resp = self.bot.conversation("py", "今天北京天气怎么样")
        logging.info("rc: %s", resp["rc"])
        logging.info("conversation: service provider [%s], logic_is_unexpected %s", \
                     resp["data"]["service"]["provider"], \
                     resp["data"]["logic_is_unexpected"])

        assert resp["data"]["service"]["provider"] == "fallback"
        assert resp["data"]["logic_is_unexpected"] == True
        logging.info(resp["data"]["string"])

    def test_ismute(self):
        logging.info("test_ismute")
        print(self.bot.ismute("py"))

    def test_profile(self):
        logging.info("test_profile")
        print(self.bot.profile("py"))

    def test_chats(self):
        logging.info("test_chats")
        print(self.bot.chats("py", 2))

def test():
    suite = unittest.TestSuite()
    # suite.addTest(Test("test_conversation"))
    # suite.addTest(Test("test_faq"))
    # suite.addTest(Test("test_mute"))
    # suite.addTest(Test("test_unmute"))
    # suite.addTest(Test("test_ismute"))
    suite.addTest(Test("test_chats"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

def main(argv):
    test()

if __name__ == '__main__':
    # FLAGS([__file__, '--verbosity', '1']) # DEBUG 1; INFO 0; WARNING -1
    app.run(main)