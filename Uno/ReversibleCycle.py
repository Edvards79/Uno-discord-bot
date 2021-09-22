from Uno.rules import RULES

class ReversibleCycle:
    """
    A class to represent cycle that can be reversed and cycled over infinitely
    ...
    Attributes
    ----------
    items : list
        list of items
    pos : int
        current position in the reversible cycle
    reversed : bool
        whether the cycle is reversed
    
    Methods
    -------
    reverse()
        Reverses the direction of the cycle
    """

    def __init__(self, items=None):
        """
        Parameters
        ----------
        items : list, optional
            list of items
        """
        if items is None:
            items = []

        self.items = items
        self.pos = 0
        self.reversed = False
    
    def reverse(self):
        """Reverses the direction of the cycle"""

        self.reversed = not self.reversed
    
    def get_current(self):
        """Returns the current item"""

        if not self.items: return None
        return self.items[self.pos]
    
    def __next__(self):
        delta = -1 if self.reversed else 1
        self.pos += delta
        if self.reversed:
            if self.pos == -1: self.pos = len(self.items) - 1
        else:
            if self.pos >= len(self.items): self.pos = 0
        
        return self.items[self.pos]