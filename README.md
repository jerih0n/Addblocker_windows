Addblocker windows
=================

Python script for creating host-based addblocker by adding inbound rules for Windows firewall, blocking all the trafic from known advertising servers. The rules block both TCP and UDP protocols and related ports

Information
-----------
Current capabilities of the program:

* download a list of known advertising ip addresses and creates inbound block rules in windows firewall for those IP addresses that are not currently blocked
* create a firewall settings backup before starting for easter reverting all changes
  
Installation
------------
Requres python and administrative privileges

Usage
------------
For Windows: 
Opne CMD with as Administrator! Changes in the firewall requres them, and it won't work with normal or restricted windows account:
    
```bash
cd [Program Directory where Encryptor.py is located] 
```
Then run in that 
```bash
python main.py
```
Reverting
---------
In case of service breakdown, or nonavailability, you can revert your firewall setting, to the point of the program FIRST start. Only the first backup will have 0 rules created by this addblocker.
To revert the changes you can import the generated firewall file using Windows Defender and Firewall settings. You need to run the Windows Firewall settings as Administrator!

![image](https://github.com/jerih0n/Addblocker_windows/assets/17022129/538bc711-ce29-4d6a-a122-1991014d9643)


In case this does not work, you can try to execute CMD command directly. Open CMD as Administrator and enter:
```bash
netsh advfirewall import "{Path}" 
```
where Path is the full path to the .wfw file. Make sure that the file path is used into ""

