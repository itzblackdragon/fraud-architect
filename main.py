from objects.transaction import Transaction
from random import randint, choice
from copy import copy
import csv

from schemes.disposable_email import DisposableEmail
from schemes.shared_property import SharedProperty
from schemes.probing import Probing

class Main:
    def setup(self):
        # Generate a list of persons
        self.persons = []
        for x in xrange(25):
            self.persons.append(Transaction())
        
        self.schemes = [
            DisposableEmail(),
            SharedProperty(),
            Probing(),
        ]
    
    def run(self):
        print "Generating persons..."        
        self.setup()
        
        fieldnames = [x for x in self.persons[0].__dict__.keys() if x not in ["mappings", "generators", "faker"]]
        
        output_file = open('./output/consumer_data.csv','wb')
        csvwriter = csv.DictWriter(output_file, delimiter=',', fieldnames=fieldnames, extrasaction='ignore')
        csvwriter.writeheader()
        
        transactions = 0
        while transactions < 10000:
            # Get the next one from the list
            person = self.persons.pop(0)
            
            # Generate a random number of transactions for this person.
            history = []
            next_transaction = copy(person)
            for x in xrange(randint(5,20)):
                transaction = copy(next_transaction)
                
                # Let's assume users only make changes 25% of the time.
                if randint(0,100) < 25:
                    print transaction.change_random()
                else:
                    transaction.change_nothing()
                
                transaction.generate_last_modified()
                history.append(transaction)
                next_transaction = copy(transaction)
                
            # Industry research suggests 1% of all transactions are fraudulent.
            if randint(0,100) < 5:
                # Let's commit some fraud.
                # Pick a scheme.
                scheme = choice(self.schemes)
                results = scheme.commit(history)
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