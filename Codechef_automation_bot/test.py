import subprocess

comp_string = subprocess.getoutput('g++ sol.cpp')

rtime_errs = ""
if not comp_string:
    rtime_errs = subprocess.getoutput('./a.out< given_input.dat >yourOut.dat')
else:
    print('comp:' + comp_string)
    exit()
if rtime_errs:
    print(rtime_errs)
    exit()
your = open('yourOut.dat', 'r')
their = open('giver_output.dat', 'r')
yout = list(map(str.strip, your.readlines()))
tout = list(map(str.strip, their.readlines()))
ylen, tlen = len(yout), len(tout)

if ylen == tlen:
    for i in range(0, tlen):
        if yout[i] != tout[i]:
            print('Outputs doesn\'t Match 😥 keep trying 💪  .To see your output see yourOut.dat file.')
            break
    else:
        print('Outputs Match Awesome 👏  👏  🎉  🎊 . To see your output see yourOut.dat file.')
else:
    print('Output doesn\'t Match 😥 keep trying 💪  .To see your output see yourOut.dat file.')
