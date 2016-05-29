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
    
    def commit(self, victim):
        # Choose whether we're going to use a fraudulent email or password
        field = choice(["password", "email"])
        
        results = []
        if field == "password":
            victim.generate_password(choice(self.canned_values["password"]))
            results.append("Changed: " + field + " for " + str(victim))
        elif field == "email":
            # Get the name of an email field
            email_field = choice(victim.mappings["email"])
            results.append(victim.change(email_field, choice(self.canned_values["email"])))
            
        # Now we take a spin and see if we also want to modify the IP address
        if randint(0,3) == 3:
            ip_field = choice(victim.mappings["ip_address"])
            results.append(victim.change(ip_field, choice(self.canned_values["ip_address"])))
            
        return results