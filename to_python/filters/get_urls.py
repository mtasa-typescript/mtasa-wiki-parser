from to_python.core.filter import FilterAbstract


class FilterGetFunctionUrls(FilterAbstract):
    def __init__(self):
        super().__init__('functions')

    def get_urls(self):
        """
        Gets urls, collects them into a dictionary and saves it into the context
        :return:
        """
        from crawler.dump_html import URL_LIST

        for url in URL_LIST:
            self.context_data.urls[url.name] = url

    def apply(self):
        self.get_urls()
        print('Got all function URLs')


class FilterGetEventUrls(FilterAbstract):
    def __init__(self):
        super().__init__('events')

    def get_urls(self):
        """
        Gets urls, collects them into a dictionary and saves it into the context
        :return:
        """
        from crawler.dump_html import EVENT_URL_LIST

        for url in EVENT_URL_LIST:
            self.context_data.urls[url.name] = url

    def apply(self):
        self.get_urls()
        print('Got all event URLs')
