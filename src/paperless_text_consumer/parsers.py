# -*- coding: utf-8 -*-

import os
import subprocess

from django.conf import settings
from documents.parsers import DocumentParser, ParseError


class TextDocumentParser(DocumentParser):
    """
    This parser simply reads the file to get the text contents.

    It will handle files ending with .txt extension, or guess if
    """

    CONVERT = settings.CONVERT_BINARY

    def __init__(self, path):
        super().__init__(path)
        self._text = None

    def get_thumbnail(self):
        """
        The thumbnail of a PDF is just a 500px wide image of the first page.
        """

        if self._text is None:
            self._text = self.get_text()

        # Text needs to be escaped depending on how the graphic primitive
        # is built. More info at https://www.imagemagick.org/Usage/draw/#text
        escaped_text = self._text.replace(
            "\\", "\\\\"  # replace one backslash by two backslashes
        ).replace('"', '\\"')  # prepend a backlash to double-quotes

        x_offset, y_offset = 5, 15
        graphic_primitive = 'text {x},{y} "{text}"'.format(
            x=x_offset, y=y_offset, text=escaped_text)

        point_size = '12'

        output_path = os.path.join(self.tempdir, "convert.png")

        run_convert(
            self.CONVERT,
            '-size', '500x500',
            'xc:white',
            '-pointsize', point_size,
            '-draw', graphic_primitive,
            output_path
        )

        return output_path

    def get_text(self):
        if self._text is None:
            with open(self.document_path) as stream:
                self._text = stream.read()
        return self._text

    def get_date(self):
        return None


def run_convert(*args):

    environment = os.environ.copy()
    if settings.CONVERT_MEMORY_LIMIT:
        environment['MAGICK_MEMORY_LIMIT'] = settings.CONVERT_MEMORY_LIMIT
    if settings.CONVERT_TMPDIR:
        environment['MAGICK_TMPDIR'] = settings.CONVERT_TMPDIR

    subprocess.Popen(args, env=environment).wait()
