### PLY Compiler

A compiler built for Formal Languages and Translation Techniques classes

Winter Semester 2017/2018  

http://ki.pwr.edu.pl/gebala/dyd/jftt2017.html

Requirements:
```
Python 3.6.3
PLY 3.9
```
Installation: (for Debian)

```
sudo apt-get install python3-pip
sudo pip3 install ply
```
Usage:
```
python3 plyc.py [input] [--output OUTPUT]
```
To compile a program, provide path as `input` argument. By default, it compiles to file `a.out` in cwd, you can specify your own filename using `--output` flag
