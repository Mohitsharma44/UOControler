import psutil

PROCNAME = ['omxplayer', 'omxplayer.bin']

for i in PROCNAME:
    for process in psutil.process_iter():
        if process.name() == i:
            process.parent().terminate()

for i in PROCNAME:
    for process in psutil.process_iter():
        if process.name() == i:
            process.terminate()
