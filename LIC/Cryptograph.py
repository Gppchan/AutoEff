from Crypto.Cipher import AES


class Cryptograph(object):

    def __init__(self, key: str):
        self.__key: bytes = self.__to_utf8_bytes(key)
        self.__cryptor = AES.new(self.__key, AES.MODE_ECB)
        self.__placeholder = "\0"

    def encrypt(self, text: str) -> str:
        """加密函数"""

        plaintext: bytes = self.__to_utf8_bytes(text)
        plaintext = self.__enlarge(plaintext)
        ciphertext = self.__cryptor.encrypt(plaintext)
        ciphertext = ciphertext.hex()
        return ciphertext

    def decrypt(self, text: str) -> str:
        """解密函数"""

        ciphertext: bytes = bytes.fromhex(text)
        plaintext = self.__cryptor.decrypt(ciphertext)
        plaintext = self.__to_utf8_str(plaintext)
        plaintext = self.__shrink(plaintext)
        return plaintext

    def __enlarge(self, text: bytes) -> bytes:
        """
        密钥key长度必须为16(AES-128), 24(AES-192)或者32(AES-256)Bytes 长度
        目前AES-128足够目前使用
        如果text不足16位，就用空字符补足为16位
        如果text大于16位但不是16的倍数，那就补足为16的倍数
        """

        target_length: int = 16
        current_length: int = len(text)
        if current_length < target_length:
            add = target_length - current_length
        elif current_length > target_length:
            add = target_length - (current_length % target_length)
        else:
            add = 0
        return text + self.__to_utf8_bytes(self.__placeholder * add)

    def __shrink(self, text: str) -> str:
        """
        信息在加密时可能被扩充，此处去掉扩充的占位符
        """

        return text.rstrip(self.__placeholder)

    @staticmethod
    def __to_utf8_bytes(text: str) -> bytes:
        return text.encode('utf-8')

    @staticmethod
    def __to_utf8_str(text: bytes) -> str:
        return text.decode('utf-8')
