from crawler.filters.fetch_function_pages import WikiPageFetcher, \
    FilterFetchFunctions


class FilterFetchEventsError(RuntimeError):
    pass


class FilterFetchEvents(FilterFetchFunctions):
    """
    Fetches events defined in the URL List
    """

    def apply(self):
        print('Events fetch began')

        url_dict = self.generate_url_list_dict(
            url_list=self.context.event_url_list,
            blacklist=self.context.event_blacklist,
            start_from=self.context.event_fetch_start_from, )
        keys = list(url_dict.keys())

        counter = 0
        for name, content in WikiPageFetcher(
                keys,
                self.context.host_url,
                self.context.fetch_batch_size
        ).fetch():
            if name not in url_dict:
                raise FilterFetchEventsError(
                    f'Not found key {name} '
                    f'in url_dict. Have you normalized the URL names?'
                )

            url_object = url_dict[name]
            counter += 1

            print(
                f'Fetched [{counter}/{len(url_dict)}] '
                f'"{url_object.name}", '
                f'{url_object.type.name}'
            )

            self.context.event_fetched.append((url_dict[name], content))
