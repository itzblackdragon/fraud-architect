from objects.person import Person
from random import randint

class Main:
    def run(self):        
        # Generate a list of persons
        persons = []
        for x in xrange(100):
            persons.append(Person())
            
        # Get the next one from the list
        person = persons.pop(0)
        
        # Industry research suggests 1% of all transactions are fraudulent.
        # For the sake of being able to find some needles in this haystack, 
        # let's bump that up to 10%.
        if randint(0,100) <= 10:
            pass
        
        
Main().run()