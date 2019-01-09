#coding:utf-8
from aliyunsdkcore import client
from aliyunsdkkms.request.v20160120 import GenerateDataKeyRequest

import ConfigParser
import json
from Crypto.Cipher import AES #pip install pycrypto
from Crypto import Random
import base64

def aes256pad(s):
	return s + (32 - len(s) % 32) * chr(32 - len(s) % 32)

if __name__=='__main__':
	#AccessKey情報を定義
	accesskeyid = "<Your AccessKeyId>"
	accesssecret = "<Your AccessKeySecret>"
	#Clientを初期化
	clt = client.AcsClient(accesskeyid,accesssecret,"ap-northeast-1")
	#KMS OpenAPI GenerateDataKeyを呼び出す
	genrequest = GenerateDataKeyRequest.GenerateDataKeyRequest()
	#keiidはKMSコンソールで作成したCMKのID
	keyid = '<Your keyid> '
	genrequest.set_KeyId(keyid)
	genrequest.set_KeySpec("AES_256")
	#json形式を指定する
	genrequest.set_accept_format("json")
	#KMSはHTTPSのRequestのみサポートする
	genrequest.set_protocol_type("https")
	genresp = clt.do_action_with_exception(genrequest)
	#KMSから平文キーと暗号キー入手するためのキーワードを取得する
	datakeydict = json.loads(genresp)
	#KMSからのキーワードを利用して、平文キーを入手する
	datakey = base64.b64decode(datakeydict["Plaintext"])
	#KMSからのキーワードを利用して、暗号キーを入手する
	cipherdatakey = datakeydict["CiphertextBlob"]
	#平文キーを使ってファイルの暗号化を行う。暗号キーと暗号ファイルのみ保存する。
	with open('cipherkey','w') as key:
		key.write(cipherdatakey)
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(datakey,AES.MODE_CBC, iv)
	with open('input.txt','r') as fp:
		filedata = aes256pad(fp.read())
		cipherfile = base64.b64encode(iv + cipher.encrypt(filedata))
		with open('cipherfile.txt','w') as output:
			output.write(cipherfile)