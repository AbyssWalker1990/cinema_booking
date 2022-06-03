import sqlite3


class SeatChecker:
    def __init__(self, name, seat_id):
        self.name = name
        self.seat_id = seat_id

    def check_seat_info(self):
        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "taken" FROM "Seat" WHERE "seat_id"=?
        """, [self.seat_id])
        result = cursor.fetchone()
        connection.close()
        if result[0] == 1:
            print("The seat is occupy")
        else:
            self.check_card()

    def check_card(self):
        card_type = input("Тип карти?")
        self.card_number = input("Номер карти?")
        cvv = input("CVV?")
        holder_name = input("Ім'я власника")

        connection = sqlite3.connect("banking.db")
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM "Card" WHERE "number"=?
        """, [self.card_number])
        result = cursor.fetchall()
        print(result)
        connection.close()
        db_card_type = result[0][0]
        db_card_number = result[0][1]
        db_cvv = result[0][2]
        db_holder_name = result[0][3]
        if card_type == db_card_type and\
                self.card_number == db_card_number and\
                cvv == db_cvv and \
                holder_name == db_holder_name:
            self.buy_ticket()
        else:
            print("Невірні дані картки")

    def buy_ticket(self):
        connection = sqlite3.connect("banking.db")
        cursor = connection.cursor()
        cursor.execute("""
               SELECT "balance" FROM "Card" WHERE "number"=?
               """, [self.card_number])
        client_balance = cursor.fetchone()
        connection.close()

        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor()
        cursor.execute("""
                       SELECT "price" FROM "Seat" WHERE "seat_id"=?
                       """, [self.seat_id])
        seat_price = cursor.fetchone()
        connection.close()

        if client_balance > seat_price:
            print("enough money")
        else:
            print("NOT ENOUGH MONEY")





name = input("Ваше ім'я? ")
seat_id = input("Виберіть місце:")
client = SeatChecker(name, seat_id)
client.check_seat_info()
