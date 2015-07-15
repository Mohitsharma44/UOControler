__author__ = 'Mohit Sharma'
__version__ = 'Development'
__license__ = 'MIT'

from omxplayer import OMXPlayer
import time
import os
import psutil

_DIR = os.path.join(os.path.expanduser('~'), 'Videos')
_PROCNAME = ['omxplayer.bin']

class Controller(object):
    def __init__(self):
        pass

    def check_new_files(self):
        '''
        check new files from _DIR
        '''
        self._files = []
        for files in os.listdir(_DIR):
            if files.endswith(('wmv', 'mp4', 'mov', 'avi')):
               self._files.append(files)
            else:
                pass

    def play_files(self):
        '''
        Play all the files sequentially
        '''
        self.idx = 0
        while True:
            # Loop over list of files
            self.current_file = self._files[self.idx]
            self.idx = (self.idx + 1) % len(self._files)
            self.next_file = self._files[self.idx]
            self.player(self.current_file)
            print 'player: ',self.player

    def player(self, current_file):
        print 'Playing:',current_file
        #time.sleep(1)
        self.omx = OMXPlayer(current_file, args=["--win", " 0,0,640,480"])
        self.omx.play()
        print self.omx.playback_status()
        try:
            while True:
                if not(self.omx.playback_status()):
                    print current_file, 'stopped'
                    break
                else: 
                    print self.omx.position()
                    time.sleep(3)
        except KeyboardInterrupt, e:
            print 'Stopping Playback..', e
            self.omx.stop()

    def kill(self):
        '''
        Kill everything in _PROCNAME and exit!
        Call this only when absolutely necessary
        '''
        for process in psutil.process_iter():
            # Kill omxplayer.bin
            if process.name() == _PROCNAME[0]:
                print 'Killing child: ',process
                process.terminate()


if __name__ == '__main__':
    c = Controller()
    c.check_new_files()
    c.play_files()
    c.player(_dir+'/IRTL.mp4')

'''
omx = OMXPlayer('IRTL.mp4')
omx.play()
while True:
    if (omx.playback_status() != 'Playing'):
        break
    else:
        print omx.position()
    time.sleep(2)
'''
