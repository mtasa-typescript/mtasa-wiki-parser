from to_python.core.filter import FilterAbstract


class FilterSaveData(FilterAbstract):
    """
    Saves all data into files
    """

    def apply(self):
        for f_name in self.context.parsed:
            # if raw_content.client is not None:
                pass
