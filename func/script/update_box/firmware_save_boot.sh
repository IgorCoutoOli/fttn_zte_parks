#!/usr/bin/expect -f
set timeout 60
set IP [lindex $argv 0]
set CD [lindex $argv 1]
#exp_internal 0
log_user 1

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
send "show $CD\n"
expect "*#"
send "exit\n"
exit 0
