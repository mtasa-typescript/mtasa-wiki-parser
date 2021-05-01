from to_python.core.filter import FilterAbstract


class FilterGetUrls(FilterAbstract):
    def get_urls(self):
        """
        Gets urls, collects them into a dictionary and saves it into the context
        """
        from to_python.dump.url_list import URL_LIST

        for url in URL_LIST:
            self.context.urls[url.name] = url

    def apply(self):
        self.get_urls()
        print('Got all URLs')
