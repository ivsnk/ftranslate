import os


AUTH_FILE = '.auth'
COMMON_FILE = 'common.py'
GIT_IGNORE = '.gitignore'
GIT_IGNORE_HIDDEN_FILES = '# Hidden files for application'
REQUIREMENTS = 'requirements.txt'
YA_TRANSLATE_HOST = 'https://translate.api.cloud.yandex.net'
YA_TRANSLATE_PATH = 'translate/v2/translate'
YA_GET_LANGS_PATH = '/translate/v2/languages'


def check_token(iam_token, folder_id):
    import requests

    resp = requests.post(
        f'{YA_TRANSLATE_HOST}{YA_GET_LANGS_PATH}',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {iam_token}',
        },
        json={
            'folderId': folder_id
        }
    )

    if resp.status_code != 200:
        print(f'**** token check response code: {resp.status_code}')
        print(resp.content.decode('utf-8'))
    return resp.status_code == 200


def remove_from_gitignore():
    git_ignore_content = None
    with open(GIT_IGNORE, 'r') as f:
        a = [x.strip() for x in f.readlines()]
        git_ignore_content = '\n'.join(a)
        if any(map(lambda x: x == GIT_IGNORE_HIDDEN_FILES, a)):
            git_ignore_content = '\n'.join(
                a[:a.index(GIT_IGNORE_HIDDEN_FILES)-1]
            )
    return git_ignore_content


def update_git_ignore(content):
    with open(GIT_IGNORE, 'w') as f:
        print(content, file=f)


def generate_common_file(token_file):
    common_values = [
        ('AUTH_FILE', token_file),
        ('YA_TRANSLATE_HOST', YA_TRANSLATE_HOST),
        ('YA_TRANSLATE_PATH', YA_TRANSLATE_PATH),
        ('YA_GET_LANGS_PATH', YA_GET_LANGS_PATH)
    ]
    with open(COMMON_FILE, 'w') as f:
        print(
            '\n'.join(map(lambda x: f'{x[0]} = \'{x[1]}\'', common_values)),
            file=f
        )
        print(
            '\n\ndef get_auth_params():\n'
            '    params = open(AUTH_FILE, \'r\').readlines()\n'
            '    return {\'iam_token\': params[0], \'folder_id\': params[1]}',
            file=f
        )


def update_auth_token_file(token_file, iam_auth_token, folder_id):
    if os.path.exists(token_file):
        code = input(
            'This change will rewrite file with auth token,'
            'are you sure of doing this? (yes/no fingerprint): '
        )
        if code != 'yes':
            print('Auth token was not updated')
            return
    with open(token_file, 'w') as f:
        print(iam_auth_token, folder_id, file=f, sep='\n', end='')


if __name__ == '__main__':
    try:
        os.system(f'pip install -r {REQUIREMENTS}')
    except:
        pass
    project_dir = os.getcwd()
    iam_auth_token = input('Input auth token (yandex iam token): ').strip()
    folder_id = input('Input folder_id (yandex cloud): ').strip()
    if not check_token(iam_auth_token, folder_id):
        print('Invalid auth tokens')
        exit(1)

    token_file = f'{project_dir}/{AUTH_FILE}'
    update_auth_token_file(token_file, iam_auth_token, folder_id)

    generate_common_file(token_file)

    update_git_ignore(
        f'{remove_from_gitignore()}\n\n{GIT_IGNORE_HIDDEN_FILES}'
        f'\n{COMMON_FILE}\n{AUTH_FILE}'
    )
