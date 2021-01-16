import os
import socket


def getMachineName():
    return socket.gethostname().replace('-', '')


def getTMpath(folder_name="data", parent_dir=None):
    uname = getMachineName()
    if parent_dir is None:
        parent_dir = 'DATA'
    parent_dir = parent_dir.lower()
    if parent_dir == 'ssd':
        parent_dir = res_strings[uname + 'SSD']
    elif parent_dir == 'data':
        parent_dir = res_strings[uname + 'DATA']
    elif parent_dir == 'dropbox':
        parent_dir = res_strings[uname + 'DROP']
    elif parent_dir == 'git':
        parent_dir = res_strings[uname + 'GIT']
    else:
        raise IOError('Unable to find parent folder')

    requested_path = os.path.join(parent_dir, folder_name)
    return requested_path


res_strings = dict(
    DolevLinuxDROP='/home/dolev/Dropbox (Aidoc)',
    DolevLinuxDATA='/home/dolev/Dropbox (Aidoc)/TailorMed Data',
    DolevLinuxGIT='/home/dolev/dev/work/aidoc-python',
    DolevLinuxSSD='/home/dolev/dev/dash/ssd'
)

home = os.path.join(os.path.expanduser('~/Dropbox (Aidoc)'))
if os.path.isdir(home) == 0:
    home = os.path.join(os.path.expanduser('~/Dropbox'))

# home = os.path.join(os.path.expanduser(r'/media/sf_Dropbox'))
baseResString = getMachineName()
if (baseResString + "DATA") not in res_strings.keys():
    res_strings[baseResString + "DATA"] = os.path.join(home, 'TailorMed Data')
    res_strings[baseResString + "DROP"] = home
    res_strings[baseResString + "GIT"] = ''
    res_strings[baseResString + "SSD"] = os.path.join(os.path.expanduser('~/ssddata'))
