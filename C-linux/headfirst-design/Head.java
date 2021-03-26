import java.util.ArrayList;

/**
 * Welcome To Design Patterns
 * --------------------------
 * 
 * A good way of thinking is: with functions and classes, we get code reuse, but with design patterns 
 * we get experience reuse. It is not about forcing your code into fitting some design pattern, but 
 * being experienced enough to recognize that a pattern would be very effective in solving your 
 * problem. 
 * 
 * Just as a reminder, abstract methods are used as a template; each child is responsive for implementing
 * these abstract functions. The same goes for abstract classes. The book gives an example about a duck
 * simulator program, where the programmer adds the fly() functionality to the superclass itself. The 
 * problem is that not all ducks fly, so he decides to override the fly function wherever the duck isn't
 * supposed to fly. Lots of code duplication, which eventually will create worse problems along the way.
 * The programmer realizes that the spec is changing quickly so he whips up some interfaces, which 
 * takes care of cases where only some (but not all subclasses) can gain a new ability. This is, again, 
 * not the cleanest solution, because there could be 48 kinds of ducks, and you'll have to make changes
 * to all. Another problem is that there could be differences in the how different types of  ducks fly
 * themselves; so, are you going to create FlyableInterface1, FlyableInterface2, ... ? Nah, not a good
 * idea. 
 * 
 * Design principle: take what varies and "encapsulate" it, so it won't affect the rest of your code. 
 * All design pattern follow this fundamental idea of seperating what changes from what stays solid 
 * and unchanged throughout the program. We know that flying and quacking is varying across ducks,
 * so we will create new classes which will implement those. 
 * 
 * Design principle: Program to an interface, not an implementation
 * What does this mean? The new class you've created (which holds flying and quacking behaviors)
 * will implement the interfaces, and not the main superclass. You are trying to set the behavior 
 * at runtime and not write the implementation into the class itself.
 */

// Using this, the structure we have right now is as below
interface FlyBehavior {
    void fly();
}

interface QuackBehavior {
    void quack();
}

class FlyWithWings implements FlyBehavior{
    @Override 
    public void fly() {

    }
}

class FlyNoWay implements FlyBehavior{
    @Override
    public void fly() {

    }
}

class Quack implements QuackBehavior{
    @Override 
    public void quack() {

    }
}

class Squeak implements QuackBehavior{
    @Override 
    public void quack() {

    }
}

class MuteQuack implements QuackBehavior{
    @Override 
    public void quack() {

    }
}

/**
 * Now you can reuse the fly behavior by implementing the interface and proving your own functionality.
 * Just instantiate the interface variables and add a function which calls the interface function. This 
 * way is programming to an implementation, which goes against the core design principles we discussed
 * earlier, but we're doing it for now. 
 * We're setting all of this so we can do stuff like, Duck duck = new TypeOfDuck(), which will have 
 * its own implementation of fly/quack behavior in duck.performQuack() or duck.fly(). 
 * Design principle: Composition > Inheritance
 * What is composition anyways? Combining simpler types into more complex types, like we did with the 
 * duck example. With this example, we used the strategy pattern. We encapsulated algorithms (quack and 
 * duck) such that either could be interchangable. 
 */

/**
 * The Observer Pattern 
 * --------------------
 * 
 * Using this pattern, objects will be able to tell when events they care about happens i.e. it is 
 * sort of a notification system. Objects can choose to be notified or not. In this chapter, we will
 * think about a weather monitoring application. What are the distinct pieces that make up this 
 * application? The weather station, the WeatherData object, and the user interface. We have a 
 * measurementsChanged() function, which we have to call for three different items i.e. 
 * currentConditions, weather stats, and weather forecast. Also, this must be extensible. If new 
 * developers want to add another display screen, the measurementsChanged() function must be called
 * in it as well. How to not duplicate this?
 * 
 * A real life example of the observer pattern is a Netflix subscription. As long as you subscribe, 
 * you get latest movies. You can unsubscribe to not get Netflix's services any more. 
 * Publisher + Subscriber = Observer Pattern 
 * A formal definition of the observer pattern is that of a one-to-many relationship such that if 
 * one object changes state, all its dependents are notified and updated automatically. 
 * 
 * Usually, we have a subject interface which defines methods for registering, removing, and 
 * notifying observers. We also have an observer interface, which just has an update function, and 
 * all observers must implement this, just like subjects must implement their interface. 
 * Design principle: when objects interact, strive for a loosely couples design 
 */

