#!/usr/bin/env python3

import sys, re, pikepdf

from decimal import *

# instructions are documented in PDF reference manual:
# https://www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/pdf_reference_archives/PDFReference.pdf

# pikepdf manual is also helpful:
# https://pikepdf.readthedocs.io/en/latest/topics/content_streams.html

# in PDF points, 1 = 1/72" or about 0.35 mm
NEW_LINE_WEIGHT = Decimal(0.001)

def convert_line_weights_in_page(page):
    instructions = list(pikepdf.parse_content_stream(page))

    for i, [operands, operator] in enumerate(instructions):
        if str(operator) == 'w' and operands[0] > 0:
            instructions[i] = ([NEW_LINE_WEIGHT], 'w')

    new_content_stream = pikepdf.unparse_content_stream(instructions)
    page.Contents = pdf.make_stream(new_content_stream)

if __name__ == '__main__':
    with pikepdf.open(sys.argv[1]) as pdf:
        for page in pdf.pages:
            convert_line_weights_in_page(page)
        
        pdf.save(sys.argv[2])