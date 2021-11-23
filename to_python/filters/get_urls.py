from to_python.core.filter import FilterAbstract


class FilterGetFunctionUrls(FilterAbstract):
    def __init__(self):
        super().__init__('functions')

    def get_urls(self) -> int:
        """
        Gets urls, collects them into a dictionary
        and saves it into the context
        :return: Length of the collected URL array
        """
        from crawler.dump_html import URL_LIST

        for url in URL_LIST:
            self.context_data.urls[url.name] = url

        return len(URL_LIST)

    def apply(self):
        length = self.get_urls()
        print(f'Got all function URLs: \x1b[34m{length}\x1b[0m items')


class FilterGetEventUrls(FilterAbstract):
    def __init__(self):
        super().__init__('events')

    def get_urls(self) -> int:
        """
        Gets urls, collects them into a dictionary
        and saves it into the context
        :return: Length of the collected URL array
        """
        from crawler.dump_html import EVENT_URL_LIST

        for url in EVENT_URL_LIST:
            self.context_data.urls[url.name] = url

        return len(EVENT_URL_LIST)

    def apply(self):
        length = self.get_urls()
        print(f'Got all event URLs: \x1b[34m{length}\x1b[0m items')
