class calc:
    def add(self,a,b=0.,c=0):
        return a+b+c
c=calc()
print(c.add(10))
print(c.add(20,30))
print(c.add(50,60,80))