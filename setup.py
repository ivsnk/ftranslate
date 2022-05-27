import os


AUTH_FILE = '.auth'
COMMON_FILE = 'common.py'
GIT_IGNORE = '.gitignore'
GIT_IGNORE_HIDDEN_FILES = '# Hidden files for application'


def check_token(token):
    return True

def remove_from_gitignore():
    git_ignore_content = None
    with open(GIT_IGNORE, 'r') as f:
        a = [x.strip() for x in f.readlines()]
        git_ignore_content = '\n'.join(a)
        if any(map(lambda x: x == GIT_IGNORE_HIDDEN_FILES, a)):
            git_ignore_content = '\n'.join(a[:a.index(GIT_IGNORE_HIDDEN_FILES)-1])
    return git_ignore_content

def update_git_ignore(content):
    with open(GIT_IGNORE, 'w') as f:
        print(content, file=f)


if __name__ == '__main__':
    project_dir = os.getcwd()
    auth_token = input('Input auth token (yandex translate): ').strip()
    if not auth_token or not check_token(auth_token):
        print("Invalid auth token")
        exit(1)

    token_file = f'{project_dir}/{AUTH_FILE}'
    with open(token_file, 'w') as f:
        print(auth_token, file=f, end='')
    
    with open(COMMON_FILE, 'w') as f:
        print(f'AUTH_FILE = \'{token_file}\'', file=f)

    update_git_ignore(f'{remove_from_gitignore()}\n\n{GIT_IGNORE_HIDDEN_FILES}\n{COMMON_FILE}\n{AUTH_FILE}')