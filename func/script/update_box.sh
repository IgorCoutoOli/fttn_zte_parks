#!/bin/bash
data=$(date +%d/%m" "%H:%M)
ONU=$1

function pinga {
    printf "\nAGUARDANDO ONU $1 PINGAR..."
    date1=$(date +"%s")
    while [ $((`date +"%s"`-$date1)) -lt 300 ]
    do
        if (! /usr/bin/ping -W3 -c3 $1 &>/dev/null)
        then
            printf "."
        else
            printf "! PINGOU!\n\n"
            i=0
            break
        fi
        i=1
    done

    if [[ $i == 1 ]]
    then
        printf "\n\nONU não pingou dentro de 5min, terminando o script\n"
        exit 8
    fi
}

cd /root/bot-prov-fttn/src/script/upgrade/att

echo -e "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo -e "!!! ATUALIZANDO-BOOT!!! Colocando em modo de upgrade de firmware"
echo -e "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"

pinga $ONU

./firmware_upgrade.sh $ONU

echo -e "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo -e "!!! ATUALIZANDO-BOOT!!! Enviando firmware, por FTP, do setor BOOT"
echo -e "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"

pinga $ONU

./ftp_boot.sh $ONU

echo -e "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo -e "!!! ATUALIZANDO-BOOT!!! Salvando firmware e rebootando"
echo -e "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"

pinga $ONU

./firmware_save_boot.sh $ONU

echo -e "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo -e "!!! ATUALIZANDO-BOOT!!! Firmware do setor BOOT atualizado"
echo -e "!!! ATUALIZANDO-BOOT!!! Aguardando ONU voltar"
echo -e "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
sleep 30

pinga $ONU

echo -e "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo -e "!!! ATUALIZANDO-SYSTEM!!! ONU $ONU modo firmware upgrade"
echo -e "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"

pinga $ONU

./firmware_upgrade.sh $ONU

echo -e "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo -e "!!! ATUALIZANDO-SYSTEM!!! ONU $ONU enviando firmware"
echo -e "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"

pinga $ONU

./ftp_sistema.sh $ONU

echo -e "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo -e "!!! ATUALIZANDO-SYSTEM!!! ONU $ONU firmware enviado"
echo -e "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"

pinga $ONU

./firmware_save_sistema.sh $ONU

echo -e "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo -e "!!! ATUALIZANDO-SYSTEM!!! ONU $ONU firmware salvo"
echo -e "!!! ATUALIZANDO-SYSTEM!!! ONU $ONU rebootando"
echo -e "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
sleep 30

pinga $ONU

VERSAO=$(./get_version.sh $1)

echo -e "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n!!!!!! ONU $1 atualizada $VERSAO !!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"