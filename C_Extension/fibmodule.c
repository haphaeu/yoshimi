#include <Python.h>

int _fib(int n)
{
    if (n < 2)
        return n;
    else
    {
        int f0=0; 
        int f1=1;
        int fib=0; 
        int i;
        for(i=1; i<n; i++)
        { 
            fib=f0+f1;
            f0=f1;
            f1=fib;
        }
        return fib;
    }
}
 
static PyObject* fib(PyObject* self, PyObject* args)
{
    int n;
 
    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;
 
    return Py_BuildValue("i", _fib(n));
}
 
static PyMethodDef FibMethods[] = {
    {"fib", fib, METH_VARARGS, "Calculate the Fibonacci numbers."},
    {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
initfib(void)
{
    (void) Py_InitModule("fib", FibMethods);
}
