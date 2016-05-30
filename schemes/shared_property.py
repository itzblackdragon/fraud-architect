from objects.scheme import Scheme
from random import choice, randint

class SharedProperty(Scheme):
    """
    Fraudsters are lazy. When they take over multiple accounts,
    they will often re-use the same password, access from the
    same IP address or even use the same email address across them.
    """
    name = "Shared Property"
    
    def __init__(self):
        self.canned_values = {
            "password": ["dragon", "mustang", "harley"],
            "email": ["aladdinsane@outlook.com", "jeangenie@yahoo.com", "ziggystardust@gmail.com"],
            "ip_address": ["27.176.155.36", "73.154.116.207", "196.169.145.25"]
        }
    
    def commit(self, history):
        # Choose whether we're going to use a fraudulent email or password
        field = choice(["password", "email"])
        
        # Choose an email field from the mappings
        victim = history[0]
        email_field = choice(victim.mappings["email"])
        
        bad_password = choice(self.canned_values["password"])
        bad_email = choice(self.canned_values["email"])
        
        subset = self.subset_history(history)
        for transaction in subset:
            if field == "password":
                transaction.generate_password(bad_password)
            elif field == "email":
                transaction.change(email_field, bad_email)
            
        return [field + " set for " + str(history[-1])]