#!/usr/bin/expect -f
set IP [lindex $argv 0]
set timeout 20

log_user 1
exp_internal 0

spawn telnet $IP
sleep 1
expect "Press <RETURN> to get started\r\n\r\n"
send "\n"
expect "Username:"
send "admin\n"
expect "Password:"
send "parks\n"
send "\n"
expect {
"*ERROR" { exit 21 }
"*Multiplexer" { exit 21 }
"*Login failed" {
        send "admin\n"
        expect "Password:"
        send "v3tf77n\n"
}
"*#" { send "\n" }
}
send "\n"
expect "*#"
send "reload\n"
expect "*(C)ancel]"
send "n\n"
expect "Restarting system..."