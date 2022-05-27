import setup

import os


if __name__ == '__main__':
    code = input(
        f'Are you sure of deleting {setup.COMMON_FILE}'
        ' and {setup.AUTH_FILE} (yes/no fingerpring)?: '
    )
    if code == 'yes':
        try:
            os.remove(setup.COMMON_FILE)
            os.remove(setup.AUTH_FILE)
        except:
            pass
        setup.update_git_ignore(setup.remove_from_gitignore())
        print('Files removed')
        exit(0)
    print('Uninstall cancelled')
