#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pycurl
import functions
import time
import os
import threading
import copy
import magic

class Downloader(threading.Thread):
    def __init__(self, pyjama):
        threading.Thread.__init__(self)
        self.pyjama = pyjama
        self.queue = []
        self.running = False

    def run(self):
        self.running = True
        while(self.running):
            if not self.is_queue_empty():
                self.download(self.queue_shift())
            time.sleep(3)

    def quit(self):
        self.running = False

    def is_queue_empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    def queue_shift(self):
        tmp = self.queue[0]
        del self.queue[0]
        return tmp

    def queue_push(self, track):
        if not os.path.isfile(self.get_local_name(track)) and track not in self.queue:
            self.queue.append(track)

    def priorize_burn(self, tracks):
        pl = []
        for track in tracks:
            if track.local != None:
                if track in self.queue:
                    del self.queue[self.queue.index(track)]
                pl.append(track)
        self.queue = pl + self.queue

    def get_local_name(self, track):
        tmp = os.path.join(functions.install_dir(), "cache")
        tmp = os.path.join(tmp, str(track.artist_id))
        tmp = os.path.join(tmp, str(track.album_id))
        return os.path.join(tmp, str(track.id)) + '.mp3'

    def download(self, track):
        uri = track.stream #.replace('mp31', 'mp32')
        tmp = os.path.join(functions.install_dir(), "cache")
        if not os.path.isdir(tmp):
            os.mkdir(tmp)
        if not os.path.isdir(os.path.join(tmp, str(track.artist_id))):
            os.mkdir(os.path.join(tmp, str(track.artist_id)))
        tmp = os.path.join(tmp, str(track.artist_id))
        if not os.path.isdir(os.path.join(tmp, str(track.album_id))):
            os.mkdir(os.path.join(tmp, str(track.album_id)))
        tmp = os.path.join(tmp, str(track.album_id))
        target = os.path.join(tmp, str(track.id)) + '.mp3'
        #print "[!] downloading %s to %s" % (uri, target)
        cmd='(wget -c -O %s.part -q "%s" && mv %s.part %s)' % (target, uri, target, target)
        #print "[!] command:", cmd
        os.system(cmd)
        mp3 = magic.open(magic.MAGIC_NONE)
        mp3.load()
        type = mp3.file(target)
        print uri
        print type
        if type[:4] == 'MPEG':
            track.local = target
        else:
            print "[!] failed to download %s, putting back in queue" % (target)
            os.unlink(target)
            self.queue_push(track)

    def get_status(self):
        tmp = []
        for track in self.pyjama.player.playlist:
            if track in self.queue:
                tmp.append((track, 'Q'))
            else:
                tmp.append((track, 'D'))
        return tmp
