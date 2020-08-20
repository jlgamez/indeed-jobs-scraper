from sys import platform


def get_driver_name():
    if platform in ['linux', 'linux2']:
        chrome_driver = 'chromedriver_linux'
    elif platform == 'darwin':
        chrome_driver = 'chromedriver_macOS'
    elif platform == 'win32':
        chrome_driver = 'chromedriver_windows.exe'
    else:
        print('\nIt seems your current OS is doesn\'t support chromedriver. You need to run the code on Ubuntu, MacOs, '
              'or Windows')
        exit()

    return chrome_driver
