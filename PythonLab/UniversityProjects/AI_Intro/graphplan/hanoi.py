def createDomainFile(domainFileName, n):
  numbers = list(range(n)) # [0,...,n-1]
  pegs = ['a','b', 'c']
  dfi = "" #Domain File Input

  # creating the propositions
  dfi += "Propositions:\n"
  for peg in pegs:
    #Option to clear
    dfi += "clear_{} ".format(peg)
    for disk in numbers:
      #Adding option for disk on top, bottom and a peg
      dfi += "disk_{disk}_on_peg_{peg} " \
             "disk_{disk}_on_top_{peg} " \
             "disk_{disk}_on_bottom_{peg} ".format(peg=peg,disk=disk)
  # adding for each disk option to be on the top of his bigger
  for diskBig in numbers:
    for diskSmall in range(diskBig):
      dfi += "disk_{diskSmall}_on_disk_{diskBig} ".format(diskBig=diskBig,diskSmall=diskSmall)
  dfi += "\n"
  # creating all the actions.
  dfi += "Actions:\n"
  for pegSrc in pegs:
    for pegDst in pegs:
      if pegSrc == pegDst:
        continue
      for diskSmall in numbers:
        # disk1 = diskSmall

        # Option of moving a disk from empty peg to a empty peg
        name = "Name: move_last_disk_{disk1}_on_peg_{pegSrc}_to_empty_peg_{pegDst}"
        pre = ["disk_{disk1}_on_peg_{pegSrc} ", "disk_{disk1}_on_top_{pegSrc} ", "disk_{disk1}_on_bottom_{pegSrc} ",
               "clear_{pegDst} "]
        addls = ["disk_{disk1}_on_peg_{pegDst} ", "disk_{disk1}_on_top_{pegDst} ", "disk_{disk1}_on_bottom_{pegDst} ",
                 "clear_{pegSrc} "]
        delete = ["disk_{disk1}_on_peg_{pegSrc} ", "disk_{disk1}_on_top_{pegSrc} ", "disk_{disk1}_on_bottom_{pegSrc} ",
                  "clear_{pegDst} "]
        dfi = creatAction(dfi, name, disk1=diskSmall, disk2=None, disk3=None, pegSrc=pegSrc, pegDst=pegDst, pre=pre,
                    addls=addls, delete=delete)
        for diskBig1 in [disk for disk in numbers if diskSmall < disk]:
          # disk1 = diskSmall disk2 = diskBig1

          # Option of moving a diskSmall from diskBig1 to a empty peg
          name = "Name: move_disk_{disk1}_from_disk_{disk2}_on_peg_{pegSrc}_to_empty_peg_{pegDst}"
          pre = ["disk_{disk1}_on_disk_{disk2} ", "disk_{disk1}_on_top_{pegSrc} ", "disk_{disk1}_on_peg_{pegSrc} ",
                 "disk_{disk2}_on_peg_{pegSrc} ", "clear_{pegDst} "]
          addls = ["disk_{disk1}_on_peg_{pegDst} ", "disk_{disk1}_on_top_{pegDst} ", "disk_{disk1}_on_bottom_{pegDst} ",
                   "disk_{disk2}_on_top_{pegSrc} "]
          delete = ["disk_{disk1}_on_disk_{disk2} ", "disk_{disk1}_on_top_{pegSrc} ", "disk_{disk1}_on_peg_{pegSrc} ",
                    "clear_{pegDst} "]
          dfi = creatAction(dfi, name, disk1=diskSmall, disk2=diskBig1, disk3=None, pegSrc=pegSrc, pegDst=pegDst, pre=pre,
                      addls=addls, delete=delete)

          # Option of moving a diskSmall from empty peg to diskBig
          name = "Name: move_last_disk_{disk1}_on_peg_{pegSrc}_to_disk_{disk2}_on_peg_{pegDst}"
          pre = ["disk_{disk1}_on_peg_{pegSrc} ", "disk_{disk1}_on_top_{pegSrc} ", "disk_{disk1}_on_bottom_{pegSrc} ",
                 "disk_{disk2}_on_peg_{pegDst} ", "disk_{disk2}_on_top_{pegDst} "]
          addls = ["disk_{disk1}_on_peg_{pegDst} ", "disk_{disk1}_on_top_{pegDst} ", "disk_{disk1}_on_disk_{disk2} ",
                   "clear_{pegSrc} "]
          delete = ["disk_{disk1}_on_peg_{pegSrc} ", "disk_{disk1}_on_top_{pegSrc} ", "disk_{disk1}_on_bottom_{pegSrc} ",
                    "disk_{disk2}_on_top_{pegDst} "]
          dfi = creatAction(dfi, name, disk1=diskSmall, disk2=diskBig1, disk3=None, pegSrc=pegSrc, pegDst=pegDst, pre=pre,
                      addls=addls, delete=delete)

          for diskBig2 in [disk for disk in numbers if diskSmall < disk and diskBig1 != disk]:
            # disk1 = diskSmall disk2 = diskBig1 disk3 = diskBig2
            # Option of moving a diskSmall from diskBig to diskBig2
            name = "Name: move_disk_{disk1}_from_disk_{disk2}_on_peg_{pegSrc}_to_disk_{disk3}_on_peg_{pegDst}"
            pre = ["disk_{disk1}_on_disk_{disk2} ", "disk_{disk1}_on_top_{pegSrc} ", "disk_{disk1}_on_peg_{pegSrc} ",
                   "disk_{disk2}_on_peg_{pegSrc} ", "disk_{disk3}_on_top_{pegDst} ", "disk_{disk3}_on_peg_{pegDst} "]
            addls = ["disk_{disk1}_on_disk_{disk3} ", "disk_{disk1}_on_top_{pegDst} ", "disk_{disk1}_on_peg_{pegDst} ",
                     "disk_{disk2}_on_top_{pegSrc} "]
            delete = ["disk_{disk1}_on_disk_{disk2} ", "disk_{disk1}_on_top_{pegSrc} ",
                      "disk_{disk1}_on_peg_{pegSrc} ", "disk_{disk3}_on_top_{pegDst} "]
            dfi = creatAction(dfi, name, disk1=diskSmall, disk2=diskBig1, disk3=diskBig2, pegSrc=pegSrc, pegDst=pegDst, pre=pre,
                        addls=addls, delete=delete)

  domainFile = open(domainFileName, 'w') #use domainFile.write(str) to write to domainFile
  domainFile.write(dfi)
  domainFile.close()  
        
