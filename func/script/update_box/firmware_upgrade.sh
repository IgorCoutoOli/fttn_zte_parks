#!/usr/bin/expect -f
set timeout 20
set IP [lindex $argv 0]
log_user 1
set force_conservative 1


spawn telnet $IP
sleep 1
expect "Press <RETURN> to get started"
send "\n"
expect "Username:"
send "admin\n"
send "\n"
expect "Password:"
send "parks\n"
send "\n"
expect {
"*ERROR" { exit 1 }
"*Multiplexer" { exit 1 }
"*Login failed" {
	send "admin\n"
	expect "Password:"
	send "v3tf77n\n"
}
"*#" { send "\n" }
}
send "\n"
expect "*#"
send "firmware upgrade\n"
expect "*#"
exit 0
