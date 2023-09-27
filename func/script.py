import os
import subprocess

from conf.settings import information
from func.utils import olt_check, error_check
from conf.settings import MSG
from ping3 import ping

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

    error = await error_check(script.returncode)

    if error is not None:
        info["message"] = f'{error}'
        print(error, script.returncode)
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

    if not ping(ip):
        information['status'] = 0
        info["message"] = MSG[21]
        return info

    script = subprocess.Popen([f'{dir_file}/script/check_macs.sh', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = script.communicate()

    lines = output.decode().split('\n')

    read = False
    write = ""

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

    if not ping(ip):
        information['status'] = 0
        info["message"] = MSG[21]
        return info

    script = subprocess.Popen([f'{dir_file}/script/reboot_box.sh', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    error = await error_check(script.returncode)

    if error is not None:
        info["message"] = f'{error}'
        return info

    info["message"] = MSG[20]
    information['status'] = 0

    return info


async def remove_box():
    olt = information['box'][:3]
    pon = information['box'][3:5]

    access = await olt_check(olt)
    info = {}

    if access == 0:
        info["message"] = MSG[2]  # Digite uma caixa que seja válida. \nExemplo: 2311120
        information.pop('box', None)
        information.pop('serial', None)
        return info

    info['status'] = 1

    command = [f'{dir_file}/script/adding_box/remove_box.sh', access['IP'], access['USER'], access['PASS'], pon, information['serial']]
    script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    error = await error_check(script.returncode)

    if error is not None:
        info["message"] = f'{error}'
        print(error, script.returncode)
        return info

    info["message"] = MSG[22]
    information['status'] = 0

    return info


async def adding_box():
    olt = information['box'][:3]
    pon = information['box'][3:5]
    slot = information['box'][5:].lstrip('0')
    vlan = f"{pon[0]}/{pon[1]}"
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

    command = [f'{dir_file}/script/adding_box/adding_olt_config.sh', access['IP'], access['USER'], access['PASS'], ip, gw, pon, information['box'], information['serial']]
    script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = await error_check(script.returncode)

    if error is not None:
        info["message"] = f'{error}'
        print(error, script.returncode)
        return info

    if not ping(ip):
        information['status'] = 0
        info["message"] = MSG[21]
        return info

    output = subprocess.check_output(f'snmpget -v2c -cparks {ip} iso.3.6.1.2.1.1.1.0', shell=True, universal_newlines=True)
    mode = output.split("(")[1].split(")")[0].strip()
    if mode != "SFU":
        command = [f'{dir_file}/script/adding_box/adding_mode_bridge.sh', ip, information['box']]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        error = await error_check(script.returncode)

        if error is not None:
            info["message"] = f'{error}'
            print(error, script.returncode)
            return info

        if not ping(ip, timeout=60*5):
            information['status'] = 0
            info["message"] = MSG[21]
            return info

    command = [f'{dir_file}/script/adding_box/adding_profile.sh', access['IP'], access['USER'], access['PASS'], vlan, pon, flow, information['serial']]
    script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = await error_check(script.returncode)

    if error is not None:
        info["message"] = f'{error}'
        print(error, script.returncode)
        return info

    output = subprocess.check_output(f'snmpget -v2c -cparks {ip} iso.3.6.1.2.1.1.1.0', shell=True, universal_newlines=True)
    lines = output.splitlines()
    if len(lines) < 2:
        exit(4)

    default = lines[1]
    version = default.split(",")[1].strip("\"")

    if version != "Version 2.7.2":
        info["message"] = MSG[23]
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

    if not ping(ip):
        information['status'] = 0
        info["message"] = MSG[21]
        return info

    info['status'] = 1

    output = subprocess.check_output(f'snmpget -v2c -cparks {ip} iso.3.6.1.2.1.1.1.0', shell=True, universal_newlines=True)
    lines = output.splitlines()
    if len(lines) < 2:
        exit(4)

    default = lines[1]
    version = default.split(",")[1].strip("\"")

    if version != "Version 2.7.2":
        command = [f'{dir_file}/script/update_box.sh', ip]
        script = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        error = await error_check(script.returncode)

        if error is not None:
            info["message"] = f'{error}'
            print(error, script.returncode)
            return info

        info["message"] = MSG[26]
        information['status'] = 0
        return info
    else:
        info["message"] = MSG[25]
