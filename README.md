## Shifter

A script to synchronize srt subtitles.

### Dependencies

```
$: pip3 install begins
```

### How to run it?

```
$: python3 shifter.py [FILE] [TIME]
```

Where `FILE` is the srt file that we want to modify and `TIME` is the timestamp to shift (forward/backwards) the subtitles.

`TIME` is in  format `HH:MM:SS,sss` (`HH`: hours, `MM`: minutes, `SS`: seconds, `sss`: milliseconds)


### Examples

#### - Synchronize all

For example, we have a subtitle **BB01x02.srt** and we figured out that is 5 seconds late. So we do:

```
$: python3 shifter.py BB01x02.srt 00:00:05,000 --backwards
```

Note that instead of specifying a negative timestamp we add the parameter `--backwards`.

#### - Synchronize from (or/and up to) a given timestamp

If we notice that the subtitles are shifting at a given minute, we do:

```
$: python3 shifter.py BB01x02.srt 00:00:05,000 --start 00:12:00,000 --backwards
```

And if we want to put a limit timestamp or a end, we do:

```
$: python3 shifter.py BB01x02.srt 00:00:05,000 --start 00:12:00,000 --end 00:20:00,000 --backwards
```
