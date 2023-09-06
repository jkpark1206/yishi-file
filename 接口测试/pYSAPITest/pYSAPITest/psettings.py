#fwname = r"D:\test data\FW Samples\wr940nv4_us_3_16_9_up_boot(160617).bin"
fwname = r"E:\test data\FW Samples\中汽院\example1.bin"
logfilename = r'D:\SourceCode\pcode\pYSAPITest\log.txt'
reportfilename = r'D:\SourceCode\pcode\pYSAPITest\report.csv'
fwcompfile1 = r"D:\Share\大通\FW 对比的sample\fw_c1.elf"
fwcompfile2 = r"D:\Share\大通\FW 对比的sample\fw_c2.elf"
fwcompuid1 = ""
fwcompuid2 = ""
compareid = ""
timeout = 300
#url = 'http://192.168.50.113:8003'
#url = 'http://127.0.0.1:8003'
#url = 'http://192.168.50.57:8003'
url = 'http://jump.cosec.tech:58012/'
#user = 'anban'
#password = '1111'
user = 'qpb'
password = '123456'
token = ''
header = {
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    "Content-Length": '0',
    'Authorization': ''
}
