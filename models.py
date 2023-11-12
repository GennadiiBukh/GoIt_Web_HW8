from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE, disconnect

disconnect()  # Роз'єднати будь-яке існуюче з'єднання перед підключенням знову

connect(db="hw8_web", host="mongodb+srv://user_hw8:567234@cluster0.yncml3w.mongodb.net/?")


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)
