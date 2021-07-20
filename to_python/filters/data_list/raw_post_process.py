import re

from to_python.core.filter import FilterAbstract


class FilterRawPostProcess(FilterAbstract):
    """
    Cleans raw data (from context.raw_data)
    """

    END_CUTOFF_REGEX = re.compile(r'=+ *(See Also|Examples?) *=+', re.IGNORECASE)

    def __init__(self, context_type: str):
        """
        :param context_type: `functions` or `events`
        """
        super().__init__(context_type)

    def post_process(self, raw: str) -> str:
        regexp_result = re.search(self.END_CUTOFF_REGEX, raw)
        if regexp_result:
            raw = raw[:regexp_result.start()]  # Cutoff

        return raw

    def apply(self):
        for name in self.context_data.raw_data:
            raw = self.context_data.raw_data[name]
            self.context_data.raw_data[name] = self.post_process(raw)
