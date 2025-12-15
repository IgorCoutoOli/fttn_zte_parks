#!/usr/bin/expect -f
#exp_internal 1
set HOST [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]
set IP [lindex $argv 3]
set GW [lindex $argv 4]
set PORT [lindex $argv 5]
set ALIAS [lindex $argv 6]
set SERIE [lindex $argv 7]
set GPON [lindex $argv 8]
set FLOW [lindex $argv 9]
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
send "configure terminal\n"
expect {
    "*(config)#" { send "interface gpon$PORT\n" }
}
expect {
    "*ERROR" { exit 2 }
    "*Multiplexer" { exit 2 }
    "% Unknown command." { exit 2 }
    "*(config-if)#" { send "onu prks00$SERIE ip address $IP/24 gw $GW\n" }
}
expect {
    "*ERROR" { exit 5 }
    "*Multiplexer" { exit 5 }
    "% Unknown command." { exit 5 }
    "*(config-if)#" { send "onu prks00$SERIE ethernet-profile auto-on uni-port 1\n" }
}
expect {
    "*ERROR" { exit 5 }
    "*Multiplexer" { exit 5 }
    "% Unknown command." { exit 5 }
    "*(config-if)#" { send "onu prks00$SERIE flow-profile ONU101$FLOW\n" }
}
expect {
    "*ERROR" { exit 10 }
    "*Multiplexer" { exit 10 }
    "% Unknown command." { exit 10 }
    "*(config-if)#" { send "onu prks00$SERIE vlan-translation-profile _100B iphost 1\n" }
}
expect {
    "% Unknown command." { send "onu prks00$SERIE vlan-translation-profile _100 iphost\n" }
}
expect {
    "*ERROR" { exit 10 }
    "*Multiplexer" { exit 10 }
    "% Unknown command." { exit 10 }
    "*(config-if)#" { send "onu prks00$SERIE vlan-translation-profile _$FLOW uni-port 1\n" }
}
expect {
    "*ERROR" { exit 11 }
    "*Multiplexer" { exit 11 }
    "% Unknown command." { exit 11 }
    "*(config-if)#"     { send "onu prks00$SERIE alias $ALIAS\n" }
}
expect {
    "*ERROR" { exit 12 }
    "*Multiplexer" { exit 12 }
    "% Unknown command." { exit 12 }
    "*(config-if)#" { send "exit\n" }
}
expect "*#"