#!/usr/bin/expect -f

set HOST [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]
set VLAN [lindex $argv 3]
set PORT [lindex $argv 5]
set FLOW [lindex $argv 6]
set SERIE [lindex $argv 7]
set timeout 20


spawn telnet $HOST
sleep 1
expect "Press <RETURN> to get started"
send "\n"
expect "Username:"
send "admin\n"
expect "Password:"
send "v3tf77n\n"
expect "*#"
send "config terminal\n"
expect {
    "*ERROR" { exit 7 }
    "*Multiplexer" { exit 7 }
    "*% Unknown command." { exit 7 }
    "*(config)#" { send "interface gpon$PORT\n" }
}
sleep 1
expect {
    "*ERROR" { exit 7 }
    "*Multiplexer" { exit 7 }
    "*% Unknown command." { exit 7 }
    "*(config-if)#" { send "onu prks00$SERIE flow-profile $FLOW\n" }
}
sleep 1
expect {
    "*ERROR" { exit 7 }
    "*Multiplexer" { exit 7 }
    "*% Unknown command." { exit 7 }
    "*(config-if)#" { send "onu prks00$SERIE vlan-translation-profile _$FLOW uni-port 1\n" }
}
sleep 1
expect {
    "*(config-if)#" { send "exit\n" }
}
expect "*#"
#send "exit\n"
exit 0
