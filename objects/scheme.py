from random import randint

class Scheme:
    
    name = "Generic Scheme"
    
    def commit(self, victim, history):
        """
        This function must be overridden by child classes.
        """
        print self.name, "was activated but is not configured to perform any action!"
        
    def subset_history(self, history):
        # Set it for some subset of the history
        start = randint(0, len(history))
        end = randint(start, len(history))
        
        return history[start:end]
    
    def display_history(self, history):
        fieldnames = [x for x in self.persons[0].__dict__.keys() if x not in ["mappings", "generators", "faker"]]
        
        for event in history:
            print event.__dict__