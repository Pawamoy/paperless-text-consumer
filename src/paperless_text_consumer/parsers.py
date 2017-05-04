# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
import math

from django.conf import settings
from paperless.documents.parsers import DocumentParser, ParseError


class TextDocumentParser(DocumentParser):
    """
    This parser uses Tesseract to try and get some text out of a rasterised
    image, whether it's a PDF, or other graphical format (JPEG, TIFF, etc.)
    """

    CONVERT = settings.CONVERT_BINARY
    DENSITY = settings.CONVERT_DENSITY if settings.CONVERT_DENSITY else 300
    THREADS = int(settings.OCR_THREADS) if settings.OCR_THREADS else None
    UNPAPER = settings.UNPAPER_BINARY
    DEFAULT_OCR_LANGUAGE = settings.OCR_LANGUAGE

    def get_thumbnail(self):
        """
        The thumbnail of a PDF is just a 500px wide image of the first page.
        """

        run_convert(
            self.CONVERT,
            "-scale", "500x5000",
            "-alpha", "remove",
            self.document_path, os.path.join(self.tempdir, "convert-%04d.png")
        )

        return os.path.join(self.tempdir, "convert-0000.png")

    def get_text(self):
        pass  # TODO: return file contents


def run_convert(*args):

    environment = os.environ.copy()
    if settings.CONVERT_MEMORY_LIMIT:
        environment["MAGICK_MEMORY_LIMIT"] = settings.CONVERT_MEMORY_LIMIT
    if settings.CONVERT_TMPDIR:
        environment["MAGICK_TMPDIR"] = settings.CONVERT_TMPDIR

    subprocess.Popen(args, env=environment).wait()


def strip_excess_whitespace(text):
    collapsed_spaces = re.sub(r"([^\S\r\n]+)", " ", text)
    no_leading_whitespace = re.sub(
        "([\n\r]+)([^\S\n\r]+)", '\\1', collapsed_spaces)
    no_trailing_whitespace = re.sub("([^\S\n\r]+)$", '', no_leading_whitespace)
    return no_trailing_whitespace


temp_dir = os.environ["HOME"]+"/"+".temp_iconlayers"
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)

temp_bg = temp_dir+"/"+"bg.png"; temp_txlayer = temp_dir+"/"+"tx.png"
picsize = ("x").join([str(n) for n in psize]); txsize = ("x").join([str(n-8) for n in psize])


def create_bg(bg_color='#DCDCDC', text_color='black', psize=[64, 64], n_lines=4, n_chars=9, output_file='/path/to/output/icon.png'):
    work_size = ",".join([str(_ - 1) for _ in psize])
    r = str(round(psize[0]/10))
    rounded = ','.join([r, r])
    command = 'convert -size %s xc:none -draw ' \
              '"fill %s roundrectangle 0,0,%s,%s" %s' % (
                picsize, bg_color, work_size, rounded, temp_bg)
    subprocess.call(["/bin/bash", "-c", command])


def read_text():
    with open(sys.argv[1]) as src:
        lines = [l.strip() for l in src.readlines()]
        return ("\n").join([l[:n_chars] for l in lines[:n_lines]])


def create_txlayer():
    subprocess.call(["/bin/bash", "-c", "convert -background none -fill "+text_color+\
                      " -border 4 -bordercolor none -size "+txsize+" caption:"+'"'+read_text()+'" '+temp_txlayer])


def combine_layers():
    create_txlayer(); create_bg()
    command = "convert "+temp_bg+" "+temp_txlayer+" -background None -layers merge "+output_file
    subprocess.call(["/bin/bash", "-c", command])

combine_layers
