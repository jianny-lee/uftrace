#!/usr/bin/env python

from runtest import TestBase
import subprocess as sp
import os.path

TDIR  = 'xxx'

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'sdt', """
# DURATION    TID     FUNCTION
   9.392 us [28141] | __monstartup();
  12.912 us [28141] | __cxa_atexit();
            [28141] | main() {
            [28141] |   foo() {
            [28141] |     /* uftrace:event */
   2.896 us [28141] |   } /* foo */
   3.017 us [28141] | } /* main */
""")

    def prerun(self, timeout):
        self.gen_port()

        self.subcmd = 'recv'
        self.option = '-d %s --port %s' % (TDIR, self.port)
        self.exearg = ''
        recv_cmd = self.runcmd()
        self.pr_debug('prerun command: ' + recv_cmd)
        self.recv_p = sp.Popen(recv_cmd.split())

        self.subcmd = 'record'
        self.option = '-H %s --port %s -E uftrace:event' % ('localhost', self.port)
        self.exearg = 't-' + self.name
        record_cmd = self.runcmd()
        self.pr_debug('prerun command: ' + record_cmd)
        sp.call(record_cmd.split())

        return TestBase.TEST_SUCCESS

    def setup(self):
        self.subcmd = 'replay'
        self.option = '-d ' + os.path.join(TDIR, 'uftrace.data')
        self.exearg = ''

    def postrun(self, ret):
        self.recv_p.terminate()
        return ret
