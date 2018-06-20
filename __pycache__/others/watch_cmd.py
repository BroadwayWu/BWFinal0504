import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re


class Watcher:
    DIRECTORY_TO_WATCH = "static"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")
           
        self.observer.join()

class Handler(FileSystemEventHandler): 
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None  
        
        elif event.event_type == 'created':
            # only output once
            if str(event.src_path).find('.crdownload') == -1:
                print("Received created event - %s." % event.src_path)
                os.system('python3 -m label_image --graph=../../../Downloads/tensorflow-for-poets-2/tf_files/retrained_graph.pb --image='+event.src_path)
                #time.sleep(1)
                #os.system('--graph=tf_files/retrained_graph.pb \\')
                #time.sleep(1)
                #os.system('--image='+str(event.src_path))
        #elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            #print("Received modified event - %s." % event.src_path)

if __name__ == '__main__':
     w = Watcher()
     w.run()
