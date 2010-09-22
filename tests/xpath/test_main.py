#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
from dominic import xpath

def test_api_decorator_raises_exception_to_trim_trace():
    "xpath.api decorator trims the trace for xpath functions"

    def throw_away():
        raise xpath.XPathError('oh yeah, original trace here!')

    try:
        throw_away()
    except xpath.XPathError, error1:
        pass

    try:
        xpath.api(throw_away)()
    except xpath.XPathError, error2:
        pass