// Weather station design 
interface Observer {
    void update(float temp, float humidity, float pressure);
}

interface Subject {
    void registerObserver(Observer o);
    void removeObserver(Observer o);
    void notifyObservers();
}

interface DisplayElement {
    void display();
}

class WeatherData implements Subject {
    private ArrayList<Observer> observers;
    private float temp;
    private float humidity;
    private float pressure;

    public WeatherData() {
        observers = new ArrayList<Observer>();
    }

    @Override 
    public void registerObserver(Observer o) {
        observers.add(o);
    }

    @Override 
    public void removeObserver(Observer o) {
        observers.remove(o);
    }

    @Override 
    public void notifyObservers() {
        for (int i = 0; i < observers.size(); i++) {
            Observer observer = (Observer) observers.get(i);
            observer.update(temp, humidity, pressure);
        }
    }

    public void measurementsChanged() {
        notifyObservers();
    }

    public void setMeasurements(float temp, float humidity, float pressure) {
        this.temp = temp;
        this.humidity = humidity;
        this.pressure = pressure;
        measurementsChanged();
    }
}

class CurrentConditionsDisplay implements Observer, DisplayElement {
    private float temp;
    private float humidity;
    private float pressure;
    Subject weatherData;

    CurrentConditionsDisplay(Subject weatherData) {
        this.weatherData = weatherData;
        weatherData.registerObserver(this);
    }
    
    @Override 
    public void update(float temp, float humidity, float pressure) {
        this.temp = temp;
        this.humidity = humidity;
        this.pressure = pressure;
        display();
    }

    @Override
    public void display() {
        System.out.println("Current conditions: " + temp + "F degrees, " + humidity + " humidity, and " + pressure + " pressure");
    }   
}

/**
 * We called display() right after the values get updated, which may not be the best way to do it, 
 * but since this is a simple example, we did it that way. All of these functionalities also exist 
 * with the in-built Observable API given to us by Java. Through it, we can even pull data through 
 * observers rather than just the subjects pushing data. Obserable is a class, so our WeatherData 
 * object must extend Observable. The observers will implement the observer interface to get 
 * going. Conventionally, while using the Observer pattern, the pulling pattern is considered 
 * more correct. 
 */

/**
 * The Decorator Pattern 
 * --------------------
 * 
 * "Decorating classes at runtime rather than compile time". For this chapter, we will take up the 
 * example of Starbuzz coffee. Each coffee is described by an abstract class which contains the 
 * decription and an abstract method cost(), which must be implemented by the children. Coffees
 * also have their own condiments, which will increase the price of coffee, depending on what it 
 * is. Rather than having a, what the book defines, "a class explosion", we will see how this 
 * design patter can be used to create a maintainable system here. 
 * 
 * Design principle: "Code should be closed to change yet open for extension".
 * The idea is to basically start with a Beverage class just like we did in the beginning, but we'll
 * decorate it with condiments. The decorator is wrapped all around the Beverage in question, and
 * polymorphism is applicable as the decorator mirrors the type of object it is wrapping. The 
 * decorators will have their own cost() function, so the finalized cost will be a long chain 
 * of cost calls, starting from the exterior decorator, going all the way to the cost() function 
 * of the Beverage. 
 * 
 * Formal definition: attaches more responsibility to an object dynamically. 
 * The key point is that the decorator must also extend the abstract class to achieve the similar 
 * types; we are not extending for the sake of inheriting behavior; we are doing it to match the 
 * types. Traditionally, the decorator pattern uses an abstract type as a model, but in Java we
 * can use interfaces to do the same too. 
 */

// Starbuzz's buzzed out design 
abstract class Beverage {
    String description = "Unknown Beverage";

    public String getDescription() {
        return description;
    }

    public abstract double getCost();
}

abstract class CondimentDecorator extends Beverage {
    // Reimplementing it so the condiment description gets stacked onto the beverage description as well
    public abstract String getDescription();
}

