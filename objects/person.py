from faker import Faker
from datetime import datetime, timedelta
import hashlib
from copy import copy
from random import choice

class Person:
    def __repr__(self):
        # Return some identifier that this is a Person object
        return "<Person: " + self.first_name + " " + self.last_name + ">"
    
    def __str__(self):
        return self.__repr__()
    
    def generate_first_name(self):
        if self.gender == "F":
            return self.faker.first_name_female()
        else:
            return self.faker.first_name_male()
        
    def generate_password(self, password=None):
        if not password:
            self.password = self.faker.password()
        else:
            self.password = password
        self.password_hash = hashlib.sha256(self.password).hexdigest()
        return self.password
    
    def generate_password_hash(self):
        self.password = self.faker.password()
        self.password_hash = hashlib.sha256(self.password).hexdigest()
        return self.password_hash
    
    def generate_last_modified(self):
        date = datetime.now()
        self.last_modified = date.strftime('%m/%d/%Y %H:%M:%S')
        self.last_modified_8601 = date.strftime('%Y-%m-%d %H:%M:%S')
        
    def generate_gender(self):
        return self.faker.random_element(["M", "F"])
    
    def generate_optional_phone(self):
        return self.faker.random_element([self.faker.phone_number(), ""])
    
    def generate_username(self):
        return (self.first_name[0] + self.last_name + self.faker.zipcode()[:3]).lower()
    
    def generate_home_email(self):
        return self.username + "@" + self.faker.free_email_domain()
    
    def generate_work_email(self):
        return self.username + "@" + self.faker.company_email().split("@")[1]

    def __init__(self):
        self.faker = Faker()
        
        self.generators = {
            "gender": self.generate_gender,
            "first_name": self.generate_first_name,
            "last_name": self.faker.last_name,
            "address": self.faker.street_address,
            "city": self.faker.city,
            "state": self.faker.state_abbr,
            "zip": self.faker.zipcode,
            "ip_address": self.faker.ipv4,
            "employee_id": self.faker.uuid4,
            "company": self.faker.company,
            "position": self.faker.job,
            "password": self.generate_password,
            "password_hash": self.generate_password_hash,
            "work_phone": self.generate_optional_phone,
            "home_phone": self.faker.phone_number,
            "cell_phone": self.generate_optional_phone,
            "username": self.generate_username,
            "home_email_address": self.generate_home_email,
            "work_email_address": self.generate_work_email,
            "last_modified": self.generate_last_modified,
        }
        
        self.mappings = {
            "email": ["home_email_address", "work_email_address"],
            "ip_address": ["ip_address"],
        }
        
        self.gender = self.generators["gender"]()
        self.ssn = self.faker.ssn()
        
        for k in self.generators.keys():
            setattr(self, k, self.generators[k]())
        
        # Format the creation date in the most useless format imaginable
        # since most applications will export it this way.
        date = self.faker.date_time_this_century()
        delta = self.faker.random_element([5, 10, 25, 50, 75, 100, 150, 300])
        last_modified = date + timedelta(days=delta, minutes=delta, seconds=delta)
        
        self.create_date = date.strftime('%m/%d/%Y %H:%M:%S')
        self.last_modified = last_modified.strftime('%m/%d/%Y %H:%M:%S')
        
        # But also present it in 8601 format in case you have intelligent
        # application logs
        self.create_date_8601 = date.strftime('%Y-%m-%d %H:%M:%S')
        self.last_modified_8601 = last_modified.strftime('%Y-%m-%d %H:%M:%S')
        
    def change(self, field, value=None):
        if not value:
            if field in self.generators.keys():
                setattr(self, field, self.generators[field]())
        else:
            setattr(self, field, value)
        return "Changed: " + field + " for " + str(self)
        
    def change_random(self):
        random_field = choice(self.generators.keys())
        self.change(random_field)
        return "Changed: " + random_field + " for " + str(self)
    
    def change_nothing(self):
        return "Changed: nothing for " + str(self)