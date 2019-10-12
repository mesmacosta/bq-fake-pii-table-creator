import random
from datetime import timedelta, datetime

import pandas as pd
from faker import Faker
from faker.providers import address
from faker.providers import automotive
from faker.providers import bank
from faker.providers import barcode
from faker.providers import company
from faker.providers import credit_card
from faker.providers import date_time
from faker.providers import internet
from faker.providers import geo
from faker.providers import job
from faker.providers import person
from faker.providers import ssn

from .uuid_helper import UUIDHelper


class DFCreator:

    def __init__(self,
                 name=None,
                 num_rows=None,
                 num_cols=None,
                 obfuscate_col_names=None):
        self.__fake = self.__init_faker()
        self.__data_functions = self.__init_fake_data_functions()
        self.__name = name
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__obfuscate_col_names = obfuscate_col_names

    def first_name_and_gender(self):
        g = 'M' if random.randint(0, 1) == 0 else 'F'
        n = self.__fake.first_name_male() if g == 'M' else self.__fake.first_name_female()
        return {'gender': g, 'first_name': n}

    def birth_and_start_date(self):
        sd = self.__fake.date_between(start_date='-20y', end_date='now')
        delta = timedelta(days=365 * random.randint(18, 40))
        bd = sd - delta

        return {'birth_date': bd.strftime('%m/%d/%Y'), 'start_date': sd.strftime('%m/%d/%Y')}

    def title_office_org_salary_bonus(self):
        position = self.title_office_org()
        title_and_salary_range = {'Engineer': [90, 120], 'Senior Engineer': [110, 140],
                                  'Manager': [130, 150], 'Associate': [60, 80], 'VP': [150, 250]}
        salary_range = title_and_salary_range[position['title']]

        salary = round(random.randint(1000 * salary_range[0], 1000 * salary_range[1]) / 1000) * 1000
        bonus_ratio = random.uniform(0.15, 0.2)
        bonus = round(salary * bonus_ratio / 500) * 500
        position.update({'salary': salary, 'bonus': bonus})
        return position

    def create(self):
        randomized_set = set()

        generators_limit = len(self.__data_functions.keys())

        num_cols = self.__num_cols if self.__num_cols \
            else random.randint(5, generators_limit)

        if num_cols > generators_limit:
            num_cols = generators_limit

        while len(randomized_set) < num_cols:
            randomized_set.add(random.choice(list(self.__data_functions.items())))

        num_rows = self.__num_rows if self.__num_rows \
            else random.randint(500, 10000)

        rows = []
        keys = [list(func().keys()) for _, func in randomized_set]
        flattened_keys = [y for x in keys for y in x]
        for _ in range(num_rows):
            deep_list = []
            for _, func in randomized_set:
                dict_item = func()
                deep_list.append(list(dict_item.values()))

            row = [item for sublist in deep_list for item in sublist]
            rows.append(row)

        dataframe = pd.DataFrame(rows)

        df_cols = []
        if self.__obfuscate_col_names:
            for i in range(len(flattened_keys)):
                df_cols.append(f'col_{i}')
        else:
            df_cols = flattened_keys

        dataframe.columns = df_cols

        random_company_name = self.__fake.bs().replace(' ', '_'). \
            replace('-', '_').replace(',', '_').lower()

        name = self.__name if self.__name \
            else f'org_{random_company_name}_{UUIDHelper.generate_uuid()}'

        return name, dataframe

    @classmethod
    def birth_and_start_date_on_windows(cls):
        bd = datetime(1960, 1, 1) + timedelta(
            seconds=random.randint(0, 1261600000))  # 40 year time delta
        earliest_start_date = bd + timedelta(seconds=random.randint(0, 567720000))  # earliest start
        # date is 18 years after birth
        latest_start_date = datetime.now()

        delta = latest_start_date - earliest_start_date
        delta_in_seconds = delta.days * 24 * 60 * 60 + delta.seconds
        random_second = random.randint(0, delta_in_seconds)
        return {'birth_date': bd.strftime('%m/%d/%Y'),
                'start_date': (bd + timedelta(seconds=random_second)).strftime('%m/%d/%Y')}

    @classmethod
    def title_office_org(cls):
        # generate a map of real office to fake office
        offices = ['New York', 'Austin', 'Seattle', 'Chicago']
        # codify the hierarchical structure
        allowed_orgs_per_office = {'New York': ['Sales'],
                                   'Austin': ['Devops', 'Platform', 'Product', 'Internal Tools'],
                                   'Chicago': ['Devops'], 'Seattle': ['Internal Tools', 'Product']}
        allowed_titles_per_org = {
            'Devops': ['Engineer', 'Senior Engineer', 'Manager'],
            'Sales': ['Associate'],
            'Platform': ['Engineer'],
            'Product': ['Manager', 'VP'],
            'Internal Tools': ['Engineer', 'Senior Engineer', 'VP', 'Manager']
        }

        office = random.choice(offices)
        org = random.choice(allowed_orgs_per_office[office])
        title = random.choice(allowed_titles_per_org[org])
        return {'office': office, 'title': title, 'org': org}

    @classmethod
    def salary_and_bonus(cls):
        salary = round(random.randint(90000, 120000) / 1000) * 1000
        bonus_ratio = random.uniform(0.15, 0.2)
        bonus = round(salary * bonus_ratio / 500) * 500
        return {'salary': salary, 'bonus': bonus}

    @classmethod
    def __init_faker(cls):
        fake = Faker()
        fake.add_provider(automotive)
        fake.add_provider(bank)
        fake.add_provider(barcode)
        fake.add_provider(geo)
        fake.add_provider(person)
        fake.add_provider(internet)
        fake.add_provider(ssn)
        fake.add_provider(address)
        fake.add_provider(job)
        fake.add_provider(date_time)
        fake.add_provider(company)
        fake.add_provider(credit_card)
        return fake

    def __init_fake_data_functions(self):
        data_functions = dict()
        data_functions['first_name_and_gender'] = self.first_name_and_gender
        data_functions['last_name'] = lambda: {'last_name': self.__fake.last_name()}
        data_functions['personal_email'] = lambda: {'email': self.__fake.email()}
        data_functions['company_email'] = lambda: {'company_email': self.__fake.company_email()}

        # > Internet
        data_functions['user_name'] = lambda: {'user_name': self.__fake.user_name()}
        data_functions['hostname'] = lambda: {'hostname': self.__fake.hostname()}
        data_functions['ipv4_private'] = lambda: {'ipv4_private': self.__fake.ipv4_private()}
        data_functions['ipv6'] = lambda: {'ipv6': self.__fake.ipv6()}
        data_functions['uri'] = lambda: {'uri': self.__fake.uri()}
        data_functions['image_url'] = lambda: {'image_url': self.__fake.image_url()}
        data_functions['mac_address'] = lambda: {'mac_address': self.__fake.mac_address()}
        # Internet <

        data_functions['bban'] = lambda: {'bban': self.__fake.bban()}
        data_functions['iban'] = lambda: {'iban': self.__fake.iban()}

        data_functions['barcode'] = lambda: {'barcode': self.__fake.ean()}

        data_functions['coordinate'] = lambda: {'coordinate': self.__fake.coordinate()}
        data_functions['latitude'] = lambda: {'latitude': self.__fake.latitude()}
        data_functions['longitude'] = lambda: {'longitude': self.__fake.longitude()}

        data_functions['license_plate'] = lambda: {'license_plate': self.__fake.license_plate()}
        data_functions['ssn'] = lambda: {'ssn': self.__fake.ssn()}
        data_functions['birth_and_start_date'] = self.birth_and_start_date
        data_functions['title_office_org_salary_bonus'] = self.title_office_org_salary_bonus
        data_functions['accrued_holidays'] = lambda: {'accrued_holiday': random.randint(0, 20)}
        data_functions['credit_card_number'] = lambda: {
            'credit_card_number': self.__fake.credit_card_number()}
        data_functions['credit_card_expire'] = lambda: {
            'credit_card_expire': self.__fake.credit_card_expire()}
        data_functions['credit_card_security_code'] = lambda: {
            'credit_card_security_code': self.__fake.credit_card_security_code()}
        return data_functions
