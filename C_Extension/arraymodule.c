#include <Python.h>

int* _array(int n)
{
    int *p;
    p = (int*) malloc(n * sizeof(int));
    int i;
    for(i=0;i<n;i++)
    {
       p[i]=random();
    }
    return p;
}
 
static PyObject* array(PyObject* self, PyObject* args)
{
    int n;
 
    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;
 
    return Py_BuildValue("i", _array(n));
}
 
static PyMethodDef ArrayMethods[] = {
    {"array", array, METH_VARARGS, "Return a random array of size n."},
    {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
initarray(void)
{
    (void) Py_InitModule("array", ArrayMethods);
}
