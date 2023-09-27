import os


def load_msg(language, file):
    dir_file = os.path.dirname(os.path.abspath(file))
    file = open(f'{dir_file}/language/{language}.txt', 'r')
    lines = file.readlines()
    MSG = {}
    
    for line in lines:
        slip = line.strip().split('#')
        if len(slip) == 2:
            ID, text = slip
            MSG[int(ID)] = text

    return MSG
