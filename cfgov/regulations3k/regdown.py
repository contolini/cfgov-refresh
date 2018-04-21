from __future__ import unicode_literals

import re

from markdown import markdown, util
from markdown.blockprocessors import ParagraphProcessor
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

# If we're on Python 3.6+ we have SHA3 built-in, otherwise use the back-ported
# sha3 library.
try:
    from hashlib import sha3_224
except ImportError:
    from sha3 import sha3_224


class RegulationsExtension(Extension):

    config = {
        'url_resolver': [
            '',
            'Function to resolve the URL of a reference. '
            'Should return (title, url).'
        ],
        'contents_resolver': [
            '',
            'Function to resolve the contents of a reference. '
            'Should return markdown contents of the reference or an empty '
            'string.'
        ],
    }

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)

        # Add block reference preprocessor for `see(label)` syntax
        md.preprocessors.add(
            'blockreference',
            BlockReferencePreprocessor(
                contents_resolver=self.getConfig('contents_resolver')
            ),
            '>reference'
        )

        # Replace the default paragraph processor with one that handles
        # `{label}` syntax and gives default hash-based ids to paragraphs
        md.parser.blockprocessors['paragraph'] = \
            LabeledParagraphProcessor(md.parser)
        del md.parser.blockprocessors['olist']


class LabeledParagraphProcessor(ParagraphProcessor):
    """ Process paragraph blocks, including those with labels.
    This processor entirely replaces the standard ParagraphProcessor in
    order to ensure that all paragraphs are labeled in some way. """

    RE = re.compile(r'(?:^){(?P<label>[\w\-]+)}(?:\s?)(?P<text>.*)(?:\n|$)')

    def test(self, parent, block):
        # return self.RE.search(block)
        return True

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = self.RE.search(block)

        if match:
            # If there's a match, then this is a labeled paragraph. We'll add
            # the paragraph tag, label id, and initial text, then process the
            # rest of the blocks normally.
            label, text = match.group('label'), match.group('text')
            p = util.etree.SubElement(parent, 'p')
            p.set('id', label)
            level = label.count('-')
            class_name = 'level-{}'.format(level)
            p.set('class', class_name)
            p.text = text.lstrip()

        elif block.strip():
            if self.parser.state.isstate('list'):
                # Pass off to the ParagraphProcessor for lists
                super(ParagraphProcessor, self).run(parent, blocks)
            else:
                # Generate a label that is a hash of the block contents. This
                # way it won't change unless the rest of this block changes.
                text = block.lstrip()
                label = sha3_224(text.encode('utf-8')).hexdigest()
                p = util.etree.SubElement(parent, 'p')
                p.set('id', label)
                p.text = text


class BlockReferencePreprocessor(Preprocessor):
    """ Process `see(label)` as an blockquoted reference """

    RE = re.compile(r'(?:^)see\((?P<label>[\w-]+)\)(?:\n|$)')

    def __init__(self, contents_resolver=None):
        super(BlockReferencePreprocessor, self).__init__()
        self.contents_resolver = contents_resolver

    def run(self, lines):
        new_lines = []
        while lines:
            line = lines.pop(0)
            match = self.RE.match(line)
            if match:
                if self.contents_resolver is '':
                    new_lines.append('')
                    continue

                label = match.group('label')
                contents = self.contents_resolver(label)
                quoted_contents = ''.join(
                    ['> ' + l for l in contents.splitlines(True)]
                )
                new_lines.append(quoted_contents)
            else:
                new_lines.append(line)

        return new_lines


def makeExtension(*args, **kwargs):
    return RegulationsExtension(*args, **kwargs)


def regdown(text, url_resolver=None, contents_resolver=None, **kwargs):
    """ Regdown convenience function
    Takes text and parses it with the RegulationsExtention configured with
    the given reference resolver functions. """
    return markdown(
        text,
        extensions=[
            RegulationsExtension(
                url_resolver=url_resolver or '',
                contents_resolver=contents_resolver or '',
            )
        ],
        **kwargs
    )


def extract_labeled_paragraph(label, text):
    """ Extract all the Regdown between the given label and the next.
    This utility function extracts all text between a labeled paragraph
    (with leading {label}) and the next labeled paragraph. """
    para_lines = []

    for line in text.splitlines(True):
        match = LabeledParagraphProcessor.RE.search(line)
        if match:
            # It's the correct label
            if match.group('label') == label:
                para_lines.append(line)

            # We've already found a label, and this is another one
            elif len(para_lines) > 0:
                break

        # We've found a label and haven't found the next
        elif len(para_lines) > 0:
            para_lines.append(line)

    return ''.join(para_lines)
