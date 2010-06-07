# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <dominic - python-pure implementation of CSS Selectors>
# Copyright (C) <2010>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
from sure import that
from tests.base import with_fixture
from dominic import DOM, Element

@with_fixture
def select_paragraphs(context):
    "dominic selecting paragraphs"
    dom = DOM(context.html)

    identifiers = ["firstp", "ap", "sndp", "en", "sap", "first"]
    paragraphs = dom.find("p")

    assert that(dom).is_a(DOM)
    for identifier, paragraph in zip(identifiers, paragraphs):
        assert that(paragraph.attribute['id']).equals(identifier)

@with_fixture
def select_html(context):
    "dominic selecting html"
    dom = DOM(context.html)

    html = dom.get("html")
    assert that(html).is_a(Element)
    assert that(html.attribute['id']).equals("html")

@with_fixture
def select_body(context):
    "dominic selecting body"
    dom = DOM(context.html)

    (body, ) = dom.find("body")
    assert that(body).is_a(Element)
    assert that(body.attribute['id']).equals("body")

@with_fixture
def select_parent_element(context):
    "dominic selecting by parent element"
    dom = DOM(context.html)

    identifiers = ["firstp", "ap", "sndp", "en", "sap", "first"]
    paragraphs1 = dom.find("div p")
    paragraphs2 = dom.find("body p")

    assert that(dom).is_a(DOM)

    assert that(paragraphs1).len_is(6)
    assert that(paragraphs2).len_is(6)

    for identifier, paragraph in zip(identifiers, paragraphs1):
        assert that(paragraph.attribute['id']).equals(identifier)

    for identifier, paragraph in zip(identifiers, paragraphs2):
        assert that(paragraph.attribute['id']).equals(identifier)

@with_fixture
def select_by_id(context):
    "dominic selecting by id"
    dom = DOM(context.html)

    (body, ) = dom.find("#firstp")
    assert that(body).is_a(Element)
    assert that(body.attribute['id']).equals("firstp")

@with_fixture
def select_by_class(context):
    "dominic selecting by class name"
    dom = DOM(context.html)

    (body, ) = dom.find(".nothiddendiv")
    assert that(body).is_a(Element)
    assert that(body.attribute['id']).equals("nothiddendiv")
    assert that(body.attribute['style']).has("height:1px;")
    assert that(body.attribute['style']).has("background:white;")

@with_fixture
def select_by_attribute_class(context):
    "dominic selecting by attribute (class)"
    dom = DOM(context.html)

    (body, ) = dom.find("[class=nothiddendiv]")
    assert that(body).is_a(Element)
    assert that(body.attribute['id']).equals("nothiddendiv")
    assert that(body.attribute['style']).has("height:1px;")
    assert that(body.attribute['style']).has("background:white;")

@with_fixture
def select_by_attribute_id(context):
    "dominic selecting by attribute (id)"
    dom = DOM(context.html)

    (body, ) = dom.find("[id=firstp]")
    assert that(body).is_a(Element)
    assert that(body.attribute['id']).equals("firstp")
