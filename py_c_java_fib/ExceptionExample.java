

class MyException extends Exception{
    String err;
    MyException(String s) {
        err = s;
    }
}


public class ExceptionExample {
    
    static int size = 4;
    
    public static void main(String[] args) {
        genE();  // calls a function that generates an exception
    }
    
    public static void get(int index) throws MyException { 
        if (index < 0 || index >= size) 
            throw new MyException(""+index); // throws an exception
    }
 
    public static void genE() { // this function will generate an exception by trying to get an index of -1
        try {
            get(-1);
        } catch (MyException err) { 
            System.out.println("oh dear!");
            System.out.println(err.getMessage());
            // how to re-throw the exception??
        }
    }
}
