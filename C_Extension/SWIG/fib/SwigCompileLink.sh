swig -python fib.i
gcc -fpic -c fibmodule.c fib_wrap.c -I/usr/include/python2.7/
gcc -shared fibmodule.o fib_wrap.o -o _fib.so
echo "Done."
echo "call in python:"
echo "import fib"
echo "fib.fib(10)"
