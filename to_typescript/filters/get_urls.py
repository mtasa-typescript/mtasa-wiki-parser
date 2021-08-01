from to_typescript.core.filter import FilterAbstract


class FilterGetUrls(FilterAbstract):
    def get_urls(self):
        """
        Gets urls, collects them into a dictionary and saves it into the context
        """
        from to_python.dump.url_list import URL_LIST
        from to_python.dump.url_list import URL_LIST_EVENT

        for url in URL_LIST:
            self.context.urls[url.name] = url

        for url in URL_LIST_EVENT:
            self.context.urls[url.name] = url

    def apply(self):
        self.get_urls()
        print(f'Got all URLs (functions and events): \u001b[34m{len(self.context.urls)}\u001b[0m')
