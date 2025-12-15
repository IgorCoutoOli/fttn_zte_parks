import os
import subprocess
import time
from ping3 import ping

from conf.settings import information
from func.utils import olt_check, error_check
from conf.settings import MSG

dir_file = os.path.dirname(os.path.abspath(__file__))


async def check_info():
    olt = information['box'][:3]
    access = await olt_check(olt)
    info = {}

    if access == 0:
        info["message"] = MSG[2] # Digite uma caixa que seja válida. \nExemplo: 2311120
        information.pop('box', None)
        return info

    info['status'] = 1

    command = [f'{dir_file}/script/check_info.sh', access['IP'], access['USER'], access['PASS'], information['box']]
    script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = script.communicate()

    lines = output.decode().split('\n')

    read = False
    write = ""

    if script.returncode != None:
        error = await error_check(script.returncode)

        if error is not None:
            info["message"] = f'{error}'
            return info

    for line in lines:
        if 'OLT-' in line:
            read = True
            continue

        if read:
            write += f'{line}\n'

    info["message"] = write
    information['status'] = 0

    return info


async def check_macs():
    olt = information['box'][:3]
    pon = information['box'][3:5]
    slot = information['box'][5:].lstrip('0')

    ip = f'10.{olt}.{pon}.{slot}'
    info = {'status': 1}

    if not ping(ip, timeout=60*2):
        information['status'] = 0
        info["message"] = MSG[21]
        return info

    script = subprocess.Popen([f'{dir_file}/script/check_macs.sh', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = script.communicate()

    lines = output.decode().split('\n')

    read = False
    write = ""

    if script.returncode != None:
        error = await error_check(script.returncode)

        if error is not None:
            info["message"] = f'{error}'
            return info

    for line in lines:
        if '#' in line or '--More--' in line:
            read = True
            continue

        if read:
            write += f'{line}\n'

    info["message"] = write
    information['status'] = 0

    return info


async def reboot_box():
    olt = information['box'][:3]
    pon = information['box'][3:5]
    slot = information['box'][5:].lstrip('0')

    ip = f'10.{olt}.{pon}.{slot}'
    info = {'status': 1}

    if not ping(ip, timeout=60*2):
        information['status'] = 0
        info["message"] = MSG[21]
        return info

    script = subprocess.Popen([f'{dir_file}/script/reboot_box.sh', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if script.returncode != None:
        error = await error_check(script.returncode)

        if error is not None:
            info["message"] = f'{error}'
            return info

    info["message"] = MSG[20]
    information['status'] = 0

    return info


async def remove_box():
    olt = information['box'][:3]
    pon = f"{information['box'][3]}/{information['box'][4]}"

    access = await olt_check(olt)
    info = {}

    if access == 0:
        info["message"] = MSG[2]  # Digite uma caixa que seja válida. \nExemplo: 2311120
        information.pop('box', None)
        information.pop('serial', None)
        return info

    info['status'] = 1

    print(access['IP'], access['USER'], access['PASS'], pon, information['serial'])

    command = [f'{dir_file}/script/remove_box.sh', access['IP'], access['USER'], access['PASS'], pon, information['serial']]
    script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = script.communicate()

    # Verificar a saída e o erro
    print(f"Saída do script:\n {stdout.decode()}")
    print(f"Erro do script:\n {stderr.decode()}")

    if script.returncode != None:
        error = await error_check(script.returncode)

        if error is not None:
            info["message"] = f'{error}'
            return info

    info["message"] = MSG[22]
    information['status'] = 0

    return info


async def adding_box():
    olt = information['box'][:3]
    gpon = f"{information['box'][3]}/{information['box'][4]}"
    pon = information['box'][3:5]
    port_pon = f"{information['box'][3]}/{information['box'][4]}"
    slot = information['box'][5:].lstrip('0')
    flow = f"{olt[1:3]}{pon}"

    ip = f'10.{olt}.{pon}.{slot}'
    gw = f'10.{olt}.{pon}.65'

    access = await olt_check(olt)
    info = {}

    if access == 0:
        info["message"] = MSG[2]  # Digite uma caixa que seja válida. \nExemplo: 2311120
        information.pop('box', None)
        information.pop('serial', None)
        return info

    info['status'] = 1

    if information['serial'][0] == "d" or information['serial'][0] == "D":
        print(access, ip, gw, port_pon, gpon, flow)
        command = [f'{dir_file}/script/adding_box/adding_profile_new.sh', access['IP'], access['USER'], access['PASS'], ip, gw, port_pon, information['box'], information['serial'], gpon, flow]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = script.communicate()

        # Verificar a saída e o erro
        print(f"Saída do script:\n {stdout.decode()}")
        print(f"Erro do script:\n {stderr.decode()}")

        if script.returncode != None:
            error = await error_check(script.returncode)

            if error is not None:
                info["message"] = f'{error}'
                print(error, script.returncode)
                return info
    else:
        # Configurando parte das configurações na OLT
        command = [f'{dir_file}/script/adding_box/adding_olt_config.sh', access['IP'], access['USER'], access['PASS'], ip, gw, port_pon, information['box'], information['serial']]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = script.communicate()

        # Verificar a saída e o erro
        print(f"Saída do script:\n {stdout.decode()}")
        print(f"Erro do script:\n {stderr.decode()}")

        if script.returncode != None:
            error = await error_check(script.returncode)

            if error is not None:
                info["message"] = f'{error}'
                print(error, script.returncode)
                return info

    if not ping(ip, timeout=60*2):
        information['status'] = 0
        info["message"] = MSG[21]
        return info

    time.sleep(10)

    # Adicionando parte das configurações na ONU
    if information['serial'][0] != "d" and information['serial'][0] != "D":
        script = subprocess.Popen(f'snmpget -v2c -cparks {ip} iso.3.6.1.2.1.1.1.0', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = script.communicate()
        output = output.decode()

        command = [f'{dir_file}/script/adding_box/adding_mode_bridge.sh', ip, information['box']]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = script.communicate()

        # Verificar a saída e o erro
        print(f"Saída do script:\n {stdout.decode()}")
        print(f"Erro do script:\n {stderr.decode()}")

        if script.returncode != None:
            error = await error_check(script.returncode)

            if error is not None:
                info["message"] = f'{error}'
                print(error, script.returncode)
                return info

        print(access['IP'], access['USER'], access['PASS'], gpon, port_pon, flow, information['serial'])

        # Ultima parte do provisionando na OLT.
        command = [f'{dir_file}/script/adding_box/adding_profile.sh', access['IP'], access['USER'], access['PASS'], gpon, port_pon, flow, information['serial']]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = script.communicate()

        # Verificar a saída e o erro
        print(f"Saída do script:\n {stdout.decode()}")
        print(f"Erro do script:\n {stderr.decode()}")

        if script.returncode != None:
            error = await error_check(script.returncode)

            if error is not None:
                info["message"] = f'{error}'
                print(error, script.returncode)
                return info

        if not "Version 2.7.2" in output and not "Version 3" in output:
            info["message"] = MSG[23]
        else:
            info["message"] = MSG[24]
    else:
        info["message"] = MSG[24]

    information['status'] = 0
    return info

async def update_box():
    olt = information['box'][:3]
    pon = information['box'][3:5]
    slot = information['box'][5:].lstrip('0')
    ip = f'10.{olt}.{pon}.{slot}'
    info = {}

    if not ping(ip, timeout=60*2):
        information['status'] = 0
        info["message"] = MSG[21]
        return info

    info['status'] = 1

    script = subprocess.Popen(f'snmpget -v2c -cparks {ip} iso.3.6.1.2.1.1.1.0', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = script.communicate()
    output = output.decode()

    if not "Version 2.7.2" in output and not "Version 3" in output:
        command = [f'{dir_file}/script/update_box/firmware_upgrade.sh', ip]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = script.communicate()

        # Verificar a saída e o erro
        print(f"Saída do script:\n {stdout.decode()}")
        print(f"Erro do script:\n {stderr.decode()}")

        if not ping(ip, timeout=60*5):
            information['status'] = 0
            info["message"] = MSG[27]
            return info

        command = [f'{dir_file}/script/update_box/ftp_boot.sh', ip]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = script.communicate()

        # Verificar a saída e o erro
        print(f"Saída do script:\n {stdout.decode()}")
        print(f"Erro do script:\n {stderr.decode()}")

        if not ping(ip, timeout=60*5):
            information['status'] = 0
            info["message"] = MSG[27]
            return info

        command = [f'{dir_file}/script/update_box/firmware_save_boot.sh', ip]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = script.communicate()

        # Verificar a saída e o erro
        print(f"Saída do script:\n {stdout.decode()}")
        print(f"Erro do script:\n {stderr.decode()}")

        if not ping(ip, timeout=60*5):
            information['status'] = 0
            info["message"] = MSG[27]
            return info

        command = [f'{dir_file}/script/update_box/firmware_upgrade.sh', ip]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = script.communicate()

        # Verificar a saída e o erro
        print(f"Saída do script:\n {stdout.decode()}")
        print(f"Erro do script:\n {stderr.decode()}")

        if not ping(ip, timeout=60*5):
            information['status'] = 0
            info["message"] = MSG[27]
            return info

        command = [f'{dir_file}/script/update_box/ftp_sistema.sh', ip]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = script.communicate()

        # Verificar a saída e o erro
        print(f"Saída do script:\n {stdout.decode()}")
        print(f"Erro do script:\n {stderr.decode()}")

        if not ping(ip, timeout=60*5):
            information['status'] = 0
            info["message"] = MSG[27]
            return info

        command = [f'{dir_file}/script/update_box/firmware_save_sistema.sh', ip]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = script.communicate()

        # Verificar a saída e o erro
        print(f"Saída do script:\n {stdout.decode()}")
        print(f"Erro do script:\n {stderr.decode()}")

        time.sleep(40)

        if not ping(ip, timeout=60*5):
            information['status'] = 0
            info["message"] = MSG[29]
            return info

        script = subprocess.Popen(f'snmpget -v2c -cparks {ip} iso.3.6.1.2.1.1.1.0', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = script.communicate()
        output = output.decode()

        if not "Version 2.7.2" in output and not "Version 3" in output:
            info["message"] = MSG[28]
            information['status'] = 0
            return info
        else:
            info["message"] = MSG[26]
            information['status'] = 0
            return info
    else:
        info["message"] = MSG[25]
        information['status'] = 0
        return info