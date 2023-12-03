
class Value:
    def __init__(self, faceAmount, remainderAmount = 0.00):
        self.faceAmount = faceAmount
        self.trueAmount = faceAmount + remainderAmount

    def __repr__(self):
        # If the value's face amount is a whole number of dollars, display as an integer.
        if self.faceAmount == round(self.faceAmount, 0):
            return "$" + str(int(self.faceAmount))
        # Otherwise, round to the nearest cent.
        else:
            return "$" + str("{:.2f}".format(self.faceAmount))
    
    # Implement standard operations for dollar values.
    def __add__(self, other):
        self, other = Value.__check_type(self, other)
        full_add = self.trueAmount + other.trueAmount
        rounded = round(full_add, 2)
        return Value(rounded, full_add - rounded)
    def __sub__(self, other):
        self, other = Value.__check_type(self, other)
        return self + Value(-1 * other.trueAmount)
    def __mul__(self, other):
        self, other = Value.__check_type(self, other)
        full_m = self.trueAmount * other.trueAmount
        rounded = round(full_m, 2)
        return Value(rounded, full_m - rounded)
    def __truediv__(self, other):
        self, other = Value.__check_type(self, other)
        full_d = self.trueAmount / other.trueAmount
        rounded = round(full_d, 2)
        return Value(rounded, full_d - rounded)
    
    # Implement standard comparisons for dollar values.
    def __lt__(self, other):
        return self.trueAmount < other.trueAmount
    def __le__(self, other):
        return self.trueAmount <= other.trueAmount
    def __eq__(self, other):
        return self.trueAmount == other.trueAmount
    def __ne__(self, other):
        return self.trueAmount != other.trueAmount
    def __gt__(self, other):
        return self.trueAmount > other.trueAmount
    def __ge__(self, other):
        return self.trueAmount >= other.trueAmount
    
    # Check and modify types so that Values and basic numeric types can be operated on
    def __check_type(self, other):
        if type(self) != Value and type(other) != Value:
            self = Value(self)
            other = Value(other)
        elif type(self) != Value:
            self = Value(self)
        elif type(other) != Value:
            other = Value(other)
        return self, other