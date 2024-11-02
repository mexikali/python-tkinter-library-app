import socket
import threading
from threading import *
from datetime import datetime

fileLock = threading.RLock()

def days_between_dates(date_str1, date_str2):
    # Convert date strings to datetime objects
    date_format = "%d.%m.%Y"
    date1 = datetime.strptime(date_str1, date_format)
    date2 = datetime.strptime(date_str2, date_format)

    # Calculate the difference in days
    delta = date2 - date1

    return delta.days

def readFiles(fileName):
    data_dict = {}
    data_list = []
    with fileLock:
        with open(fileName) as _file:
            lines = _file.readlines()

        for line in lines:
            data = line.strip().split(";")

            if fileName == "users.txt" or fileName == "books.txt":
                data_dict[data[0]] = data[1:]

            elif fileName == "operations.txt":
                data_list.append(data)

    if fileName == "operations.txt":
        return data_list

    return data_dict

def calculateStatistics(reportNo):

    books = readFiles("books.txt")
    operations = readFiles("operations.txt")

    # most rented books
    if reportNo == 1:
        rents = {}
        for operation in operations:
            if operation[0] == "rent":
                for i in operation[4:]:
                    if rents.get(i) is None:
                        rents[i] = 1
                    else:
                        rents[i] += 1

        max_value = max(rents.values())
        max_ids = [k for k, v in rents.items() if v == max_value]
        msg = "report1"
        for i in max_ids:
            msg = msg + ";" + books[i][0]

        return msg

    # which librarian has the highest number of operations
    elif reportNo == 2:
        librarians = {}
        for operation in operations:
            current = operation[1]
            if librarians.get(current) is None:
                librarians[current] = 1
            else:
                librarians[current] += 1

        max_value = max(librarians.values())
        max_ids = [k for k, v in librarians.items() if v == max_value]
        msg = "report2"
        for i in max_ids:
            msg = msg + ";" + i

        return msg

    # what is the total generated revenue by the library
    elif reportNo == 3:

        returnOP = []
        rentOP = []
        for operation in operations:
            if operation[0] == "rent":
                rentOP.append(operation)
            elif operation[0] == "return":
                returnOP.append(operation)

        total = 0

        for i in rentOP:

            rented_books = i[4:]
            rented_date = i[3]
            renter1 = i[2]

            for j in returnOP:

                numberOfDays = days_between_dates(rented_date, j[3])
                returnedBookIDs = j[5:]
                renter2 = j[2]

                if any(element in returnedBookIDs for element in rented_books) and numberOfDays > 0 and renter1 == renter2:

                    bookIDs = set(rented_books).intersection(returnedBookIDs)
                    total += float(j[4])
                    rented_books = [i for i in rented_books if i not in bookIDs]

                    if len(rented_books) == 0:
                        break

        return "report3;" + str(total)


    # what is the average rental period for the "Harry Potter" book?
    elif reportNo == 4:
        returnOP = []
        rentOP = []
        for operation in operations:
            if operation[0] == "rent" and "3" in operation[4:]:
                rentOP.append(operation)
            elif operation[0] == "return" and "3" in operation[5:]:
                returnOP.append(operation)

        total_time = 0
        number_of_renters = 0

        for i in rentOP:
            start_date = i[3]
            renter1 = i[2]
            for j in returnOP:
                end_date = j[3]
                renter2 = j[2]
                if renter1 == renter2 and days_between_dates(start_date, end_date) > 0:
                    total_time += days_between_dates(start_date, end_date)
                    number_of_renters += 1
                    break

        result = round((total_time / number_of_renters), 2)

        return "report4;" + str(result)


def checkAvailability(bookIDs):
    books = readFiles("books.txt")
    availability = True
    notAvailableBooks = ""
    for bookID in bookIDs:
        if int(books[bookID][3]) == 0:
            availability = "availabilityerror"
            notAvailableBooks = notAvailableBooks + ";" + books[bookID][0] + "|" + books[bookID][1]

    return str(availability) + notAvailableBooks


def canClientRent(clientUserName):
    rentedBooks = []
    returnedBooks = []
    operations = readFiles("operations.txt")

    for operation in operations:
        if operation[0] == "rent" and operation[2] == clientUserName:
            rentedBooks = rentedBooks + operation[4:]
        elif operation[0] == "return" and operation[2] == clientUserName:
            returnedBooks = returnedBooks + operation[5:]

    if len(rentedBooks) != len(returnedBooks):
        books = readFiles("books.txt")
        msg = "renterror;" + clientUserName
        notReturnedBooks = []
        for i in rentedBooks:
            if returnedBooks.count(i) != rentedBooks.count(i) and i not in notReturnedBooks:
                msg = msg + ";" + books[i][0] + "|" + books[i][1]
                notReturnedBooks.append(i)
        return msg
    else:
        return "True"

def updateBookFile(bookIDs, operation):
    books = readFiles("books.txt")
    try:
        for bookID in bookIDs:
            if operation == "rent":
                books[bookID][3] = str(int(books[bookID][3]) - 1)

            elif operation == "return":
                books[bookID][3] = str(int(books[bookID][3]) + 1)
        with fileLock:
            with open("books.txt", "w") as file:
                for i in books.keys():
                    row = i + ";" + books[i][0] + ";" + books[i][1] + ";" + books[i][2] + ";" + books[i][3]
                    if list(books.keys())[-1] != i:
                        row += "\n"
                    file.writelines(row)

        return True

    except:
        return False

