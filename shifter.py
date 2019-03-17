#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    A time shifter for subtitle synchronization.
'''

import begin
from datetime import timedelta
from re import compile, match
from string import Template

class DeltaTemplate(Template):
    delimiter = "%"

class Shift(object):
    """docstring for Shift."""
    def __init__(self, file):
        self.delta = self.strf_to_delta('00:00:00,000')
        self.file = file
        self.pattern = compile("[0-9]{2}\:[0-9]{2}\:[0-9]{2}\,[0-9]{3}")
        self.temp = DeltaTemplate("%H:%M:%S,%m")

    def delta_to_strf(self, tdelta):
        '''Convert a deltatime object in string formated as %H:%M:%S,%m.'''
        d = {"D": tdelta.days}
        hours, rem = divmod(tdelta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        mil =  tdelta.microseconds
        d["H"] = "{:02d}".format(hours)
        d["M"] = "{:02d}".format(minutes)
        d["S"] = "{:02d}".format(seconds)
        d["m"] = "{:03d}".format(int(str(mil)[:3]))
        return self.temp.substitute(**d)

    def strf_to_delta(self, i):
        '''Convert a string formated as %H:%M:%S,%m in a deltatime obect.'''
        if i[0] == '-':
            return timedelta( hours=int(i[1:3]) * -1,
                              minutes=int(i[4:6]) * -1,
                              seconds=int(i[7:9]) * -1,
                              milliseconds=int(i[10:]) * -1 )
        else:
            return timedelta( hours=int(i[0:2]),
                              minutes=int(i[3:5]),
                              seconds=int(i[6:8]),
                              milliseconds=int(i[9:]) )


    def sync(self, time_amount, start='00:00:00,000', stop=None, backwards=False):
        '''Synchronize subtitles file.'''
        prev_values = []
        in_file = open(self.file, 'r+', encoding='utf8', errors='replace')
        filedata = in_file.read()
        prev_values = self.pattern.findall(filedata)
        sfrom = self.strf_to_delta(start)
        if backwards: self.delta = self.strf_to_delta('-' + time_amount)
        else: self.delta = self.strf_to_delta(time_amount)
        index = -1
        for i in range(len(prev_values)):
            ts = self.strf_to_delta(prev_values[i])
            if ts < sfrom: index = i
            else: break
        prev_values = prev_values[index+1:]
        if stop is not None:
            index = -1
            sfrom = self.strf_to_delta(stop)
            for i in range(len(prev_values)):
                ts = self.strf_to_delta(prev_values[i])
                if ts < sfrom: index = i
                else: break
            prev_values = prev_values[:index+1]
        for i in prev_values:
            ts = self.strf_to_delta(i)
            ts += self.delta
            filedata = filedata.replace(i, self.delta_to_strf(ts))
        in_file.seek(0)
        in_file.write(filedata)
        in_file.close()

@begin.start
@begin.convert(time=str)
def main(file: 'File to synch',
         time: 'Time amount to shift(-/+) the subtitles',
         start: 'Start synch from timestamp'="00:00:00,000",
         end: 'End synch at timestamp'="23:59:59,999",
         backwards: 'Take the TIME backwards'=False
         ):
    '''Synchronize subtitles in a given file.'''
    sh = Shift(file)
    if end == "23:59:59,999": end = None
    sh.sync(time, start, end, backwards)
