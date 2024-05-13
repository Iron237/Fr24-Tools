class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

# 创建一个Person对象并调用greet方法
person = Person("John", 25)
person.greet()