# -*- coding: UTF-8 -*-  
# ȫ�������б�http://dll.uuwise.com/index.php?n=ApiDoc.AllFunc
# ����QQ:87280085

from ctypes import *
import sys
import os
import hashlib
import httplib
import urllib
import string
import zlib
import binascii
import random

reload(sys)						#���룬��Ū�Ļ�����������
sys.setdefaultencoding('utf8')	#���룬��Ū�Ļ�����������



#�õ��ļ���MD5ֵ����
def getFileMd5(strFile):  
    file = None;  
    bRet = False;  
    strMd5 = "";  
    try:  
        file = open(strFile, "rb");  
        md5 = hashlib.md5();  
        strRead = "";  
          
        while True:  
            strRead = file.read(8096);  
            if not strRead:  
                break;  
            md5.update(strRead);  
        #read file finish  
        bRet = True;  
        strMd5 = md5.hexdigest();  
    except:  
        bRet = False;  
    finally:  
        if file:  
            file.close()  
  
    return [bRet, strMd5]; 

#��ȡ�ļ�CRC32��
def getFileCRC(filename):
    f = None;  
    bRet = False;
    crc = 0;
    blocksize = 1024 * 64
    try:
                f = open(filename, "rb")
                str = f.read(blocksize)
                while len(str) != 0:
                        crc = binascii.crc32(str,crc) & 0xffffffff
                        str = f.read(blocksize)
                f.close()
                bRet = True; 
    except:
        print "compute file crc failed!"+filename
        return 0
    return [bRet, '%x' % crc];

#�Է��������ص�ʶ��������У��
def checkResult(dllResult, s_id, softVerifyKey, codeid):
    bRet = False;
    #���������ص��Ǵ������
    print(dllResult);
    print(len(dllResult));
    if(len(dllResult) < 0):
        return [bRet, dllResult];
    #��ȡ��У��ֵ��ʶ����
    items=dllResult.split('_')
    verify=items[0]
    code=items[1]

    localMd5=hashlib.md5('%d%s%d%s'%(s_id, softVerifyKey, codeid, (code.upper()))).hexdigest().upper()
    if(verify == localMd5):
        bRet = True;
        return [bRet, code];
    return [bRet, "У����ʧ��"]
def GetChecksumCode(filename,soft_id,soft_key,soft_verify_key,username,password):
	UUDLL=os.path.join(os.path.dirname(__file__), 'UUWiseHelper.dll')
	pic_file_path = os.path.join(os.path.dirname(__file__), '', filename)
	s_id  = soft_id                                # ���ID
	s_key = soft_key  # ���Key ��ȡ��ʽ��http://dll.uuwise.com/index.php?n=ApiDoc.GetSoftIDandKEY
	UU = windll.LoadLibrary(UUDLL)
	setSoftInfo = UU.uu_setSoftInfoW
	login = UU.uu_loginW
	recognizeByCodeTypeAndPath = UU.uu_recognizeByCodeTypeAndPathW
	getResult = UU.uu_getResultW
	uploadFile = UU.uu_UploadFileW
	getScore = UU.uu_getScoreW
	checkAPi=UU.uu_CheckApiSignW	#api�ļ�У�麯�������ú󷵻أ�MD5�����ID+��дDLLУ��KEY+��д���ֵ����+����API�ļ���MD5ֵ+��д������API�ļ���CRC32ֵ��
	dllMd5=getFileMd5(UUDLL);	#api�ļ���MD5ֵ
	dllCRC32=getFileCRC(UUDLL);	#API�ļ���CRC32ֵ
	randChar=hashlib.md5(random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')).hexdigest();	#����ַ����������÷������Ľ�����
	softVerifyKey=soft_verify_key;	#�ڿ����ߺ�̨����б��ڻ�ȡ������й¶��KEY��ͼ����http://dll.uuwise.com/index.php?n=ApiDoc.GetSoftIDandKEY


	checkStatus=hashlib.md5('%d%s%s%s%s'%(s_id,(softVerifyKey.upper()),(randChar.upper()),(dllMd5[1].upper()),(dllCRC32[1].upper()))).hexdigest();		#��������������ֵ���ֵ��Ӧһ�����ʾ�ɹ�

#debugPoint = raw_input("Pleas input you user name and press enter:")
	serverStatus=c_wchar_p("");	#�������������Ľ��,serverStatus��checkStatusֵһ���Ļ�����OK
	checkAPi(c_int(s_id), c_wchar_p(s_key.upper()),c_wchar_p(randChar.upper()),c_wchar_p(dllMd5[1].upper()),c_wchar_p(dllCRC32[1].upper()),serverStatus);  #���ü�麯��,����Ҫ����һ�μ��ɣ�����Ҫÿ���ϴ�ͼƬ������һ��


#���API�ļ��Ƿ��޸�


	if not (checkStatus == serverStatus.value):
		print("sorry, api file is modified")	#���API�ļ����޸ģ�����ֹ����
		return ''
    

	user_i = username
	passwd_i = password

	user = c_wchar_p(user_i)  # ��Ȩ�û���
	passwd = c_wchar_p(passwd_i)  # ��Ȩ����


#setSoftInfo(c_int(s_id), c_wchar_p(s_key))		#�������ID��KEY������Ҫ����һ�μ��ɣ�ʹ����checkAPi�����Ļ����Ͳ���ʹ�ô˺�����
	ret = login(user, passwd)		                #�û���¼������Ҫ����һ�μ��ɣ�����Ҫÿ���ϴ�ͼƬ������һ�Σ�����������⣬���統�ɽű�ִ�еĻ�

	if ret > 0:
		print('login ok, user_id:%d' % ret)                 #��¼�ɹ������û�ID
	else:
		print('login error,errorCode:%d' %ret )
		return ''

	ret = getScore(user, passwd)                            #��ȡ�û���ǰʣ�����
	print('The Score of User : %s  is :%d' % (user.value, ret))

	result=c_wchar_p("                                              ")	#�����ڴ�ռ䣬�����ڴ�й¶
	code_id = recognizeByCodeTypeAndPath(c_wchar_p(pic_file_path),c_int(2002),result)
	if code_id <= 0:
		print('get result error ,ErrorCode: %d' % code_id)
	else:
		checkedRes=checkResult(result.value, s_id, softVerifyKey, code_id);
		print("the resultID is :%d result is %s" % (code_id,checkedRes[1]))  #ʶ����Ϊ���ַ����� c_wchar_p,���õ�ʱ��ע��ת��һ��
		return checkedRes
	return ''
