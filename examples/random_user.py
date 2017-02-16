from typing import List

import pyasq


class Name:
    first: str
    last: str


class Person:
    gender: str
    name: Name


class Result:
    results: List[Person]


@pyasq.api('https://randomuser.me/api')
class RandomUser:

    @pyasq.endpoint('/')
    def user(self) -> Result:
        pass


def demonstrate():
    user = RandomUser().user.get().results[0]
    print(user.gender)  # e.g. 'female'
    print(user.name.first)  # e.g. 'roëlle'


if __name__ == '__main__':
    demonstrate()
