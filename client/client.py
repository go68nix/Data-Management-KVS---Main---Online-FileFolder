import http.client
import json


class Client():

    def __init__(self, connection, user_id):
        self.conn = connection
        self.user_id = user_id

    # make json request to server
    def json_request(self, method, path, body):
        self.conn.request(method, path, json.dumps(body), headers={
                          "Content-Type": "application/json"})
        flask_response = self.conn.getresponse()
        return flask_response.read().decode()

####################################################
# TODO: implement CRUD like operations in client   #
####################################################

    def put(self, key, content):
        """
        Upsert (key, content) tuple into the file folder.
        Return the server response
        """
        body = {"uid": self.user_id, "content": content}
        return self.json_request("POST", f"/{key}", body)

    def read(self, key):
        """
        Retrieve the file-content associated with the given key owned by the user.
        Return the server response
        """
        body = {"uid": self.user_id}
        return self.json_request("GET", f"/{key}", body)

    def remove(self, key):
        """
        Remove the file-content associated with the given key owned by the user.
        Return the server response
        """
        body = {"uid": self.user_id}
        return self.json_request("DELETE", f"/{key}", body)

    def list(self):
        """
        List all file-content owned by the user.
        Return the server response
        """
        body = {"uid": self.user_id}
        return self.json_request("GET", "/", body)

####################################################
# TODO end                                         #
####################################################


def example_use():
    # establish connection
    conn = http.client.HTTPConnection("127.0.0.1", 8080)

    # set user for DB
    client = Client(conn, 0)

    # example usage
    print("Posting elements ...")
    client.put("PGDP", "1.3")
    client.put("GDB", "1.0")
    client.put("GBS", "1.7")

    print("Listing elements ...")
    print(client.list())

    print("Getting an element ...")
    response = client.read("PGDP")
    print(response)

    print("Deleting GBS ...")
    response = client.remove("GBS")
    print(response)

    print("Getting GBS ...")
    response = client.read("GBS")
    print(response)

    # change user
    client = Client(conn, 1)
    print("Getting PGDP ...")
    response = client.read("PGDP")
    print(response)

    conn.close()
    pass


def client_prompt():
    # establish connection
    conn = http.client.HTTPConnection("127.0.0.1", 8080)
    print("Welcome to our new online database.")
    user_id = input("Please enter user id: ")

    client = Client(conn, user_id)

    greeting = f"""
Hello user {user_id}!"""

    options = """Choose from the following options:
  1. Set
  2. Read
  3. Delete
  4. List
  5. Exit"""

    print(greeting)

    while True:

        print()
        print(options)

        option = input("Enter option: ")
        if option == "1":
            key = input("Enter key: ")
            value = input("Enter value: ")
            print(client.put(key, value))
        elif option == "2":
            key = input("Enter key: ")
            print(client.read(key))
        elif option == "3":
            key = input("Enter key: ")
            print(client.remove(key))
        elif option == "4":
            print("Listing elements ...")
            print(client.list())
        elif option == "5":
            print("Goodbye!")
            conn.close()
            break
        else:
            print("Invalid option!")


if __name__ == "__main__":

    # example_use()
    client_prompt()
