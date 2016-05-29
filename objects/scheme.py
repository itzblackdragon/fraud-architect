class Scheme:
    
    name = "Generic Scheme"
    
    def commit(self, victim):
        """
        This function must be overridden by child classes.
        """
        print self.name, "was activated but is not configured to perform any action!"