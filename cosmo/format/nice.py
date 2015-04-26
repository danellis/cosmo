class NiceFormatter(object):
    def print(self, triples):
        previous_page_url = None
        previous_link_type = None

        for page_url, link_type, link_url in triples:
            if page_url != previous_page_url:
                print(page_url)
                previous_page_url = page_url
            if link_type != previous_link_type:
                print("  Link type '{}':".format(link_type))
                previous_link_type = link_type
            print("    {}".format(link_url))

