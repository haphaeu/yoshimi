@echo off

:: compile
gcc fib.c -o fib.exe
javac Fib.java

:: run
echo Python > results.txt
python fib.py >> results.txt
echo Java >> results.txt
java Fib >> results.txt
echo C >> results.txt
fib.exe >> results.txt