def creatAction(dfi,name,disk1=None,disk2=None,disk3=None,pegSrc=None, pegDst=None,pre=[],addls=[],delete=[]):
  dfi += name.format(disk1=disk1,disk2=disk2,disk3=disk3,pegSrc=pegSrc,pegDst=pegDst)
  dfi += "\npre: "
  for p in pre:
    dfi += p.format(disk1=disk1,disk2=disk2,disk3=disk3,pegSrc=pegSrc,pegDst=pegDst)
  dfi += "\nadd: "
  for p in addls:
    dfi += p.format(disk1=disk1,disk2=disk2,disk3=disk3,pegSrc=pegSrc,pegDst=pegDst)
  dfi += "\ndelete: "
  for p in delete:
    dfi += p.format(disk1=disk1, disk2=disk2,disk3=disk3, pegSrc=pegSrc, pegDst=pegDst)
  dfi += "\n"
  return dfi

def createProblemFile(problemFileName, n):
  numbers = list(range(n)) # [0,...,n-1]
  pegs = ['a','b', 'c']
  dfi = ""  # Domain File Input
  # creating a problem all the bilding on a and need to move to b
  dfi += "Initial state: clear_b clear_c "
  # puting all bilsing on a
  dfi += "disk_0_on_top_a "
  # disks 0 to n-2
  for small in numbers:
    dfi += "disk_{small}_on_peg_a ".format(small=small)
    if small < n-1:
      big = small + 1
      dfi += "disk_{small}_on_disk_{big} ".format(big=big,small=small)
  # last disk
  dfi += "disk_{last}_on_bottom_a ".format(last=numbers[-1])
  dfi += "\n"

  # define goal on c
  dfi += "Goal state: clear_a clear_b "
  # puting all bilsing on a
  dfi += "disk_0_on_top_c "
  # disks 0 to n-2
  for small in numbers:
    dfi += "disk_{small}_on_peg_c ".format(small=small)
    if small < n - 1:
      big = small + 1
      dfi += "disk_{small}_on_disk_{big} ".format(big=big, small=small)
  # last disk
  dfi += "disk_{last}_on_bottom_c ".format(last=numbers[-1])
  dfi += "\n"

  problemFile = open(problemFileName, 'w')  # use problemFile.write(str) to write to problemFile
  problemFile.write(dfi)
  problemFile.close()

import sys
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Usage: hanoi.py n')
    sys.exit(2)
  
  n = int(float(sys.argv[1])) #number of disks
  domainFileName = 'hanoi' + str(n) + 'Domain.txt'
  problemFileName = 'hanoi' + str(n) + 'Problem.txt'
  
  createDomainFile(domainFileName, n)
  createProblemFile(problemFileName, n)