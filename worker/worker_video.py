from __future__ import print_function

__author__ = 'Mohit Sharma'
__version__ = 'Development'
__license__ = 'MIT'

from omxplayer import OMXPlayer
import time
import os
import sys
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
               self._files.append(os.path.join(_DIR, files))
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
            # Play files one after the other
            self.player(self.current_file)
            
    def player(self, current_file):
        print(current_file,'\n','\tPlaying')
        # Set output window size
        self.omx = OMXPlayer(current_file, args=["--win", " 0,0,640,480"])
        self.omx.play()
        try:
            self.omx.set_position(15.0)
            while True:
                try:
                    if not(self.omx.playback_status()):
                        # If file ended.. stop playback
                        print('\n\tStopped\n')
                        self.omx.stop()
                        break
                    
                    else:
                        # Print time elapsed
                        print('\r\t','{0:.2f}'.format(self.omx.position()),
                              '/', '{0:.2f}'.format(self.omx.duration())+
                              ' seconds', end = ''),
                        sys.stdout.flush()
                    
                except Exception, e:
                    # dBUS exception for file that 
                    # finished playing. Ignore!
                    pass

        except KeyboardInterrupt, e:
            # Catch Ctrl+C and stop playing
            # current file
            print('Stopping Playback..', e)
            self.omx.stop()

    def kill(self):
        '''
        Kill everything in _PROCNAME and exit!
        Call this only when absolutely necessary
        '''
        for process in psutil.process_iter():
            # Kill omxplayer.bin
            if process.name() == _PROCNAME[0]:
                print('Killing child: ',process)
                process.terminate()


if __name__ == '__main__':
    c = Controller()
    c.check_new_files()
    c.play_files()
