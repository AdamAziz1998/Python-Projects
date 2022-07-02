class c:
    def f(self,x):
        print("abc", x)

    def g(self):
        x = 1
        self.f(x)
        print(1)


class_instance = c()
class_instance.g()