class Espresso extends Beverage {
    public Espresso() {
        description = "Espresso";
    }

    public double getCost() {
        return 1.99;
    }
}

class HouseBlend extends Beverage {
    public HouseBlend() {
        description = "House Blend Coffee";
    }

    public double getCost() {
        return .89;
    }
}

class Mocha extends CondimentDecorator {
    Beverage beverage;

    public Mocha(Beverage beverage) {
        this.beverage = beverage;
    }

    public String getDescription() {
        return beverage.description + ", Mocha";
    }

    public double getCost() {
        return .20 + beverage.getCost(); 
    }
}

/**
 * Now you can do stuff like:
 * Beverage b1 = new Espresso(); --> simply creates an espresso
 * Beverage b2 = HouseBlend() 
 * b2 = new Mocha(b2); --> adds , Mocha and .20 to the HouseBlend() object dynamically
 * 
 * Your use of decorators will break if you want to write code for a concrete type like Espresso. 
 * The use of decorators should always be against the abstract Beverage type for it to work as 
 * expected. 
 * Note - Decorators are often created using other patterns like Factory or Builder, which creates 
 * robust decorators. 
 */

/**
 * The Factory Pattern
 * -------------------
 * 
 * There are other ways of instantiating objects than simple, public new statements, which may 
 * create problems. This pattern has to do with creating objects, and it may be very useful,
 * espcially in solving the problems we saw with the decorator pattern. 
 * We want to use interfaces, but the catch is that we have to use new to instantiate a concrete
 * class at some point, right? Even if it breaks one of the design principles. Let's go back
 * to our idea of seperate the parts which vary. For example - a pizza shop will have many
 * different types of pizzas, and clearly they are variable. 
 * 
 * Now, we are trying to encapsulate object creation i.e. we need to instantiate the right 
 * concrete class given the right conditions. The code which handles the creation of a pizza
 * will be moved to another object called Factory. 
 */

// A simple PizzaFactory 
/*
class SimplePizzaFactory {
    public Pizza createPizza(String type) {
        Pizza pizza = null;
        if (type.equals("cheese")) {
            pizza = new CheesePizza();
        } ...

        return pizza;
    }
}
*/

/**
 * Using the factory is simple, just create a factory reference and initialize it in the class's 
 * constructor and call the createPizza method. Right now, all you've done is move the code to
 * another class, but it still gives you some benefits, such as reusability of the factory in other
 * areas of the application. There's still more to come though. 
 * How can you "franchise" this pizza factory? We want to use the PizzaStore code (which initializes
 * the simple factory in the constructor), but we also want there to be certain additions you can 
 * make such as NYStylePizza or ChicagoStylePizza.
 * Well, we can simply get rid of all this factory pattern and create two different factories of styles
 * of pizza. 
 * 
 * NYPizzaFactory nyFactory = new NyPizzaFactory();
 * PizzaStore nyStore = new PizzaStore(nyFactory);
 * 
 * and so on
 * 
 * A better way of formulating the problem is that you'd like to standardize store and pizza creation,
 * but allow flexibility for differences in the pizza themselves. You could make createPizza an 
 * abstract method such that every subclass must re-implement it. Thus, we're gonna have NYPizzaStore, 
 * ChicagoPizzaStore, .... With this, the factory remains consistent, but we'll have different 
 * subclasses of PizzaStore which will override the createPizza method. From the point of view of 
 * the orderPizza function, there a lot of decoupling because it has no idea which pizza is coming into
 * it, as the style of pizza is created in the store subclasses. 
 * 
 * In other words, what the factory pattern really does, is handles object creation and encapsulates
 * it in a concrete subclass. So, with our implementation, we order a pizza like this: 
 * PizzaStore ny = new NyPizzaStore();
 * ny.orderPizza("cheese");
 * Inside the orderPizza function, the if block for cheese runs, and we get
 * Pizza pizza = createPizza("cheese"), which returns a NyCheesePizza
 * 
 * We can make Pizza itself an abstract class, which the concrete child classes which inherit
 * (such as NyCheesePizza). You can override the cut/bake/whatever functions in the child 
 * classes if you want the pizza to be different from default behavior; for example, if 
 * a particular pizza subclass wants the pizza to be cut into squares, which is different 
 * from the default behavior. 
 */

