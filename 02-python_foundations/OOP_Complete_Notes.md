# Object-Oriented Programming in Python

> These notes were converted from the handwritten PDF. The explanations and examples preserve the source material, while the Python code has been normalized into valid syntax and consistent class naming.

## Table of Contents

1. [What Is Object-Oriented Programming?](#1-what-is-object-oriented-programming)
2. [What Is an Object?](#2-what-is-an-object)
3. [Classes and Instances](#3-classes-and-instances)
4. [Methods, Attributes, and `self`](#4-methods-attributes-and-self)
5. [The `__init__` Constructor](#5-the-__init__-constructor)
6. [The Four Core OOP Principles](#6-the-four-core-oop-principles)
7. [Inheritance](#7-inheritance)
8. [Polymorphism](#8-polymorphism)
9. [Quick Summary](#9-quick-summary)

---

## 1. What Is Object-Oriented Programming?

Object-oriented programming, or **OOP**, is a programming **paradigm**, meaning a coding style or a way of organizing a program.

Common programming paradigms include:

- **Procedural programming**
- **Object-oriented programming**
- **Functional programming**

### Procedural Programming

Procedural programming organizes a program as a **sequence of steps** or instructions.

```text
Input -> Step 1 -> Step 2 -> Step 3 -> Output
```

### Object-Oriented Programming

OOP organizes a program around **objects** and the interactions between them.

OOP can make code:

- Reusable
- Readable
- Maintainable
- Suitable for building larger packages and applications

In Python, everything is treated as an object, including:

- Lists
- Strings
- Tuples
- Dictionaries
- Numbers
- Functions
- Classes

---

## 2. What Is an Object?

An object consists of two main parts:

```text
Object = State + Behavior
```

### State

The state of an object is represented by its **attributes**, which are variables attached to the object.

Examples:

- A player's name
- A player's age
- A customer's balance
- An employee's job

### Behavior

The behavior of an object is represented by its **methods**, which are functions defined inside a class.

Examples:

- Setting a player's name
- Changing a player's position
- Displaying an employee greeting

### Encapsulation

**Encapsulation** means bundling data together with the code that operates on that data.

```text
Encapsulation = Data + Methods that operate on the data
```

For example, a `Player` object can store a player's name and also provide a method for changing that name.

---

## 3. Classes and Instances

A **class** is a blueprint or template used to create objects.

An **instance** is a specific object created from a class.

```text
Class -> Blueprint or template
Instance -> Object created from the class
```

### Creating an Empty Class

```python
class Player:
    pass
```

The `pass` statement is used when a class or function has no implementation yet.

### Creating Instances

```python
class Player:
    pass


p1 = Player()
p2 = Player()
```

Here:

- `Player` is the class.
- `p1` is one instance of `Player`.
- `p2` is another instance of `Player`.
- `p1` and `p2` are separate objects.

---

## 4. Methods, Attributes, and `self`

A method is a function defined inside a class.

```python
class Player:
    def set_name(self, name):
        self.name = name
```

### Understanding `self`

`self` refers to the current instance of the class.

It is conventionally used as the first parameter of every instance method.

```python
class Player:
    def set_name(self, name):
        self.name = name
```

In this example:

- `set_name()` is a method.
- `self` refers to the object calling the method.
- `name` is a value passed into the method.
- `self.name` creates or updates an attribute on the object.

> Python technically allows another parameter name instead of `self`, but using `self` is the standard and recommended convention.

### Using the Method

```python
class Player:
    def set_name(self, name):
        self.name = name


p1 = Player()
p1.set_name("Ahmed")

print(p1.name)
```

Output:

```text
Ahmed
```

The following method call:

```python
p1.set_name("Ahmed")
```

sets the object's attribute in a way conceptually similar to:

```python
p1.name = "Ahmed"
```

### Inspecting a Class with `dir()`

The built-in `dir()` function can be used to inspect the names available on a class or object, including its attributes and methods.

```python
print(dir(Player))
```

---

## 5. The `__init__` Constructor

The `__init__()` method is used to initialize data when an instance is created.

It is commonly called the class **constructor**, although technically Python creates the object before `__init__()` initializes it.

### Player Example

```python
class Player:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

Now data can be supplied while creating each instance:

```python
p1 = Player("Ahmed", 29)
p2 = Player("Anas", 5)
```

Each instance stores its own values:

```python
print(p1.name)
print(p1.age)

print(p2.name)
print(p2.age)
```

### Customer Example

```python
class Customer:
    def __init__(self, name, job, balance):
        self.name = name
        self.job = job
        self.balance = balance
```

Creating a customer:

```python
c1 = Customer("Abdo", "Engineer", 20_000)
```

Accessing the customer's attributes:

```python
print(c1.job)
print(c1.balance)
```

Output:

```text
Engineer
20000
```

The initialization code runs each time a new instance is created.

---

## 6. The Four Core OOP Principles

The notes identify four core principles of object-oriented programming.

| Principle | Meaning |
|---|---|
| **Encapsulation** | Combining data and the code that operates on it |
| **Inheritance** | Extending functionality from a parent class to child classes |
| **Polymorphism** | Providing a unified interface through methods with the same name |
| **Abstraction** | Working with an outer interface while hiding implementation details |

### 6.1 Encapsulation

Encapsulation bundles an object's data and behavior inside a class.

```python
class Customer:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def show_balance(self):
        print(self.balance)
```

The attributes and the methods that use them are grouped in one class.

### 6.2 Inheritance

Inheritance allows a child class to receive and extend functionality from a parent class.

```text
Parent class -> Existing functionality
Child class  -> Parent functionality + Additional functionality
```

### 6.3 Polymorphism

Polymorphism allows different classes to provide methods with the same name while implementing different behaviors.

```text
Same method name -> Different class-specific behavior
```

### 6.4 Abstraction

Abstraction means interacting with an object's visible interface while its internal implementation details remain hidden.

```text
Use the outer interface -> Hide internal details
```

---

## 7. Inheritance

The following parent class contains general player functionality.

```python
class Player:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def set_position(self, position):
        self.position = position

    def set_celebration(self, celebration):
        self.celebration = celebration
```

A child class can inherit from `Player` and add more attributes and methods.

```python
class AfricanPlayer(Player):
    def __init__(self, name, age, color, hair_style):
        super().__init__(name, age)
        self.color = color
        self.hair_style = hair_style

    def set_speed(self, speed):
        self.speed = speed
```

### Parent and Child Relationship

```text
Player
  |
  +-- AfricanPlayer
```

`AfricanPlayer` receives the parent class functionality:

- `name`
- `age`
- `set_position()`
- `set_celebration()`

It also adds its own functionality:

- `color`
- `hair_style`
- `set_speed()`

### Creating a Child-Class Instance

```python
player = AfricanPlayer(
    name="Ahmed",
    age=29,
    color="Brown",
    hair_style="Curly",
)

player.set_position("Forward")
player.set_celebration("Slide")
player.set_speed(90)
```

The parent constructor may also be called directly:

```python
Player.__init__(self, name, age)
```

However, `super().__init__(name, age)` is generally clearer and easier to maintain.

---

## 8. Polymorphism

In the following example, both classes define a method called `set_name()`, but each method accepts different data and performs different behavior.

### Player Class

```python
class Player:
    def set_name(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

        print(
            f"Name is set to {self.first_name} {self.last_name}"
        )
```

### Employee Class

```python
class Employee:
    def set_name(self, name):
        self.name = name
        print(f"Hello Mr. {self.name}")
```

### Using the Same Method Name

```python
p1 = Player()
e1 = Employee()

p1.set_name("Ahmed", "Mostafa")
e1.set_name("Ahmed")
```

Output:

```text
Name is set to Ahmed Mostafa
Hello Mr. Ahmed
```

Both objects provide a method called `set_name()`, but the implementation is specific to each class. This demonstrates a unified method interface with class-specific behavior.

---

## 9. Quick Summary

- OOP is a programming paradigm based on objects and their interactions.
- An object contains **state** and **behavior**.
- State is represented by attributes.
- Behavior is represented by methods.
- A class is a blueprint used to create instances.
- `self` refers to the current instance.
- `__init__()` initializes instance data.
- Encapsulation combines data with the methods that operate on it.
- Inheritance extends parent-class functionality in a child class.
- Polymorphism allows the same method name to represent different behaviors.
- Abstraction exposes an interface while hiding internal details.

---

## Complete Combined Example

```python
class Player:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def set_position(self, position):
        self.position = position

    def set_celebration(self, celebration):
        self.celebration = celebration

    def display(self):
        print(f"Player: {self.name}, Age: {self.age}")


class AfricanPlayer(Player):
    def __init__(self, name, age, color, hair_style):
        super().__init__(name, age)
        self.color = color
        self.hair_style = hair_style

    def set_speed(self, speed):
        self.speed = speed

    def display(self):
        print(
            f"Player: {self.name}, Age: {self.age}, "
            f"Color: {self.color}, Hair style: {self.hair_style}"
        )


player = AfricanPlayer(
    name="Ahmed",
    age=29,
    color="Brown",
    hair_style="Curly",
)

player.set_position("Forward")
player.set_celebration("Slide")
player.set_speed(90)
player.display()
```