def updateOperationFile(newData):
    newData = "\n" + newData
    try:
        with fileLock:
            with open("operations.txt", 'a') as file:
                file.writelines(newData)
        return True

    except:
        return False

def checkBookReturnedAlready(clientUserName, bookIDs):
    books = readFiles("operations.txt")
    rented_books = []
    returned_books = []
    for line in books:
        if line[0] == "rent" and clientUserName == line[2]:
            rented_books.append(line)
        elif line[0] == "return" and clientUserName == line[2]:
            returned_books.append(line)

    for i in bookIDs:
        rented = []
        returned = []
        for rnt in rented_books:
            if i in rnt[4:]:
                rented.append(i)

        for rtr in returned_books:
            if i in rtr[5:]:
                returned.append(i)

        if len(rented) == len(returned):
            bookData = readFiles("books.txt")
            msg = "returnerror" + ";" + clientUserName
            print(bookIDs)
            for bookID in bookIDs:
                msg = msg + ";" + bookData[bookID][0] + "|" + bookData[bookID][0]
            print(msg)
            return msg

        else:
            return "True"



def calculate_rent_fee(book_ids, date_str, name):
    # This function calculates the rent fee based on the daily fee and rental period
    books_data = readFiles("books.txt")
    operations = readFiles("operations.txt")
    rented = []
    total_rent_fee = 0

    for book_id in book_ids:
        for operation in operations:
            if operation[0] == "rent" and operation[2] == name and book_id in operation[4:]:
                rented.append(operation)
        oldDate = rented[-1][3]

        daily_fee = float(books_data[book_id][2])

        total_days_rented = days_between_dates(oldDate, date_str)

        total_rent_fee += total_days_rented * daily_fee


    return str(round(total_rent_fee, 2))


class ClientThread(Thread):

    def __init__(self, clientsocket, clientaddress):
        Thread.__init__(self)
        self.clientsocket = clientsocket
        self.clientaddress = clientaddress
        print("Connection from ", clientaddress)

    def run(self):
        msg = "connectionsuccess".encode()
        self.clientsocket.send(msg)
        while True:
            try:
                data = self.clientsocket.recv(1024).decode()
                rowData = data
                data = data.split(";")

                if data[0] == "login":
                    result = readFiles("users.txt")
                    if data[1] in result.keys() and result[data[1]][0] == data[2]:
                        msg = "loginsuccess;" + data[1] + ";" + result[data[1]][1]
                    else:
                        msg = "loginfailure"
                    msg = msg.encode()
                    self.clientsocket.send(msg)

                elif data[0] == "rent":
                    availability = checkAvailability(data[4:])
                    canRent = canClientRent(data[2])

                    if availability != "True":
                        self.clientsocket.send(availability.encode())

                    elif canRent != "True":
                        self.clientsocket.send(canRent.encode())

                    else:
                        if updateBookFile(data[4:], "rent") and updateOperationFile(rowData):
                            self.clientsocket.send("rentsuccess".encode())
                        else:
                            self.clientsocket.send("fileError".encode())

                elif data[0] == "return":

                    librarian_username = data[1]
                    client_name = data[2]
                    date_str = data[3]
                    book_ids = data[4:]

                    invalid_returns = checkBookReturnedAlready(client_name, book_ids)

                    if invalid_returns.split(";")[0] == "returnerror":
                        self.clientsocket.send(invalid_returns.encode())

                    else:
                        success_msg = ""
                        try:
                            # Calculate the rent fee
                            rent_fee = calculate_rent_fee(book_ids, date_str, client_name)
                            if float(rent_fee) >= 0:

                                datamsg = "return;" + librarian_username + ";" + client_name + ";" + date_str + ";" + rent_fee + ";" + ";".join(book_ids)
                                # Log the return operation in operations.txt
                                isOperationUpdate = updateOperationFile(datamsg)
                                isUpdated = updateBookFile(book_ids, "return")

                                if isOperationUpdate and isUpdated:
                                    # Send a success message back to the client
                                    success_msg = f"returnsuccess;Return operation successful!\n\nCost: {rent_fee} $"
                                else:
                                    success_msg = f"fileError"

                            elif float(rent_fee) < 0:
                                success_msg = f"daterror"
                            self.clientsocket.send(success_msg.encode())
                        except Exception as e:
                            # Handle any exceptions that might occur during the return operation
                            error_msg = f"Error during return operation:\n{str(e)}"
                            self.clientsocket.send(error_msg.encode())

                if "report" in data[0]:
                    result = calculateStatistics(int(data[0][-1]))
                    result = result.encode()
                    self.clientsocket.send(result)

            except ConnectionError:
                print("Connection lost with ", clientaddress)
                break

        self.clientsocket.close()


HOST = "127.0.0.1"
PORT = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print("Server is started")
print("Waiting for connections")
while True:
    server.listen()
    clientsocket, clientaddress = server.accept()
    newThread = ClientThread(clientsocket, clientaddress)
    newThread.start()
