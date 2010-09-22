#!/usr/bin/env python

import dominic
import unittest
from dominic import xpath

class TestRepr(unittest.TestCase):
    """Test the conversion of compiled expressions to strings."""

    def test_repr(self):
        queries = [
            """true and false or true""",
            """1 = 2 or 3 != 4 or 5 <= 6 or 7 >= 9 or 10 > 11 or 12 < 13""",
            """1 + 2 - 3 * 4 div 5 mod 6""",
            """chapter | verse""",
            """4 + -5""",
            """concat(concat("this", 'that'), concat("'a'", '"b"'))""",
            """$a + $prefix:b""",
            """/step/step[1]/step[hop/skip[last()]/jump = 2]""",
            """child::*""",
            """descendant::*""",
            """parent::*""",
            """ancestor::*""",
            """following-sibling::*""",
            """preceding-sibling::*""",
            """following::*""",
            """preceding::*""",
            """attribute::*""",
            """self::*""",
            """descendant-or-self::*""",
            """ancestor-or-self::*""",
            """*:that""",
            """this:*""",
            """this:that""",
            """*:*""",
            """*""",
            """processing-instruction()""",
            """processing-instruction(name)""",
            """processing-instruction('"name"')""",
            """processing-instruction("'name'")""",
            """comment()""",
            """text()""",
            """node()""",
            """(step/step)[1]""",
        ]

        for query in queries:
            expr1 = xpath.XPath(query)
            expr2 = xpath.XPath(str(expr1))
            expr3 = eval(repr(expr2))
            self.failUnlessEqual(str(expr1), str(expr2))
            self.failUnlessEqual(str(expr1), str(expr3))

if __name__ == '__main__':
    unittest.main()
