from to_python.core.filter import FilterAbstract


class FilterParseFunctionSignature(FilterAbstract):
    """
    Parses function signature
    """

    def parse_signature(self, code: str):
        """
        Parses given code
        """
        pass

    def pick_signature(self, raw_data: str) -> str:
        """
        Picks out function signature code from an entire data
        """
        pass

    def apply(self):
        for f_name in self.context.side_data:
            for side, data in self.context.side_data[f_name]:
                pass
