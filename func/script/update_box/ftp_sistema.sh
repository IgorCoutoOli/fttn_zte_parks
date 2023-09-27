#!/usr/bin/expect
set timeout 300
set IP [lindex $argv 0]
#exp_internal 1
log_user 1
set force_conservative 1  


spawn ftp $IP
sleep 1
expect "Name*"
send "upload\n"
expect "Password:"
send "parks\n"
expect "ftp> "
send "hash\n"
expect "ftp> "
send "bin\n"
expect "ftp> "
send "put sistema_2.7.2.dwn\n"
expect "ftp> "
#send "exit\n"
exit 0
