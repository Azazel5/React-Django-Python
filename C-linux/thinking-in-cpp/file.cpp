#include <iostream>

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
 * 
 * Don't fall into "analysis paralysis" and not get any work done. There are things which don't 
 * reveal themselves until it's design time, coding time, or implementation time. Basically, all 
 * you need to know is:
 *     1. What are the objects?
 *     2. What are their interfaces?
 * 
 * There are five phases which the author recommends to answer the above stated questions. First
 * of all, as simple as it sounds, make a plan. "Getting right into coding" can be useful when you 
 * have a well-defined problem. Set up some milestones which will measure your progress. In this 
 * case, you'll also want to define a mission statement. This is equivalent to a "high level"
 * view of the project. From what I gather, this isn't the time to get bogged down by low level 
 * details like where to put the nav bar, what kind of styles you'll implement, but rather the 
 * core functionalities you'll wanna implement. The first phase is actually the system specification
 * and minute details, well-designed. The author says not to focus too much on designing the user/
 * system spec because they will usually change over time. 
 * 
 * Use cases are "scenarios" which may happen. While users interact with your app, what are the 
 * possible things that can happen/go wrong? This seems to be reminiscent of error handling. 
 * Remember: you'll get stuck if you get hell bent on perfecting the use case diagrams now
 * because you simply won't be able to find all of them; "everything will reveal itself with time".
 * Now comes phase 2, and this is where you'll define your classes, data structures, etc. If 
 * you're creating lots of classes, look at their names, their responsibilities, and how the 
 * classes are interacting with each other. 
 * 
 * The author recommends using a card based system to design your classes in this step and then
 * move onto describing them in terms of UML. You're done with phase 2 when you have described
 * the objects and their interfaces. 
 * 
 * Phase 3 is all about building the core functionality. Phase 3 and 4 (iterate the use cases)
 * aren't to be confused with a one time, big coding session to finish the app. Make each 
 * feature/use case an iteration, until all is done. One iteration = 2-3 weeks, One iteration =
 * one use case, by the end the system must be ready to go, tested, with one more feature than 
 * before. Finally, you evolve the app in phase 5, which can encompass everything from fixing 
 * bugs to "maintaining". 
 * 
 * The author then spends some time talking about the importance of testing: he believes that 
 * test driven development is the way to go. Integration tests are useful while adding use
 * cases, as the tests will holler at you if you break something. To put the point to bed, TDD
 * also forces you to think "outside your classes" and will reveal commanalities/other features
 * to you. 
 */

/**
 * Making & Using objects
 * ----------------------
 * 
 * Let's talk compilers versus interpreters. The transition from writing to executing is immediate.
 * For example, python is an interpreted language, which is why you don't build any executables or 
 * anything like Java/C++/C. On the other hand, compilers compile and create executables. Programs 
 * can be built and tested independently, debugging experience is better. 
 * 
 * When a C++ program is run, a preprocessor is run using preprocessor directives and then the compiler
 * starts parsing the language, by buiding trees of phrases. Then, a minor optimization later, the trees
 * are visited and each node is converted either to assembly or machine code (if assembly, the 
 * assembler is run). More optimizations and the linker will link all the object files into an 
 * executable. Another benefit of compiled programs == type checking. 
 * 
 * One thing that people who've experienced C before (like myself) face is namespaces; you simply
 * include the library and expect functions to be called, but that isn't how it works. You gotta
 * use namespaces and get to the function you want. This adds a new layer of protection so that 
 * function names and other stuff don't collide. 
 * 
 * It is reckless to use the using namespace in a header file. Be wary of how you use it, especially
 * in big projects/programs. 
 */

// String concatation
int string_example()
{
    std::cout << "I am too big for you"
                 "Cause I go on and on"
                 "very useful in cases where"
                 "you wanna break things up ;)"
              << std::endl;
}

/**
 * C++ supports string concatation by the + operator, which is what you used extensively in Java.
 * To do file IO,, you must include a library and use the ifstream or ofstream object. Getline is
 * a function which reads strings line by line (only terminating when a \n character is encountered).
 * You can add the contents of an entire file into one string: beware, this has certain use cases,
 * but it is bad in other scenarios.
 * Vectors are containers in C++ which dynamically determines memory. The vector class is a template
 * in that it can hold any type. Some useful functions to know are push_back, push_front, insert etc. 
 * You can index into or assign vectors just like you would with arrays. 
 */

