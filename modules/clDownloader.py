#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pycurl
import functions
import time
import os
import threading
import copy

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
            time.sleep(1)

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
        self.queue.append(track)

    def priorize_burn(self, tracks):
        pl = []
        for track in tracks:
            if track in self.queue:
                del self.queue[self.queue.index(track)]
            pl.append(track)
        self.queue = self.queue + pl

    def download(self, track):
        uri = track.stream.replace('mp31', 'mp32')
        tmp = os.path.realpath('cache')
        if not os.path.isdir(tmp):
            os.mkdir(tmp)
        if not os.path.isdir(os.path.join(tmp, str(track.artist_id))):
            os.mkdir(os.path.join(tmp, str(track.artist_id)))
        tmp = os.path.join(tmp, str(track.artist_id))
        if not os.path.isdir(os.path.join(tmp, str(track.album_id))):
            os.mkdir(os.path.join(tmp, str(track.album_id)))
        tmp = os.path.join(tmp, str(track.album_id))
        target = os.path.join(tmp, str(track.id)) + '.mp3'
        os.system('wget -O ' + target + ' -q ' + uri)
        track.local = 'file://' + target
         