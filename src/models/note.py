from src.database import Database
import uuid
import datetime


class Note(object):

    def __init__(self, title, content, author, created_date=None, _id=None):
        self.title = title
        self.content = content
        self.created_date = datetime.datetime.utcnow() if created_date is None else created_date
        self.author = author
        self._id = uuid.uuid4().hex if _id is None else _id

    def json_data(self):
        """method to build note attributes"""
        return {
            "title": self.title,
            "content": self.content,
            "created_date": self.created_date,
            "author": self.author,
            "_id": self._id
        }

    def save_to_mongo(self):
        """method to save created note to 'notes' collection"""
        Database.insert("notes", self.json_data())

    def update_mongo(self, match):
        """method to update a note"""
        Database.update("notes", match, {"$set": self.json_data()})

    @staticmethod
    def find_one(id):
        """method to find a note from the notes collection using the note id"""
        return Database.find_one("notes", {"_id": id})

    @staticmethod
    def find_all(author):
        """method to find all notes in the note collection that belongs to a particular author"""
        note_array = []
        note = Database.find("notes", {"author": author})
        # create and return an array of notes
        for i in note:
            note_array.append(i)
        return note_array

    @staticmethod
    def delete(id):
        """method to delete a note from the note collection using note id"""
        Database.delete("notes", {"_id": id})