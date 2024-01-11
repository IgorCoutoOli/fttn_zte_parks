#!/usr/bin/expect -f
#exp_internal 1
set HOST [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]
set IP [lindex $argv 3]
set GW [lindex $argv 4]
set PORT [lindex $argv 5]
set ALIAS [lindex $argv 5]
set SERIE [lindex $argv 1]
set timeout 20

spawn telnet $HOST
sleep 1
expect "Press <RETURN> to get started"
send "\n"
expect "Username:"
send "$USER\n"
expect "Password:"
send "$PASS\n"
expect "*#"
send "conf t\n"
expect "*(config)#"
expect {
    "*(config)#" { send "interface gpon$PORT\n" }
}
expect {
    "*ERROR" { exit 2 }
    "*Multiplexer" { exit 2 }
    "*% Unknown command." { exit 2 }
    "*(config-if)#"	{ send "onu prks00$SERIE ip address $IP/24 gw $GW\n" }
}
expect {
    "*ERROR" { exit 5 }
    "*Multiplexer" { exit 5 }
    "*% Unknown command." { exit 5 }
    "*(config-if)#" { send "onu prks00$SERIE flow-profile 02_PROVISIONAMENTO\n" }
}
expect {
    "*ERROR" { exit 10 }
    "*Multiplexer" { exit 10 }
    "*% Unknown command." { exit 10 }
    "*(config-if)#" { send "onu prks00$SERIE vlan-translation-profile _100 iphost\n" }
}
expect {
    "*ERROR" { exit 11 }
    "*Multiplexer" { exit 11 }
    "*% Unknown command." { exit 11 }
    "*(config-if)#"	{ send "onu prks00$SERIE alias $ALIAS\n" }
}
expect {
    "*ERROR" { exit 12 }
    "*Multiplexer" { exit 12 }
    "*% Unknown command." { exit 12 }
    "*(config-if)#" { send "exit\n" }
}
expect "*#"
send "exit\n"
exit 0
