from objects.scheme import Scheme
from random import choice, randint
from faker import Faker

class Probing(Scheme):
    """
    Fraudsters will sometimes attempt to make surreptitious charges to a credit
    card just to see if it works, then follow it up with a large purchase if it does.
    
    http://ask.metafilter.com/155037/What-tipped-off-the-credit-card-company-for-fraud
    
    In this case we simulate someone doing the same thing with personal information
    as a precursor to some form of identity theft.
    
    Just to add entropy, it also simulates aborted attempts; i.e. "probes"
    that did not result in any completed mischief.
    """
    name = "Probing"
    
    # TODO: Thoroughly test this module
    
    def commit(self, history):
        # Choose a field to tamper with.
        victim = history[0]
        field = choice(["first_name", "last_name", "address", "city", choice(victim.mappings["email"])])
        
        # A minor change is always made-- can be in a variety of forms
        offset = self.make_minor_change(history, field)
        
        # The property may or may not be subsequently reset to its original value
        self.commit_value(history, offset, field)
        
        # A significant change to any number of fields may or may not be made afterward
        self.make_significant_change(history)
            
        return [field + " set for " + str(history[-1])]
    
    def make_minor_change(self, history, field):
        # Pick a random transaction that isn't toward the end of the history
        transaction = choice(history[:-3])
        offset = history.index(transaction)
        
        # Get the value of the property we're going to change
        string = str(transaction.__dict__[field])
        
        # Now, pick one:
        if randint(1,2) == 1:
            # Replace up to two letters/digits with another of same type
            for x in xrange(randint(1,2)):
                string = self.swap_characters(string)
        else:
            # Add up to two random letters or digits to the end
            for x in xrange(randint(1,2)):
                string = self.append_garbage(string)
            
        # Store the modified value back in the transaction
        transaction.__dict__[field] = string
            
        return offset
    
    def swap_characters(self, string):
        # Pick a random character index from string
        string = list(string)
        index = randint(0, len(string) - 1)
        
        if string[index].isalpha():
            # Replace it with another alpha char
            string[index] = Faker().random_letter().lower()
        else:
            # Replace it with a digit
            string[index] = Faker().random_digit()
            
        try:
            return "".join(str(s) for s in string)
        except TypeError as e:
            print e, string
            exit()
    
    def append_garbage(self, string):
        # If the last character is a letter, append a random letter
        if string[-1].isalpha():
            string = string + Faker().random_letter()
        else:
            # If the last character is a number, append a random number
            string = string + str(Faker().random_digit())
            
        return string
            
    def commit_value(self, history, offset, field):
        # Given the changed field at history[offset], apply the same change to
        # some subset of the history.
        subset = self.subset_history(history[offset:])
        
        tainted_transaction = history[offset]
        
        for transaction in subset:
            transaction.__dict__[field] = tainted_transaction.__dict__[field]
            
    def make_significant_change(self, history):
        # Time to do some damage.
        #
        # Determine how many modifications we're going to make for this transaction.
        passes = randint(1,4)
        
        # Pick a random transaction toward the end of the history.
        #
        # If we choose the 2nd or 3rd from the end, the subsequent transactions will
        # retain their original values and it will appear the fraudster tried to cover
        # their tracks by reverting the changes after the fact.
        #
        # If we end up choosing the final event, there is no room for additional 
        # changes.
        transaction = choice(history[-3:])
        
        for x in xrange(passes):
            transaction.change_random()