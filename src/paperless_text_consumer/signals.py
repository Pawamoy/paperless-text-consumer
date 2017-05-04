# -*- coding: utf-8 -*-

import string

from .parsers import TextDocumentParser


class ConsumerDeclaration(object):
    @classmethod
    def handle(cls, sender, **kwargs):
        return cls.test

    @classmethod
    def test(cls, doc):
        if cls.is_text_file(doc.lower()):
            return {"parser": TextDocumentParser, "weight": 0}
        return None

    @classmethod
    def is_text_file(cls, filename):
        # https://stackoverflow.com/questions/1446549/
        s = open(filename).read(512)
        text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
        _null_trans = string.maketrans("", "")
        if not s:
            # Empty files are considered text
            return True
        if "\0" in s:
            # Files with null bytes are likely binary
            return False
        # Get the non-text characters (maps a character to itself then
        # use the 'remove' option to get rid of the text characters.)
        t = s.translate(_null_trans, text_characters)
        # If more than 30% non-text characters, then
        # this is considered a binary file
        if float(len(t)) / float(len(s)) > 0.30:
            return False
        return True
