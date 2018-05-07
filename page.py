class Page:
    def __init__(self):
        self._cur_page = 1
        self._page_size = 50
        self._total_page = 0

    def initialized(self):
        self._cur_page = 1
        self._page_size = 50
        self._total_page = 0

    def has_more_page(self):
        return self._cur_page < self._total_page

    def get_cur_page(self):
        return self._cur_page

    def get_total_page(self):
        return self._total_page

    def set_page_size(self, size):
        self._page_size = size

    def set_total_page(self, total):
        self._total_page = total

    def next_page(self):
        self._cur_page += 1

    def prev_page(self):
        if self._cur_page > 0:
            self._cur_page -= 1
