from readable import *
import lxml.html
import os 
import urlparse
import re

class Medium(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def run(self, html, dom_tree=None, url=None):
        result = {}

        # this is unique in slashdot 
        bodies = dom_tree.find_class("post-field body")
        tree = None
        if len(bodies) > 0:
            tree = bodies[0]
        else:
            rb = Readable()
            tree = rb.grab_article(html)

        if tree is not None:
            opts = dict(scripts=True, javascript=True, comments=True,
                        style=True, links=True, meta=False, page_structure=False,
                        processing_instructions=True, embedded=False, frames=False,
                        forms=False, annoying_tags=False, safe_attrs_only=False)
            cleaner = lxml.html.clean.Cleaner(**opts)
            cleaner(tree)
            for tag in tree.xpath('//*[@class]'):
                tag.attrib.pop('class')

            result['content'] = lxml.html.tostring(tree, pretty_print=True)

            tree = lxml.html.fromstring(result['content'])
            result['images'] = []
            imgs = tree.xpath('//img | //IMG')
            for img in imgs:
                src = img.get('src')
                if src is not None:
                    result['images'].append({'url': src})

            return result
        else:
            return None