/**
 * The C in C++
 * ------------
 * 
 * This chapter is just a big collection of existing C functionalities within C++, so I will
 * only list items which are new to me personally. 
 * 
 * Variable argument lists are represented as ... in C++. The book suggests for the readers to
 * wait until later in the book where better methods for specifying var args have been detailed.
 * C++ introduces the bool type which isn't there in C, which solely used 0 or 1 for that. A 
 * bad style is to convert a boolean value to and fro each other using the ++/-- operators. 
 * Specifiers take the 4 basic types available in C++ and expand them: the ones we're interested
 * in are long, short, unsigned, and signed. Here's the hierarchy for an int: short int -> int ->
 * long int. For floats, float -> double -> long double. Floats always have a sign. Unsigned 
 * ints have an extra bit to represent more (positive) numbers. 
 * 
 * Every element in your program has an address, which can be accessed using pointers. 
 * Memory is laid out in a contiguous manner, so int a and int b will be 4 bytes away from each
 * other. A pointer can point to any sort of type, so you have to define the kind of this it is 
 * pointing to. Note - if you have something like int *a, b, c, b and c will be normal ints.
 * Initialization at point of definition is a good rule. Why would you wanna proxy a variable 
 * with a pointer? Change outside objects from a function and for other clever programming 
 * techniques (very vague, book). 
 * 
 * Pass by reference is a new concept introduced in C++. Here's the traditional and new way:
 * Traditional:
 *     void func(int *ptr) {
 *      *ptr = 5;  
 *     }
 * 
 *     int ptr = 2;
 *     func(&ptr);
 * 
 * New:
 *      void func(int &ptr) {
 *       ptr = 5;
 *      }
 * 
 *      int ptr = 2;
 *      func(ptr);
 * 
 * You can think of this as just syntactic difference for now, but you'll learn later that 
 * there are some things you can achieve only with the reference way as compared to the 
 * traditional way. There's one more interesting type i.e. the void*, which can encompass
 * all kinds of variables, ints, strings, or whatever. You must cast the void pointer to 
 * a type to be able to dereference that. This type should be avoided because it generates
 * storage problems: the pointer will be able to be casted to doubles, shorts, etc. 
 * Const - you know this is never going to change; Volatile - you never know when this will
 * change
 * 
 * Casting is powerful, and you have obviously used it all the time since you've worked with
 * C. However, be wary while casting a smaller type to a larger type, as it will occupy more
 * memory than you accounted for and may overflow into some other data. This is particularly
 * the case when casting pointers. C style casts are actually a malpractice because casting
 * should be done in a limited way. In C++, you can do explicit casts by static_cast. 
 * Note - narrowing conversions are still dangerous regardless of whether you follow the C
 * or C++ style. 
 * Sizeof is actually an operator, not a function. If you're applying it to a type, you must
 * do sizeof(char), but if you're applying it to, say, int x, you will do sizeof x. The 
 * power of typedef in C comes when we're working with lots of structs. 
 * 
 * The enum keyword automatically enumerates list of identifiers you give it numbers like 0,
 * 1, 2, ... The idea of an enum is much less used in C++ because of the struct's jacked 
 * younger brother AKA the class. Remember that arrays are pointers, so if you're passing
 * an array to a function, it's akin to passing a pointer. Another reminder: all command line
 * arguments are character arrays; if you wanna change anything to anything, you're reponsible
 * for the conversions.
 * 
 * Pointers can be modified to point somewhere else, but array identifiers cannot. 
 * int* a;
 * double *b;
 * Assume you have initialized both. When you do a++ and b++, you will move a 4 bytes forward
 * and b 8 bytes forward.
 * 
 * Adding a debugging flag is a good choice because you can seperate out parts where you're 
 * debugging. It can be as simple as a plain boolean variable. It is also a good idea to 
 * write macros for print statements, which you'll do a lot while debugging. An excellent
 * example used in the book: #define PR(x) cout << #x " = " << x << "\n"; 
 * int a = 1;
 * P(a); -- this will simply do cout << "a = " << 1 << "\n"; Pretty nifty!
 * 
 * You can define pointers to functions like void (*funcptr)();
 * This is a pointer to a function which takes no argument and returns void. If you don't
 * add the parenthesis, it'll just be void *funcptr(); which is a function which returns 
 * a void* rather than a VARIABLE (pointer to a function). You can get quite complicated with
 * this. For example - you could have an array of pointers to functions. 
 * 
 * Makefiles - a simple example
 * hello.exe: hello.cpp
 *    g++ hello.cpp
 * 
 * Here, hello.exe is the target and hello.cpp is the dependency. Makefiles can also define a 
 * bunch of macros for effective string replacement. 
 */

// Pointer to function example
void func()
{
    std::cout << "Wassup" << std::endl;
}

int main()
{
    // Declare a pointer to function variable fp
    void (*fp)();
    // Assign it to a function
    fp = func;
    // Call the function by dereferencing the pointer first and then passing arguments (if any)
    (*fp)();
}
