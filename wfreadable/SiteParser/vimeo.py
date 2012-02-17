import lxml.html
from readable import *
import opengraph
class Vimeo(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def run(self, html, dom_tree, url=None):
        result = {}

        desc = None
        desc_tag = dom_tree.get_element_by_id('description')
        if desc_tag is not None:
            desc = lxml.html.tostring(desc_tag)

        if desc is None:
            rb = Readable()
            tree = rb.grab_article(html)
            desc = lxml.html.tostring(tree, pretty_print=True)

        result['content'] = desc

        og = opengraph.OpenGraph()
        metas = og.parser(html)
        if og.is_valid():
            if self.verbose:
                for x,y in og.items():
                    print "%-15s => %s" % (x, y)
        
            result['videos'] = []

            if 'video' in og:
                video = {}
                h = 391
                if 'video:height' in og:
                    video['height'] = og['video:height']
                    h = video['height']
                w = 640
                if 'video:width' in og:
                    video['width'] = og['video:width']
                    w = video['width']
                video['url'] = og['video']
                result['videos'].append(video)
                embed = '<p><iframe src="{0}" frameborder="0" width="{1}" height="{2}"></iframe></p>'.format(og['video'], w, h)
                result['content'] = '{0}{1}'.format(embed, desc)
            return result
            
        else:
            return desc
