# -*- coding: utf-8 -*-
"""
Created on Monday Feb 20 2017

@author: jclarke
"""

from bs4 import BeautifulSoup
import os
import sys

def strip_code(bs_tree):
    removeds = [n.extract() for n in bs_tree.find_all(class_ = 'input')]
    removeds = [n.extract() for n in bs_tree.find_all(class_ = 'output_prompt')]
    removeds = [n.extract() for n in bs_tree.find_all(class_ = 'jp-Cell-inputWrapper')]
    removeds = [n.extract() for n in bs_tree.find_all(class_ = 'jp-OutputPrompt')]

if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(usage="%prog FILENAME1 FILENAME2 ...",
                          description="""\
Strip input code cells and input prompts from a Jupyter HTML file so that it's suitable for sharing""")

    parser.add_option('-o', '--output_file', default=[],
                         help='Write output to the given file (default is to write to "cleaned FILENAME").',
                         dest='output_file', action='append')

    parser.add_option('-i', '--insert_css', default=[],
                         help='Insert custom CSS into the file.',
                         dest='insert_css', action='append')

    options, args = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)

    if len(options.output_file) > 0 and len(options.output_file) != len(args):
        print('ERROR: The number of input files given does not match the number of output files given.', file=sys.stderr)
        sys.exit(1)

    import codecs
    for i, filename in enumerate(args):
        if i >= len(options.output_file):
            splitpath = os.path.split(filename)
            path = list(splitpath[:-1])
            fname = splitpath[-1]
            outfile = os.path.join(*(path + ['cleaned ' + fname]))
        else:
            outfile = options.output_file[i]

        doctree = BeautifulSoup(codecs.open(filename, encoding='utf-8'), 'lxml')

        strip_code(doctree)

        if len(options.insert_css):
            for cssfile in options.insert_css:
                f = open(cssfile, 'r')
                styletag = doctree.new_tag("style")
                styletag.append(f.read())
                doctree.body.insert(-1, styletag)
                f.close()

        f = codecs.open(outfile, encoding='utf-8', mode='w')
        f.write(str(doctree))
        f.close()
