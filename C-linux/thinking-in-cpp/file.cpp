/**
 * Introduction to Objects 
 * -----------------------
 * 
 * What is abstraction anyways? Hiding the unnecesary information so you can focus more on the details 
 * of the problem. For example, C is an abstraction of assembly language. The author describes objects
 * in OOP as mini-problems. They have their own states and operations they can perform. All objects,
 * while being unique themselves, have a distinct type: the class. Objects of the same class should
 * be able to perform similar tasks, send similar messages, and should have some common distinctive
 * features/functions/interface. 
 * The interface itself is defined by the functions you define in the class. For example, a CoffeMug 
 * class has openLid(), closeLid() functions. For access control, C++ has three access modifiers i.e.
 * public, private, and protected. 
 * Car <>----- Engine               [Each Car has an Engine]
 * Inheritance doesn't have the flexibility that composition has because of compile time restrictions.
 * 
 * A derived type has all functions and variables of a base type (if not private). The derived 
 * class has the same interface as the base class, and thus it is the same type as its parent.
 * There are two ways to differentiate behavior in a child class: add new functions ("is-like-a") 
 * or override an existing function (if you have fully overridden all functions of the parent, this 
 * is a "is-a" relationship). The danger with adding functions is that your parent class may also 
 * need that new function. 
 * 
 * Interchangable objects with polymorphism. When you have code which references the base type
 * while creating objects, it won't get affected by the creation of new types, which is useful and 
 * prevents bugs not to mention being easier to write. An example, if there's a BirdController 
 * class which uses a base Bird class, it doesn't have to execute or know about a special type
 * of derived bird (Goose, Pidgeon, whatever). Polymorphism will run the right code by simply 
 * doing Bird bird = new Pidgeon(); bird.fly(); -> this is dynamic and will run the pidgeon's
 * specific fly function. OOP languages use late binding, so the compiler doesn't know which 
 * fly() function to call until runtime. In C++, you must use the virtual keyword to use this 
 * dynamicness.  
 * 
 * If we have a function which takes a Shape object, and you pass it a Triangle object (a child 
 * of the Shape class), the function will run the Traingle class's functions dynamically. This
 * is called upcasting. 
 * 
 * In C++, you can create objects on the stack (static, fast) or the heap (dynamic, more flexible).
 * Unlike C, there is no malloc in C++; instead, you use the new operator to do the mallocing, and 
 * call delete after you're done with the object. You don't need to do anything for stack objects,
 * as the deallocation is done automatically.  
 */