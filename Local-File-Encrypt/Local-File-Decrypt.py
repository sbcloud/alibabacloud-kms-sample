#coding:utf-8
from aliyunsdkcore import client
from aliyunsdkkms.request.v20160120 import DecryptRequest

import ConfigParser
import json
from Crypto.Cipher import AES
import base64

def aes256pad(s):
	return s[:-ord(s[len(s)-1:])]

if __name__=='__main__':
	#AccessKey情報を定義
	accesskeyid = "<Your AccessKeyId>"
	accesssecret = "<Your AccessKeySecret>"
	#Clientを初期化
	clt = client.AcsClient(accesskeyid,accesssecret,"ap-northeast-1")
	#暗号ファイルを読み取る
	with open('cipherkey','r') as fp:
		cipherdatakey = fp.read()
		#暗号キーを利用して、KMS OpenAPI Decryptを呼び出す
		decrequest = DecryptRequest.DecryptRequest()
		decrequest.set_CiphertextBlob(cipherdatakey)
		#json形式を指定する
		genrequest.set_accept_format("json")
		#KMSはHTTPSのRequestのみサポートする
		decrequest.set_protocol_type("https")
		decresp = clt.do_action_with_exception(decrequest)
		#KMSから平文キーを入手するためのキーワードを取得する
		plaintext = json.loads(decresp)
		#KMSからのキーワードを利用して平文キーを入手する
		datakey = base64.b64decode(plaintext["Plaintext"])
		#平文キーを利用して暗号ファイルを復号化して、内容を表示する
		with open('cipherfile.txt','r') as cipher:
			cipherfile = base64.b64decode(cipher.read())
			iv = cipherfile[:AES.block_size]
			aes = AES.new(datakey, AES.MODE_CBC, iv)
			print aes.decrypt(cipherfile[AES.block_size:]).decode('utf-8')