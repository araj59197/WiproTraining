from abc import ABC, abstractmethod


class BANK(ABC):
    @abstractmethod
    def interest(self):
        pass

    @abstractmethod
    def loan(self):
        pass


class SBI(BANK):
    def interest(self):
        print("SBI interest is 6%")

    def loan(self):
        print("SBI loan is 10%")


s = SBI()
s.interest()
s.loan()
