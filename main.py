#!/usr/bin/python
# -*- coding: UTF-8 -*-

from config import Config  # get test info
from login import login    # login test

# test case
all_test = {
  'load_page_test': login.load_page_test,
  'account_test': login.account_test,
  'logo_test': login.logo_test,
  'alert_message_test': login.alert_test,
}


if __name__ == '__main__':
    # load config.ini
    config = Config('Default')

    all_test['load_page_test'](config.hostname, config.timeout, config.page_width, config.page_high)
    all_test['account_test'](config.hostname, config.timeout, config.page_width, config.page_high)
    all_test['logo_test'](config.hostname, config.timeout, config.page_width, config.page_high)
    all_test['alert_message_test'](config.hostname, config.timeout, config.page_width, config.page_high)

    exit(0)
