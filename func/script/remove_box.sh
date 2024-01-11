#!/usr/bin/expect -f

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]
set PON [lindex $argv 3]
set SERIAL [lindex $argv 4]
set timeout 20

spawn telnet $IP
sleep 1
expect "Press <RETURN> to get started"
send "\n"
expect "Username:"
send "$USER\n"
expect "Password:"
send "$PASS\n"
expect "*#"
send "config terminal\n"

expect {
    "*(config)#" { send "interface gpon$PON\n" }
}

expect {
    "% Unknown command" {
        exit 2
    }
    "*(config-if)#" { send "no onu prks00$SERIAL\n" }
}

expect {
    "% Unknown command" {
        exit 9
    }
    "*(config-if)#" { send "exit\n" }
}

expect "*#"
exit 0
