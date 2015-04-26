class DotFormatter(object):
    def print(self, triples):
        print('digraph {')
        for page_url, link_type, link_url in triples:
            print('  "{}" -> "{}" [type={}]'.format(page_url, link_url, link_type))
        print('}')
