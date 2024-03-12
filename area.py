import multiprocessing
import time
import threading
import concurrent.futures
import random as rd


class Trapezoid:
    def __init__(self, trap=None):
        if trap is None:
            trap = [0, 0, 0]
        self.a = trap[0]
        self.b = trap[1]
        self.h = trap[2]

    def __str__(self):
        return 'ტოლფერდა ტრაპეციის დიდი ფუძეა -> {}, პატარა ფუძეა -> {}, ხოლო სიმაღლეა ->{}'.format(self.b, self.a,
                                                                                                    self.h)

    def area(self):
        return (self.a + self.b) / 2 * self.h

    def __lt__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() < other.area()
        return False

    def __eq__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() == other.area()
        return False

    def __ge__(self, other):
        if isinstance(other, Trapezoid):
            return not self.__lt__(other)
        return False

    def __add__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() + other.area()
        return -1

    def __sub__(self, other):
        if isinstance(other, Trapezoid) and self.__ge__(other):  # საკლები მეტი ან ტოლი უნდა იყოს
            return self.area() - other.area()
        return "გამოკლება შეუძლებელია"

    def __mod__(self, other):
        if isinstance(other, Trapezoid) and self.__ge__(other):
            return int(self.area() / other.area())  # დავალებაში გვჭირდება რამდენჯერ მოთავსდება, ამიტომ უნდა
            # გამოვიყენოთ / და არა %, ასევე გასაყობი მეტი ან ტოლი უნდა იყოს
        return "0-ჯერ მოთავსდება"


# creating rectangle class which is child of trapezoid
class Rectangle(Trapezoid):
    def __init__(self, re=None):
        super().__init__([re[0], re[0], re[1]])

    def __str__(self):
        return "მართკუთხედის სიმაღლეა -> {}, ხოლო სიგანე -> {}".format(self.a, self.h)


# creating square class which is child of rectangle
class Square(Rectangle):
    def __init__(self, re=None):
        super().__init__([re[0], re[0], re[0]])

    def __str__(self):
        return "კვადრატის გვერდია -> {}".format(self.a)


# functions to calculate generate areas
def trapezoid_area(arr):
    for i in arr:
        tr = Trapezoid(i)
        tr.area()
        # you can print here parameters if you want
        # print(tr, "ფართობით", tr.area())


def rectangle_area(arr):
    for i in arr:
        rc = Rectangle(i)
        rc.area()
        # you can print here parameters if you want
        # print(rc,"ფართობით",  rc.area())


def square_area(arr):
    for i in arr:
        sq = Square(i)
        sq.area()
        # you can print here parameters if you want
        # print(sq, "ფართობით", sq.area())


def regular(arr):
    start = time.perf_counter()

    trapezoid_area(arr)
    rectangle_area(arr)
    square_area(arr)

    finish = time.perf_counter()

    print('in general Finished in: ', round(finish - start, 2), 'second(s)')


# this function is used to calculate time to compute areas of 10000 trapezoid, rectangle and square using threads

def threads(arr):
    start1 = time.perf_counter()

    t1 = threading.Thread(target=trapezoid_area, args=(arr,))
    t1.start()
    t2 = threading.Thread(target=rectangle_area, args=(arr,))
    t2.start()

    t1.join()
    t2.join()

    finish1 = time.perf_counter()
    print('with threads Finished in: ', round(
        finish1 - start1, 2), 'second(s)')


# this function is used to calculate time to compute areas of 10000 trapezoid, rectangle and square using processes
def multiprocess(arr):
    start2 = time.perf_counter()

    p1 = multiprocessing.Process(target=trapezoid_area, args=(arr,))
    p2 = multiprocessing.Process(target=rectangle_area, args=(arr,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    finish2 = time.perf_counter()
    print('with pools Finished in: ', round(finish2 - start2, 2), 'second(s)')


def hybrid(arr):
    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Create 5 processes, each spawning 20 threads
        results = [executor.submit(hybrid_threading, arr) for _ in range(5)]

        # Wait for all processes to finish
        for _ in concurrent.futures.as_completed(results):
            pass

    finish = time.perf_counter()
    print('Hybrid Execution Finished in: ', round(finish - start, 2), 'second(s)')


def hybrid_threading(arr):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create 20 threads for each process
        results = [executor.submit(trapezoid_area, arr) for _ in range(20)]

        # Wait for all threads to finish
        for _ in concurrent.futures.as_completed(results):
            pass


if __name__ == "__main__":
    trapecoids = [[rd.randint(1, 200), rd.randint(
        1, 200), rd.randint(1, 200)] for _ in range(10000)]
    rectangles = [[rd.randint(1, 200), rd.randint(1, 200)] for _ in range(10000)]
    squares = [rd.randint(1, 200) for _ in range(10000)]

    print("Regular Execution:")
    regular(trapecoids)

    print("\nMultithreading Execution:")
    threads(trapecoids)

    print("\nMultiprocessing Execution:")
    multiprocess(trapecoids)

    print("\nHybrid Execution:")
    hybrid(trapecoids)
