# -*- coding: utf-8 -*-

from .parsers import TextDocumentParser


class ConsumerDeclaration:
    TEXT_CHARS = bytearray(
        {7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})

    @classmethod
    def handle(cls, sender, **kwargs):
        return cls.test

    @classmethod
    def test(cls, doc):

        # FIXME: this algorithm can surely be improved.
        # Also the weight should be balanced with other consumers'
        # and the defaults paperless consumers' weights.
        splits = doc.lower().split('.')
        if len(splits) > 1:
            extension = splits[-1]
            if extension == 'txt':
                weight = 10  # txt extension, high weight
            elif cls.is_text_file(doc):
                weight = 0  # unknown extension but text file, low weight
            else:
                return None
        elif cls.is_text_file(doc):
            weight = 5  # no extension and text file, medium weight
        else:  # considered binary file, do not handle
            return None

        return {
            'parser': TextDocumentParser,
            'weight': weight
        }

    @classmethod
    def is_text_file(cls, filename):
        # https://stackoverflow.com/questions/898669/
        with open(filename, 'rb') as stream:
            first_ko = stream.read(1024)
        return not bool(first_ko.translate(None, cls.TEXT_CHARS))
