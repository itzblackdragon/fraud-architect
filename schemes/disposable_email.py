from objects.scheme import Scheme
from random import choice, randint

class DisposableEmail(Scheme):
    """
    Simulate a user changing their email address to use
    a disposable email account.
    
    There is no legitimate need for this in most environments,
    and should be a dead giveaway something fraudulent is
    happening.
    """
    name = "Disposable Email"
    
    def __init__(self):
        """
        This is not a comprehensive list, but there are some
        regulars on it.
        """
        file = open('resources/disposable_email_blacklist.conf', 'r')
        blacklist = [line.rstrip() for line in file.readlines()]
        self.domains = blacklist
        
    def commit(self, victim, history):
        # Get a random email address field from the person
        field = choice(victim.mappings["email"])
        
        # Choose a disposable domain name
        domain = choice(self.domains)
        
        # Get the username
        username = victim.username
        
        # Make the address
        fake_address = username + "@" + domain
        
        subset = self.subset_history(history)
        for transaction in subset:
            setattr(transaction, field, fake_address)
        
        return [field + " set for " + str(history[-1])]