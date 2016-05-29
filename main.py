from objects.person import Person
from random import randint, choice
from copy import copy
import csv

from schemes.disposable_email import DisposableEmail
from schemes.shared_property import SharedProperty

class Main:
    def setup(self):
        # Generate a list of persons
        self.persons = []
        for x in xrange(25):
            self.persons.append(Person())
            
        # Make a backup of original persons so we can emulate change
        # reversal later.
        self.original_persons = copy(self.persons)
        
        self.schemes = [
            DisposableEmail(),
            SharedProperty(),
        ]
    
    def run(self):
        print "Generating persons..."        
        self.setup()
        
        fieldnames = [x for x in self.persons[0].__dict__.keys() if x not in ["mappings", "generators", "faker"]]
        
        output_file = open('./resources/output.csv','wb')
        csvwriter = csv.DictWriter(output_file, delimiter=',', fieldnames=fieldnames, extrasaction='ignore')
        csvwriter.writeheader()
        
        transactions = 0
        while transactions < 10000:
            # Get the next one from the list
            person = self.persons.pop(0)
            
            # Industry research suggests 1% of all transactions are fraudulent.
            # If we roll greater than 1/100, emulate normal user behavior.
            if randint(0,100) > 0:
                # Let's assume users only make changes 25% of the time.
                if randint(0,100) < 25:
                    print person.change_random()
                else:
                    print person.change_nothing()
                    
            else:
                # We rolled less than 10/100.
                # Let's commit some fraud.
                scheme = choice(self.schemes)
                results = scheme.commit(person)
                for result in results:
                    print "FRAUD (" + scheme.name + "): " + result 
            
            # Update the timestamp
            # TODO: Does not update fast enough; results in a lot of duplicate TS
            person.generate_last_modified()
            
            # Write this transaction to file
            csvwriter.writerow(person.__dict__)
            
            # Put the person back in line
            self.persons.append(person)
            transactions += 1
        
Main().run()