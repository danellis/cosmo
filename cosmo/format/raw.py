class RawFormatter(object):
    def print(self, triples):
        for page_url, link_type, link_url in triples:
            print("{} {} {}".format(page_url, link_type, link_url))

