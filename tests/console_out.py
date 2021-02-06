from logmagic.loggerutil import make_logger
from unittest import TestCase
import unittest
import sys
from io import StringIO
import contextlib
import re


class ConsoleOutTest(TestCase):
    def test_debugout(self):
        # global saved_stdout  # Use sys.__stdout__ instead
        # saved_stdout = sys.stdout
        # global out_stream
        out_stream = StringIO()
        # sys.stdout = out_stream
        with contextlib.redirect_stdout(out_stream):
            with contextlib.redirect_stderr(out_stream):
                logger = make_logger()
                logger.debug('Log Message')
        output = out_stream.getvalue()
        # sys.stdout = saved_stdout  # Use sys.__stdout__ instead
        regex_match = \
            re.fullmatch( \
            '[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} \- Default Logger \- DEBUG \- Log Message\n' \
            , output)
        self.assertIsNotNone(regex_match)


if __name__ == '__main__':
    unittest.main()

