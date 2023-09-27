#!/usr/bin/expect -f
set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]
set BOX [lindex $argv 3]
set timeout 5
exp_internal 0
log_user 1
set force_conservative 1

spawn telnet $IP
sleep 1
expect "Press <RETURN> to get started"
send "\n"
expect "Username:"
send "$USER\n"
expect "Password:"
send "$PASS\n"
expect {
    "% Unknown command" {
        exit 1
    }
    "*#" {
      send "show gpon onu $BOX\n"
    }
}
expect {
    "% Unknown command" {
        exit 1
    }
    "*#" {
      send "show gpon onu $BOX summary\n"
    }
}
expect {
    "*#" {
      send "exit"
    }
}
