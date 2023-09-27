#!/bin/bash
#VERSION=$(./version.sh $1|grep -i system|cut -d":" -f2)
padrao=$(snmpget -v2c -cparks $1 iso.3.6.1.2.1.1.1.0)
version=$(echo $padrao|cut -d"," -f2|sed 's/\"//')
echo $version

