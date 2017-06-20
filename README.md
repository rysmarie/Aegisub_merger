## Aegisub merger
Implementation of Aegisub files(.ass) merging program.

## How to use
Use option `--folder` or `--files` to supecify which files to merge.
When you use `--folder` option, all files inside the folder will be merged.
Use `--output` to specify the name of output file. (default is merged\_subtitle.ass)
You can use `--setpos` option to make the position of subtitles same which were set position in the original file.
For example, by using `--setpos 10 10` option, 
```
{\pos(0, 0)} subtitle1
subtitle 2
```
and
```
subtitle 3
{\pos(1, 1)}subtitle4
```
will become like this:
```
{\pos(10, 10)} subtitle1
subtitle 2
subtitle 3
{\pos(10, 10)}subtitle4
```

Subtitles will be sorted by time.

