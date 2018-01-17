from src.database import Database
from src.models.note import Note
import uuid
from tabulate import tabulate


class User(object):

    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def json_data(self):
        """method to build user attributes"""
        return {
            "username": self.username,
            "password": self.password,
            "_id": self._id
        }

    def save_to_mongo(self):
        """method to save created user to 'users' collection """
        Database.insert("users", self.json_data())

    @classmethod
    def get_by_username(cls, name):
        """method to get a user instance using username"""
        user = Database.find_one("users", {"username": name})
        if user is not None:
            return cls(**user)

    def login(self, name, password):
        """method to authenticate user using username and password"""
        user = self.get_by_username(name)
        if user is not None:
            if user.password == password:
                print("You have successfully logged in")
                return user
        else:
            print("Error Occurred logging in, Check username and password")
            return None

    @staticmethod
    def register(name, password):
        """method to create user using name and password"""
        user = User(name, password)
        user.save_to_mongo()
        print("Account Created")
        # login user after creating account
        user.login(name, password)
        return user

    def read_data(self):
        """method to display notes of a particular user"""
        # get 2 instances of the note, 1 to be returned, the second to be modified for easy viewing for user
        note1 = Note.find_all(self.username)
        note2 = Note.find_all(self.username)

        if len(note2) != 0:
            # modifying note for ease of referencing by adding a s/n attribute
            num = 0
            for item in note2:
                num += 1
                item["S/N"] = num
            return_note = note2

            # modifying note for easy reading by viewer by changing id to serial number and shortening date
            num = 0
            for item in note1:
                num += 1
                item["_id"] = num
                item["created_date"] = str(item["created_date"]).split(" ")[0]
            print(tabulate(tabular_data=note1, headers="keys", tablefmt="rst"))

            return return_note
        else:
            print("Sorry, No Notes Found")

    def write_data(self):
        """method to create data for user"""
        title = input("Title: ")
        content = input("Content: ")
        author = self.username
        note = Note(title, content, author)
        note.save_to_mongo()
        print("\nEntry added to database")

    def edit_data(self):
        """method to edit title or content of a note"""
        note_list = self.read_data()
        if note_list is not None:
            try:
                num = int(input("Enter ID of Note to Edit: "))
                # get id from serial number
                for note in note_list:
                    if note["S/N"] == num:
                        id = note["_id"]

                # get note using id
                response = Note.find_one(id)
                note = Note(**response)

                # get key match that will be used for edit
                current_title = note.title
                current_content = note.content

                # prompt user to edit title or content
                ans = input("Edit\n1. Title\n2. Content\n")
                ans = ans.strip()

                # edit title or content based on user choice
                if ans == "1":
                    title = input("Enter new title: ")
                    note.title = title
                    note.update_mongo(match={"title": current_title})
                    print("Title successfully edited")
                elif ans == "2":
                    content = input("Enter new content: ")
                    note.content = content
                    note.update_mongo(match={"content": current_content})
                    print("Content successfully edited")
                else:
                    print("Invalid option selected")
            except:
                print("Error occurred during edit, check Id and try again")

    def delete_data(self):
        """method to delete note from database"""
        note_list = self.read_data()

        if note_list is not None:
            try:
                # prompt user for choice
                num = int(input("Enter Id of Note to Delete: "))

                # get id for note
                for note in note_list:
                    if note["S/N"] == num:
                        id = note["_id"]
                Note.delete(id)
                print("Entry has been deleted")
            except:
                print("Error occurred during delete, check Id and try again")
