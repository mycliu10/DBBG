

nst = 0
nsk = 500
for count_jobs in range(80):
    with open("counter.dat", "w") as fh:
        fh.write(nst.__str__())
        fh.write("\n")
        fh.write((nst+nsk).__str__())
    nst += nsk
    import subprocess
    subprocess.call(["qsub forge.sub"], shell=True)
    import time
    time.sleep(15)


