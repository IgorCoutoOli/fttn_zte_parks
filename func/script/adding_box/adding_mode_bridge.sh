#!/usr/bin/expect -f

set IP [lindex $argv 0]
set ALIAS [lindex $argv 1]
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
send "configure terminal\n"
expect "*(config)#"
send "aaa username admin level priviledged password v3tf77n\n"
expect "*(config)*"
send "no ip routing\n"
expect "*(config)#"
send "no ipv6 routing\n"
expect "*(config)#"
send "no interface bridge0\n"
expect "*(config)#"
send "no ip dhcp pool local\n"
expect "*(config)#"
send "no ip domain lookup\n"
expect "*(config)#"
send "no ip http server\n"
expect "*(config)#"
send "hostname $ALIAS\n"
expect "*(config)*"
send "bridge stp\n"
expect "*(config)*"
send "snmp-server community parks rw\n"
expect "*(config)#"
send "opmode bridge\n"
expect "*(config)#"
send "do copy r s\n"
expect "*Configuration saved.\r\n"
send "exit\n"
expect "*#"
send "reload\n"
expect "*(C)ancel]"
send "n\n"
expect "Restarting system..."
exit 0
#send "exit\n"
#expect "*#"
#send "exit\n"

