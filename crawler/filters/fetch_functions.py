from crawler.core.filter import FilterAbstract
from crawler.core.types import FunctionUrl


class FilterFetchFunctions(FilterAbstract):
    """
    Fetches functions defined in the URL List
    """

    def fetch_function(self, url: FunctionUrl) -> str:
        """
        Fetches page from wiki
        :param url: Data about the function
        :return: Fetched data
        """
        print('Fetch')

    def save_file(self, url: FunctionUrl, result: str):
        """
        Saves fetched data into a file
        :param url: Data about the function
        :param result: Fetched data
        """
        pass

    def apply(self):
        for url in self.context.url_list:
            result = self.fetch_function(url)
            self.save_file(url, result)
