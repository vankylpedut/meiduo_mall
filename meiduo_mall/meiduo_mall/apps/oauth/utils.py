from django.conf import settings
from itsdangerous import BadData
from itsdangerous import TimedJSONWebSignatureSerializer


def generate_encrypted_openid(openid):
    '''生成加密的openid'''
    serializer = TimedJSONWebSignatureSerializer(
        settings.SECRET_KEY, expires_in=60 * 10
    )  # 有效期为10分钟
    return serializer.dumps({'openid': openid}).decode()

def check_encrypted_openid(encrypted_openid):
    '''校验openid是否过期，是否被篡改'''
    serializer = TimedJSONWebSignatureSerializer(
        settings.SECRET_KEY,expires_in=60*10
    )# 有效期为10分钟

    try:
        data = serializer.loads(encrypted_openid)
    except BadData:
        return None
    else:
        return data.get('openid')
