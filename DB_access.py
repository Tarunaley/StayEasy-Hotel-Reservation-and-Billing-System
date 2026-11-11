import sqlite3
import csv
def get_connection():
    conn=sqlite3.connect("stayeasy.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
def create_tables():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
        create table is not exists rooms(
            room_number integer primary key,
            room_type text not null,
            floor integer not null
        )
    """)
    cursor.execute("""
        create table is not exists(
            mobile text primary key,
            name text not null,
            email text not null
        )
    """)

    cursor.execute("""
        create table is not exists bookings(
            mobile text not null,
            room_number integer not null,
            check_in text not null,
            check_out text not null,
            guests_count integer not null,
            breakfast integer not null,
            status text not null,

            FOREIGN KEY(mobile) REFERENCES guests(mobile),
            FOREIGN KEY(room_number) REFERENCES rooms(room_number)
        )
    """)
    
    conn.commit()
    conn.close()
def load_rooms():
    rooms_data=[]
    with open("rooms.csv", "r") as file:
        reader=csv.DictReader(file)
        for row in reader:
            rooms_data.append(row)
    seen_ids=set()

    conn=get_connection()
    cursor=conn.cursor()
    with open("app.log", "a") as log_file:
        for row in rooms_data:
            try:
                room_number=row["room_no"].strip()
                room_type=row["room_type"].strip().capitalize()
                floor=row["floor"].strip()
                if not room_number or not room_type or not floor:
                    log_file.write(f"{row}: Values cannot be null\n")
                    continue
                if not room_number.isdigit() or int(room_number)<=0:
                    log_file.write(f"{room_number}: Invalid room number\n")
                    continue
                if room_number in seen_ids:
                    log_file.write(f"{room_number}: Duplicate room found\n")
                    continue

                if room_type not in ["Standard", "Deluxe", "Suite"]:
                    log_file.write(f"{room_number}: Invalid room type\n")
                    continue

                if not (floor.isdigit() and int(floor)>0):
                    log_file.write(f"{room_number}: Invalid floor\n")
                    continue
                seen_ids.add(room_number)
                cursor.execute("""
                    INSERT INTO rooms
                    (room_number, room_type, floor)
                    VALUES (?, ?, ?)
                """, (int(room_number),room_type,int(floor)))
            except ValueError as e:
                log_file.write(f"{row}: Invalid record - {e}\n")
    conn.commit()
    conn.close()
def get_available_rooms(check_in, check_out, room_type):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        select r.room_number
        FROM rooms r
        WHERE r.room_number NOT IN (
            SELECT b.room_number
            FROM bookings b
            WHERE b.check_in<?
            AND b.check_out>?
            AND b.status IN ('CONFIRMED', 'CHECKED_IN')
        )
        AND r.room_type = ?
        ORDER BY r.room_number;
        """

    cursor.execute(query,(check_out,check_in,room_type))
def add_guest(guest):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute()
    conn.commit()   
    conn.close()
def create_booking(booking):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            insert into bookings
            ( mobile, room_number, check_in,
             check_out, guests_count, breakfast, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (booking.booking_id,
            booking.guest.mobile,
            booking.room.room_number,
            booking.check_in,
            booking.check_out,
            booking.guests_count,
            int(booking.breakfast),
            booking.status))
        
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()
