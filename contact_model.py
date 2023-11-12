from mongoengine import Document, StringField, BooleanField, connect, disconnect
from faker import Faker

fake = Faker('uk_UA')

disconnect()  # Роз'єднати будь-яке існуюче з'єднання перед підключенням знову

connect(db="hw8_web", host="mongodb+srv://user_hw8:567234@cluster0.yncml3w.mongodb.net/?")

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    address = StringField()
    phone = StringField()
    is_message_sent = BooleanField(default=False)
    
    meta = {'collection': 'contacts'}

    @classmethod
    def create_fake_contact(cls):
        return cls(
            full_name=fake.name(),
            email=fake.email(),
            address=fake.address(),
            phone=fake.phone_number()
        )

