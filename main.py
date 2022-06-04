import sqlite3
import webbrowser
import random
import string

from fpdf import FPDF



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
        connection.close()
        db_card_type = result[0][0]
        db_card_number = result[0][1]
        db_cvv = result[0][2]
        db_holder_name = result[0][3]
        if card_type == db_card_type and \
                self.card_number == db_card_number and \
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
        self.client_balance = cursor.fetchone()
        connection.close()

        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor()
        cursor.execute("""
                       SELECT "price" FROM "Seat" WHERE "seat_id"=?
                       """, [self.seat_id])
        seat_price = cursor.fetchone()
        connection.close()

        if self.client_balance > seat_price:
            print("Enough money")
            self.seat_status_change(occupied=1, seat_id=self.seat_id)
            self.balance_change()
        else:
            print("NOT ENOUGH MONEY")

    def seat_status_change(self, occupied, seat_id):

        connection = sqlite3.connect("cinema.db")
        connection.execute("""
        UPDATE "Seat" SET "taken"=? WHERE "seat_id"=?
        """, [occupied, seat_id])
        connection.commit()
        connection.close()

    def balance_change(self):
        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor()
        cursor.execute("""
               SELECT "price" FROM "Seat" WHERE "seat_id"=?
               """, [self.seat_id])
        self.seat_price = cursor.fetchone()
        print(self.seat_price)
        connection.close()

        new_client_balance = self.client_balance[0] - self.seat_price[0]

        connection = sqlite3.connect("banking.db")
        connection.execute("""
                UPDATE "Card" SET "balance"=? WHERE "number"=?
                """, [new_client_balance, self.card_number])
        connection.commit()
        connection.close()

        print("Покупка Успішно проведена")


class TicketPdf:

    def __init__(self, filename):
        self.filename = filename

    def generate(self, seat_checker):
        letters = string.ascii_lowercase
        print(''.join(random.choice(letters) for i in range(10)))

        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()
        pdf.set_font(family='Times', style='B', size=24)
        pdf.cell(w=0, h=80, txt='Your Digital Ticket', align='C', border=1, ln=1)

        pdf.set_font(family='Times', style='B', size=14)
        pdf.cell(w=150, h=40, txt='Name: ', border=1)
        pdf.cell(w=200, h=40, txt=client.name, border=1, ln=1)

        pdf.cell(w=150, h=40, txt='Ticket Id: ', border=1)
        pdf.cell(w=200, h=40, txt=letters, border=1, ln=1)
        pdf.cell(w=150, h=40, txt='Price: ', border=1)
        pdf.cell(w=200, h=40, txt=str(client.seat_price[0]), border=1, ln=1)
        pdf.cell(w=150, h=40, txt='Seat ID: ', border=1)
        pdf.cell(w=200, h=40, txt=client.seat_id, border=1, ln=1)





        pdf.output(self.filename)
        webbrowser.open(self.filename)





name = input("Ваше ім'я? ")
seat_id = input("Виберіть місце:")
client = SeatChecker(name, seat_id)
client.check_seat_info()
ticket = TicketPdf("ticket.pdf")
ticket.generate(client)

