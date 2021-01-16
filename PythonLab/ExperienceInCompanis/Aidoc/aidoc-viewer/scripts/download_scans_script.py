from dicomaizer.common.uid import string2hash

worklist_file = '/Users/annabankirer/Downloads/sheba_abdomen'
command = ' scp -i ~/.ssh/aidoc aidoc@demo-eastus.aidoc-nsps.com:/datadrive/viewer-data/scans/{}.mat .'
with open(worklist_file) as f:
    for line in f:
        line = line.strip()
        if len(line) == 0:
            continue

        print(command.format(string2hash(line)))