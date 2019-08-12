class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.title

    def __exit__(self, *_):
        self.wait_for(self.page_has_loaded)

    @staticmethod
    def wait_for(condition_function):
        import time

        start_time = time.time()
        while time.time() < start_time + 5:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception(
            'Timeout waiting for {}'.format(condition_function.__name__)
        )

    def page_has_loaded(self):
        new_page = self.browser.title
        return new_page != self.old_page