/**
 * Finally, we're ready for the official factory pattern! The creator method/class should never 
 * know what concrete class is being creator for you to reap the benefits of this pattern. You
 * can also think of this as parallel class hierarchies. The Store and Product are both abstract 
 * and are extended by a bunch of concrete classes, such as ChicagoStore and ChicagoDeepDishPizza for 
 * example. All products must implement the interface so classes which use products can simply 
 * refer to the interface rather than the concrete class. A class having to depend on many concrete 
 * classes is bad design! Object instantiation is a dependency. 
 * 
 * Design principle: Depend on abstractions, not concrete classes
 * This will allow you use dependency inversion principle: instead of 
 * A -> B; A -> C;... we will have A <- B; A <- C;....
 * A high level component is one that is composed of many low level components. Both should depend
 * on abstractions. 
 * 
 * Here are a few tips:
 *  1. Don't hold references to concrete class: you're depending on it! Move it to a factory.
 *  2. No class should derive from a concrete type: derive from an interface or abstraction
 *  3. Implemented methods in the base class shouldn't be overriden. This makes sense because
 *     if you're overriding it, it doesn't make sense to put it in the base class. However, I 
 *     have a confusion about this. What if only one subclass wants to override it and the other 
 *     99 don't (kind of like the "cut" method described above)? In my personal opinion, that would
 *     be okay, but I guess we will find out soon. 
 * 
 * The book does address this question by saying that these are guildelines and not rules. Use 
 * your own judgement! Moving on with the pizza franchise, what if you want to implement 
 * ingredients too, but you want it to be standardized. Not only that, you know that one 
 * ingredient may be used differently in a different region i.e. same component, different 
 * implementation. 
 */

/**
 * interface PizzaIngredientFactory {
        Dough createDough();
        Sauce createSauce();
        Cheese createCheese();
        Veggies[] createVeggies();
        Pepperoni createPepperoni();
        Clams createClams();
    }
 *
 * Thus, we're gonna create factories implementing this interface for each region, which'll
 * override all these methods. Then we will create the ingredient classes for each region.
 * Here's an example of NewYorkIngredients:
 * 
 * class NewYokIngredients implements PizzaIngredientFactory {
        Dough createDough() {
            return new ThinCrust();
        }

        Sauce createSauce() {
            return new MarinaSauce();
        }

        Cheese createCheese() {
            return new RegianoCheese();
        }

        Veggies[] createVeggies() {
            Veggies[] veggies = {new Onion(), new Tomato(), new Mushroom()};
            return veggies;
        }

        Pepperoni createPepperoni() {
            return new SlicedPepperoni();
        }

        Clams createClams() {
            return new FreshClams();
        }
 * }
 * 
 * With this, each franchise branch will be able to have different implementations of ingredients
 * if they want. For example, New York has fresh clams, but Chicago may not be able to get them. So
 * the ChicagoFactory will return FrozenClams(). This solidifies the benefit of interfaces and abstract
 * classes. Any client using the IngredientFactories will only need the interface: no implementation 
 * details required here!
 * 
 * To implement this into our existing pizza factory, we can add an abstract method, just like createPizza.
 * We already know that each concrete pizza type implements the Pizza interface, so it should override 
 * the prepare method. We will instantiate an Ingredient factory here and add it in the constructor. 
 * Since this derived class will inherit variables like dough, cheese, etc, we will save them and 
 * call the create functions for each. 
 * clam = ingredientFactory.createClam(), will return FrozenClam if the ingredientFactory is Chicago's
 * and fresh if the factory is New York's. The stores themselves don't require much changes; the only
 * thing is that each store will create the particular ingredient factory and pass it to the concrete
 * pizza class's constructor.
 * 
 * aaand we're done with the abstract factory pattern. There are differences between the factory 
 * pattern (one product) and the abstract factory pattern (families of products). Factory method
 * relies on inheritance: object creation is left to subclasses which implement the factory method.
 * Abstract factory uses object composition: these objects are created in the factory method of the 
 * abstract factory.  
 */