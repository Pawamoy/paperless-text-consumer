# -*- coding: utf-8 -*-

from .parsers import TextDocumentParser


class ConsumerDeclaration:
    TEXT_CHARS = bytearray(
        {7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})

    @classmethod
    def handle(cls, sender, **kwargs):
        print('handling')
        return cls.test

    @classmethod
    def test(cls, doc):

        print('testing')
        splits = doc.lower().split('.')
        extension = splits[-1]

        if len(splits) <= 1:  # no extension, normal weight
            weight = 0

        elif extension == 'txt':  # txt extension, more weight
            weight = 1

        elif cls.is_text_file(doc):  # guessed with first ko, less weight
            weight = -1

        else:  # considered binary file, do not handle
            return None

        print('weight = %s ' % weight)
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
