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

@with_fixture("divs.html")
def text_return_the_text_within_element(context):
    "Element().text() returns the text content"
    dom = DOM(context.html)

    p = dom.find("#the-only-paragraph").first()

    assert that(p.text()).equals("the only one in th whole damn thing!?")

@with_fixture("divs.html")
def text_modifies_the_text_within_element(context):
    "Element().text('new text') modifies the text content"

    dom = DOM(
        '<div class="drinks">\n'
        '  <h1 id="header">I like piña colada!</h1>\n'
        '</div>'
    )

    h1 = dom.find("div.drinks h1").first()
    assert that(h1.text()).equals("I like piña colada!")

    h1.text('Do you like vodka?')
    assert that(h1.text()).equals("Do you like vodka?")
    assert that(h1.html()).equals('<h1 id="header">Do you like vodka?</h1>')

    assert that(dom.html()).equals(
        '<div class="drinks">\n'
        '  <h1 id="header">Do you like vodka?</h1>\n'
        '</div>'
    )

@with_fixture("divs.html")
def html_return_the_html_string(context):
    "Element().html() returns the html string"
    dom = DOM(context.html)

    p = dom.find("#the-only-paragraph").first()

    assert that(p.html()).equals(
        '<p id="the-only-paragraph">the only one in th whole damn thing!?</p>'
    )

@with_fixture("divs.html")
def html_modifies_the_html_within_element(conhtml):
    "Element().html('new html') modifies the html string"

    dom = DOM(
        '<div class="drinks">\n'
        '  <h1 id="header">I like marguerita!</h1>\n'
        '</div>'
    )

    h1 = dom.find("div.drinks h1").first()
    assert that(h1.html()).equals('<h1 id="header">I like marguerita!</h1>')

    h1.html('<strong>Yeah, whiskey is much better!</strong>')
    assert that(h1.html()).equals('<strong>Yeah, whiskey is much better!</strong>')
    assert that(h1.text()).equals('Yeah, whiskey is much better!')

    assert that(dom.html()).equals(
        '<div class="drinks">\n'
        '  <strong>Yeah, whiskey is much better!</strong>\n'
        '</div>'
    )

@with_fixture("divs.html")
def first_returns_the_first(context):
    "selecting all childs of some element"
    dom = DOM(context.html)

    elements = dom.find("#objects li")

    p = elements.first()
    assert that(p).is_a(Element)
    assert that(p.tag).equals("li")
    assert that(p.attribute['id']).equals("ball")
    assert that(p.text()).equals("to kick")

@with_fixture("divs.html")
def last_returns_the_last(context):
    "selecting all childs of some element"
    dom = DOM(context.html)

    elements = dom.find("#objects li")

    p = elements.last()
    assert that(p).is_a(Element)
    assert that(p.tag).equals("li")
    assert that(p.attribute['id']).equals("puppet")
    assert that(p.text()).equals("to care with")
