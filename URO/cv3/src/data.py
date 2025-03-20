import json
from typing import Optional


class PostalInfo:
    street: str
    streetNumber: str
    city: str
    postalCode: str

    def __init__(
        self,
        street: str = "",
        streetNumber: str = "",
        city: str = "",
        postalCode: str = "",
    ):
        self.street = street
        self.streetNumber = streetNumber
        self.city = city
        self.postalCode = postalCode

    def __str__(self):
        return f"street: {self.street}, streetNumber: {self.streetNumber}, city: {self.city}, postalCode: {self.postalCode}"

    def __iter__(self):
        return iter((self.street, self.streetNumber, self.city, self.postalCode))

    def toJson(self):
        json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def fromJson(data):
        if not data:
            return None

        return PostalInfo(
            data.get("street", ""),
            data.get("streetNumber", ""),
            data.get("city", ""),
            data.get("postalCode", ""),
        )


class ContactInfo:
    firstName: str
    lastName: str
    phoneNumber: str
    postalInfo: Optional[PostalInfo]
    birthCertificateNumber: str

    def __init__(
        self,
        firstName="",
        lastName="",
        phoneNumber="",
        birthCertificateNumber="",
        postalInfo: Optional[PostalInfo] = None,
    ):
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.postalInfo = postalInfo
        self.birthCertificateNumber = birthCertificateNumber

    def __str__(self):
        return f"firstName: {self.firstName}, lastName: {self.lastName}, phoneNumber: {self.phoneNumber}, postalInfo: {self.postalInfo}"

    def __iter__(self):
        tup = (
            self.birthCertificateNumber,
            self.firstName,
            self.lastName,
            self.phoneNumber,
        )
        tup += (*self.postalInfo,) if self.postalInfo else ()
        return iter(tup)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def fromJson(data: dict):
        return ContactInfo(
            data.get("birthCertificateNumber", ""),
            data.get("firstName", ""),
            data.get("lastName", ""),
            data.get("phoneNumber", ""),
            PostalInfo.fromJson(data.get("postalInfo")),
        )

    @staticmethod
    def sampleData():
        return [
            ContactInfo(
                "John",
                "Doe",
                "+1-555-1234",
                "123456789",
                PostalInfo("Main Street", "42", "New York", "10001"),
            ),
            ContactInfo(
                "Alice",
                "Smith",
                "+44-20-7946-0958",
                "987654321",
                PostalInfo("Baker Street", "221B", "London", "NW1 6XE"),
            ),
            ContactInfo(
                "Marie",
                "Curie",
                "+33-1-2345-6789",
                "111222333",
                PostalInfo("Rue de la Science", "7", "Paris", "75005"),
            ),
            ContactInfo(
                "Liam",
                "Johnson",
                "+1-617-555-7890",
                "444555666",
                PostalInfo("Boylston St", "500", "Boston", "02116"),
            ),
            ContactInfo(
                "Emma",
                "Williams",
                "+61-2-5551-4321",
                "777888999",
                PostalInfo("George St", "80", "Sydney", "2000"),
            ),
            ContactInfo(
                "Noah",
                "Davis",
                "+81-3-5555-6789",
                "123123123",
                PostalInfo("Shibuya", "15-7", "Tokyo", "150-0002"),
            ),
            ContactInfo(
                "Olivia",
                "Martinez",
                "+34-91-555-9876",
                "456456456",
                PostalInfo("Gran Via", "23", "Madrid", "28013"),
            ),
            ContactInfo(
                "James",
                "Taylor",
                "+1-415-555-2468",
                "789789789",
                PostalInfo("Market St", "870", "San Francisco", "94103"),
            ),
            ContactInfo(
                "Sophia",
                "Anderson",
                "+49-89-555-1357",
                "321321321",
                PostalInfo("Marienplatz", "1", "Munich", "80331"),
            ),
            ContactInfo(
                "Isabella",
                "Lopez",
                "+39-06-5555-8642",
                "987987987",
                PostalInfo("Via del Corso", "18", "Rome", "00186"),
            ),
            # No Postal Info
            ContactInfo("Tom", "Brown", "+49-30-1234567", "555666777"),
            ContactInfo("Mason", "Hernandez", "+55-11-5555-2468", "654654654"),
        ]
