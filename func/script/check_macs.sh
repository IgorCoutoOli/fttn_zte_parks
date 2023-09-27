#!/usr/bin/expect -f
set timeout 5
set IP [lindex $argv 0]
exp_internal 0
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
  "*Login failed" {
          send "admin\n"
          expect "Password:"
          send "v3tf77n\n"
  }
  "*#" { send "\n" }
}
send "\n"
expect "*#"
send "show macs\n"
expect -ex "--More--" {send -- " "; exp_continue}
expect "*#"
send "exit\n"
exit 0
