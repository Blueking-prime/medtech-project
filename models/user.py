#!/usr/bin/env python3
'''User module'''
import hashlib
from models.base import Base, datetime, timedelta, TIMESTAMP_FORMAT


class AlreadyExists(Exception):
    '''Raised if the item already exists'''

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class DoesNotExist(Exception):
    '''Raised if the item doesn't exist'''

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NoPermission(Exception):
    '''Raised if the user doesn't have the required permissions'''

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class User(Base):
    """ User class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        """
        super().__init__(*args, **kwargs)
        self._email = kwargs.get('_email')
        self._password = kwargs.get('_password')
        self.medication = kwargs.get('medication')
        self.role = kwargs.get('role')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.session_id = None
        self.reset_token = None

    @property
    def email(self) -> str:
        '''Getter of the email'''
        return self._email

    @email.setter
    def email(self, email: str):
        '''Setter of new email'''
        if len(User.search({'email': email})) > 0:
            raise AlreadyExists('This email is already in use')
        else:
            self._email = email

    @property
    def password(self) -> str:
        """ Getter of the password
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """ Setter of a new password: encrypt in SHA256
        """
        if pwd is None or type(pwd) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def update_medication(self, medication: dict, password: str):
        '''Sets the user's medication parameters

        template = {
            'drug_name': [
                'dose',
                'time between doses (hours)',
                'max total doses [optional]',
                'date medication was issued [optional]
            ],
        }
        '''
        if self.is_valid_password(password):
            if not self.medication:
                self.medication = dict()
            for k, v in medication.items():
                if v[3]:
                    date_issued = datetime.strptime(v[3], TIMESTAMP_FORMAT)
                else:
                    date_issued = datetime.utcnow()

                if v[2]:
                    end_date = date_issued + timedelta(
                            days=(int(v[1]) * int(v[2])/24)
                        )
                    max_doses = int(v[2])
                else:
                    end_date = None
                    max_doses = None

                self.medication.update({
                        k: {
                            'dose': int(v[0]),
                            'time_between_dosage': int(v[1]),
                            'max_doses': max_doses,
                            'date_issued': date_issued,
                            'end_date': end_date
                        }
                    })

            self.save()
        else:
            raise NoPermission()

    def remove_medication(self, drug_name: str, password: str):
        '''Removes a medication from the users medications'''
        try:
            if self.is_valid_password(password):
                self.medication.pop(drug_name)
            else:
                raise NoPermission
        except KeyError:
            raise DoesNotExist('This drug isn\'t part of the users medication')

    def is_valid_password(self, pwd: str) -> bool:
        """ Validate a password
        """
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        pwd_e = pwd.encode()
        return hashlib.sha256(pwd_e).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """ Display User name based on email/first_name/last_name
        """
        if self.email is None and self.first_name is None \
                and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)

    def to_json(self, for_serialization: bool = False) -> dict:
        '''Overloads to_json to convert med dates to serializable formats'''
        res_dict = super().to_json(for_serialization)
        for i in res_dict['medication']:
            date_issued = res_dict['medication'][i].get('date_issued')
            if type(date_issued) is datetime:
                res_dict['medication'][i]['date_issued'] = date_issued.strftime(TIMESTAMP_FORMAT)
            end_date = res_dict['medication'][i].get('end_date')
            if type(end_date) is datetime:
                res_dict['medication'][i]['end_date'] = end_date.strftime(TIMESTAMP_FORMAT)

        return res_dict


if __name__ == '__main__':
    user_email = "bob@hbtn.io"
    user_clear_pwd = "H0lbertonSchool98!"

    user = User(first_name='Mark', last_name='The Zuck')
    user.email = user_email
    user.password = user_clear_pwd
    print("New user: {}".format(user.id))
    print('Display name: {}'.format(user.display_name()))
    print('Hashed password: {}\n'.format(user.password))

    drug_template = {
            'Covid pill': [
                '2',
                '8',
                '9',
                ''
            ],
        }

    user.update_medication(drug_template, user_clear_pwd)
    print(user.to_json())
    print('--------------------------')
    print(user.__dict__)
    # user.save()

    # user_email = "braap@bop.mid"
    # user_clear_pwd = "H0ltryuhiop98!"

    # user = User(first_name='Tim', last_name='Cuck')
    # user.email = user_email
    # user.password = user_clear_pwd
    # print("New user: {}".format(user.id))
    # print('Display name: {}'.format(user.display_name()))
    # print('Hashed password: {}\n'.format(user.password))

    # print(user.to_json())

    # user.save()