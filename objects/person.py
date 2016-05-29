from faker import Faker
from datetime import timedelta
import hashlib
from copy import copy

class Person:
    def __repr__(self):
        # Return some identifier that this is a Person object
        return "<Person: " + self.first_name + " " + self.last_name + ">"
        
    def __init__(self):
        faker = Faker()
        
        # --- Static properties ---
        self.gender = faker.random_element(["M", "F"])
        if self.gender == "F":
            self.first_name = faker.first_name_female()
        else:
            self.first_name = faker.first_name_male()
        self.last_name = faker.last_name()
        self.ssn = faker.ssn()
        self.address = faker.street_address()
        self.city = faker.city()
        self.state = faker.state_abbr()
        self.zip = faker.zipcode()
        self.ip_address = faker.ipv4()
        self.employee_id = faker.uuid4()
        self.company = faker.company()
        self.position = faker.job()
        
        # SHA won't match password, but that should be ok for this purpose
        self.password = faker.password()
        self.password_hash = hashlib.sha256(self.password).hexdigest()
        
        self.work_phone = faker.random_element([faker.phone_number(), ""])
        self.home_phone = faker.phone_number()
        self.cell_phone = faker.random_element([faker.phone_number(), ""])
        
        # --- Dynamic properties ---
        self.username = (self.first_name[0] + self.last_name + faker.zipcode()[:3]).lower()
        
        # Format the creation date in the most useless format imaginable
        # since most applications will export it this way.
        date = faker.date_time_this_century()
        delta = faker.random_element([5, 10, 25, 50, 75, 100, 150, 300])
        last_modified = date + timedelta(days=delta, minutes=delta, seconds=delta)
        
        self.create_date = date.strftime('%m/%d/%Y %H:%M:%S')
        self.last_modified = last_modified.strftime('%m/%d/%Y %H:%M:%S')
        
        # But also present it in 8601 format in case you have intelligent
        # application logs
        self.create_date_8601 = date.strftime('%Y-%m-%d %H:%M:%S')
        self.last_modified_8601 = last_modified.strftime('%Y-%m-%d %H:%M:%S')
        
        self.home_email_address = self.username + "@" + faker.free_email_domain()
        self.work_email_address = self.username + "@" + faker.company_email().split("@")[1]