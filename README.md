# Encrypted-File-Transfer
Encrypted File Transfer using AES

Provide encrypted file transfer between two nodes.

The program takes an input file , encrypts the file using symatric AES key (hard coded, change it to be uniq).


The software has 3 modes:Server ,client , md5 

Usage: 
Run as Client to send the file
Client -     send_enc.py <server ip> <local file>  <port>"
Server -     send_enc2.py -l <port>"
Verify md5 - send_enc.py md5 <file name>"

