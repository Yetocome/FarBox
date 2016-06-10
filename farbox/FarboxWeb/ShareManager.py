import random
from .models import ShareInfo
ShareKeyLen = 10


def generate_share_key():
    while True:
        charset = '1234567890abcdefghijklmnopqrstuvwxyz'
        length = len(charset)
        key = ''
        for i in range(ShareKeyLen):
            key += charset[random.randint(0, length - 1)]
        try:
            ShareInfo.objects.get(pk=key)
        except:
            return key


def generate_share_info(path_id):
    return ShareInfo(share_key=generate_share_key(), path_id=path_id)


if __name__ == '__main__':
    print(generate_share_key())