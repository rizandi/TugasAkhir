import paramiko
import os
import time

hostname = "10.183.249.219"
password = "raspberry"

username = "pi"
port = 22

# try:
touch = 0
# counter = 0
while(True):
    # print(counter)
    counter+=1
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    
    client.connect(hostname, port=port, username=username, password=password)
    # while(True):
    #     print(counter)
    #     counter+=1
    stdin, stdout, stderr = client.exec_command("tshark -a duration:15 -w monitoring1.pcap -T fields -E separator=, -E quote=d -e frame.number -e frame.time -e_ws.col.Source -e_ws.col.Destination -e_ws.col.Protocol -e_ws.col.info")
    exit_status = stdout.channel.recv_exit_status()
    checker_pengambilan = os.system("pscp -pw raspberry pi@10.183.249.219:/home/pi/monitoring1.pcap D:/")
    print(str(checker_pengambilan))
    while(checker_pengambilan):
        checker_pengambilan = os.system("pscp -pw raspberry pi@10.183.249.219:/home/pi/monitoring1.pcap D:/")
    stdin_cek1, stdout_cek1, stderr_cek1 = client.exec_command("python accessdate.py")
    a_cek1 = stdout_cek1.read()
    a_cek1 = str(a_cek1)
    b_cek1 = a_cek1.split(" ")
    c_cek1 = b_cek1[4]
    stdin, stdout, stderr = client.exec_command("touch -a monitoring1.pcap")
    stdin_cek2, stdout_cek2, stderr_cek2 = client.exec_command("python accessdate.py")
    a_cek2 = stdout_cek2.read()
    a_cek2 = str(a_cek2)
    b_cek2 = a_cek2.split(" ")
    c_cek2 = b_cek2[4]
    print(c_cek1, c_cek2)
    # pengambilan berhasil
    print("pengambilan berhasil") 
    if(c_cek1 != c_cek2):
        print(touch)
        touch = 1
    else:
        print(touch)
        touch = 0
    while(not touch):
        # pengambilan tidak berhasil dan dilakukan lagi
        print("pengambilan dilakukan kembali")
        print(c_cek1, c_cek2)
        stdin_cek1, stdout_cek1, stderr_cek1 = client.exec_command("python accessdate.py")
        print(c_cek1, c_cek2)
        a_cek1 = stdout_cek1.read()
        a_cek1 = str(a_cek1)
        b_cek1 = a_cek1.split(" ")
        c_cek1 = b_cek1[4]
        stdin, stdout, stderr = client.exec_command("touch -a monitoring1.pcap")
        print(c_cek1, c_cek2)
        stdin_cek2, stdout_cek2, stderr_cek2 = client.exec_command("python accessdate.py")
        print(c_cek1, c_cek2)
        a_cek2 = stdout_cek2.read()
        a_cek2 = str(a_cek2)
        b_cek2 = a_cek2.split(" ")
        c_cek2 = b_cek2[4]
        print(c_cek1, c_cek2)
        if(c_cek1 != c_cek2):
            touch = 1
        else:
            touch = 0
    # copy pcap untuk di merge
    os.system('copy D:\\networkmonitoring1.pcap D:\\networkmonitoringcopy1.pcap')
    # merger pcap menggunakan mergecap 
    os.system("mergecap -w D:\\networkmonitoring1.pcap D:\\networkmonitoringcopy1.pcap D:\monitoring1.pcap")
    #jadikan csv untuk dibaca
    os.system("tshark -r D:\\networkmonitoring1.pcap -T fields -E separator=, -E quote=d -e frame.number -e frame.time -e_ws.col.Source -e_ws.col.Destination -e_ws.col.Protocol -e_ws.col.info > D:\\output.csv")
    client.close()
#   finally:
#   client.close()