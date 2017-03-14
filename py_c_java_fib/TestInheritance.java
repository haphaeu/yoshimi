import java.util.ArrayList;


public class TestInheritance {
    public static void main(String[] args) {
        GrandWizard grandWizard1 = new GrandWizard();
        grandWizard1.name = "Flash";
        grandWizard1.sayName();
        ((Dude)grandWizard1).sayName();
    }
}

class Dude {
    public String name;
    public int hp = 100;
    public int mp = 0;
    public void sayName() {
        System.out.println(name);
    }
    public void punchFace(Dude target) {
        target.hp -= 10;
    }
}

class Spell {
    int dummy = 1;
}

class Wizard extends Dude { 
    ArrayList<Spell> spells; 
    public void cast(String spell) {
        // cool stuff here
        mp -= 10;
    }
}

class GrandWizard extends Wizard { 
    public void sayName() { 
        System.out.println("Grand wizard" + name);
    }
}

/*
long startTime = System.nanoTime();
        res = fib(n);
        double elapsedTime = (System.nanoTime() - startTime)/1e9;
*/