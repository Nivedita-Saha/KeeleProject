import csv
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import Menu, Toplevel, Label, Entry, Button, messagebox
from datetime import datetime
import tkinter as tk
from TextNiv import *







reservations = []
# Load room data from hotel_room.CSV
def load_room_data():
    rooms_data = []
    with open('/Users/niveditasaha/Downloads/Coursework syst. desgn./hotel_room.csv', 'r') as room_file:
        reader = csv.DictReader(room_file)
        for row in reader:
            rooms_data.append(row)
    return rooms_data

# Load room data from CSV reservations_hotel.csv file
def load_reservation_data():
    reservations_data = []
    with open('/Users/niveditasaha/Downloads/Coursework syst. desgn./reservations_hotel.csv', 'r') as reservations_file:
        reader = csv.DictReader(reservations_file)
        for row in reader:
            reservations_data.append(row)
    return reservations_data


# Function to save reservations data after room booking to reservations_hotel.CSV file
def save_reservation_data(data, filename):
    with open(filename, 'w', newline='') as reservation_file:
        fieldnames = ['Reference Number', 'Name', 'Room ID', 'Number of People', 'Check-in Date', 'Check-out Date', 'Total Price']
        writer = csv.DictWriter(reservation_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# Function to calculate total price, this total price differ according to the room categorisation
def calculate_total_price(room_type, num_nights):
    price_per_night = 0
    if room_type == "Standard-Single":
        price_per_night = 30
    elif room_type == "Standard-Double":
        price_per_night = 35
    elif room_type == "Deluxe-Double":
        price_per_night = 50
    elif room_type == "Family":
        price_per_night = 60
    elif room_type == "Suit":
        price_per_night = 75
    else:
        return None
    return price_per_night * num_nights






# Function to open booking window

def book_room_tkinter():
    def OnClick_BookRoom():
        # Retrieve user input
        name = name_textbox.get()
        number_of_people = int(people_dropdown.get())
        check_in_date_str = check_in_date_textbox.get()
        check_out_date_str = check_out_date_textbox.get()
        room_id = int(room_id_dropdown.get())  
        room_type = rooms_dropdown.get()

        # Validate input, if the listed inputs will not fill then it will show error message
        if not name or not check_in_date_str or not check_out_date_str or not room_type:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Convert dates to datetime objects
        try:
            check_in_date = datetime.strptime(check_in_date_str, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Calculate total price based on the dates
        num_nights = (check_out_date - check_in_date).days
        total_price = calculate_total_price(room_type, num_nights)

        if total_price is None:
            messagebox.showerror("Error", "Invalid room type selected.")
            return


        
        

        # Display receipt after room booking
        reference_number = len(reservations) + 1
        show_receipt(reference_number, name, number_of_people, check_in_date, check_out_date, total_price, room_id, room_type)

    # Open booking window, this function use to create a room booking window
    booking_window = Toplevel(root)
    booking_window.title("Room Booking")
    booking_window.geometry("500x300")


    # Background image for room booking window
    room_window_bg_image = tk.PhotoImage(file=r"/Users/niveditasaha/Downloads/Coursework syst. desgn./IMG_0062.png")
    room_window_bg_label = tk.Label(booking_window, image=room_window_bg_image)
    room_window_bg_label.place(relwidth=1, relheight=1)



     # Name, it's a textbox where user input their name during booking
    tk.Label(booking_window, text="Enter Name").pack(anchor=tk.W, padx=10)
    name_textbox = tk.Entry(booking_window)
    name_textbox.pack(anchor=tk.W, padx=10)

    # Number of people, it's a dropdown using to choose the number of people for the room booking
    choices = ['1', '2', '3', '4']
    tk.Label(booking_window, text="Number of People").pack(anchor=tk.W, padx=10)
    people_dropdown = ttk.Combobox(booking_window, values=choices)
    people_dropdown.pack(anchor=tk.W, padx=10)

    # Check-in Date, this textbox follows YYYY-MM-DD format for check-in
    tk.Label(booking_window, text="Enter Check-in Date (YYYY-MM-DD)").pack(anchor=tk.W, padx=10)
    check_in_date_textbox = tk.Entry(booking_window)
    check_in_date_textbox.pack(anchor=tk.W, padx=10)

    # Check-out Date, this textbox follows YYYY-MM-DD format for check-out
    tk.Label(booking_window, text="Enter Check-out Date (YYYY-MM-DD)").pack(anchor=tk.W, padx=10)
    check_out_date_textbox = tk.Entry(booking_window)
    check_out_date_textbox.pack(anchor=tk.W, padx=10)

    # Room ID, based on the hotel_room.csb file this dropdown created, so that users can choose their Room ID according to their preferences during room booking
    choices = ['1', '2', '3', '4','5','6','7','8','9','10','11','12']
    tk.Label(booking_window, text="Room ID").pack(anchor=tk.W, padx=10)
    room_instructions = tk.Label(booking_window, text="Please check the room ID details in the menu check room status")
    room_instructions.pack(anchor=tk.W, padx=10)
    room_id_dropdown = ttk.Combobox(booking_window, values=choices)  # Define room_id_dropdown
    room_id_dropdown.pack(anchor=tk.W, padx=10)


    # Types of room, based on given csv file fives types of rooms options created by using dropdown and also a room instruction for booking those rooms
    tk.Label(booking_window, text="Types of Rooms").pack(anchor=tk.W, padx=10)
    room_instructions = tk.Label(booking_window, text="Attention!! Standard-Single room for maximum 1 person\nStandard-double and Deluxe-Double for maximum 2 people\nFamily and Suit for maximum 3-4 people")
    room_instructions.pack(anchor=tk.W, padx=10)
    choices = ['Standard-Single', 'Standard-Double', 'Deluxe-Double', 'Family', 'Suit']
    rooms_dropdown = ttk.Combobox(booking_window, values=choices)
    rooms_dropdown.pack(anchor=tk.W, padx=10)


    
     
# This displays a submit button of 'Book Room', after filling the details, by clicking it users cn book their room
    submit_button = tk.Button(booking_window, text='Book Room', command=OnClick_BookRoom)
    submit_button.pack(anchor=tk.W, padx=10, pady=10)


# Function to display room status, thsi shows which rooms are booked and how many rooms are available for booking
def display_room_status():
    # Load room data
    room_file_path = '/Users/niveditasaha/Downloads/Coursework syst. desgn./hotel_room.csv'
    rooms = load_room_data()
    
    available_rooms = []
    booked_rooms = []
    

    for room in rooms:
        booked = False
        for reservation in reservations:
            if room['Room ID'] == reservation['Room ID']:
                booked = True
                break
        if booked:
            booked_rooms.append(room)
        else:
            available_rooms.append(room)

    message = "Available Rooms:\n"
    for room in available_rooms:
        message += f"Room ID: {room['Room ID']}, Room Type: {room['Room Type']}, Price per Night: £{room['Price']}\n"

    message += "\nBooked Rooms:\n"
    for room in booked_rooms:
        message += f"Room ID: {room['Room ID']}, Room Type: {room['Room Type']}, Price per Night: £{room['Price']}\n"

    messagebox.showinfo("Room Status", message)


        
        


    # Function to show reservation receipt
def show_receipt(reference_number, name, number_of_people, check_in, check_out, total_price, room_id, room_type):
    receipt_window = Toplevel(root)
    receipt_window.title("Reservation Receipt")


    # Display receipt, this listed details will show in the reservation receipt after room booking
    tk.Label(receipt_window, text="Reservation Receipt", font=('Arial', 16, 'bold')).pack()
    tk.Label(receipt_window, text=f"Reference Number: {reference_number}").pack()  # Include reference number
    tk.Label(receipt_window, text=f"Name: {name}").pack()
    tk.Label(receipt_window, text=f"Number of People: {number_of_people}").pack()
    tk.Label(receipt_window, text=f"Check-in Date: {check_in.strftime('%Y-%m-%d')}").pack()
    tk.Label(receipt_window, text=f"Check-out Date: {check_out.strftime('%Y-%m-%d')}").pack()
    tk.Label(receipt_window, text=f"Room Type: {room_type}").pack()
    tk.Label(receipt_window, text=f"Room ID: {room_id}").pack()  
    tk.Label(receipt_window, text=f"Total Price: £{total_price}").pack()

    # Append reservation data to reservations list
    reservations.append({
        'Reference Number': reference_number,
        'Name': name,
        'Number of People': number_of_people,
        'Check-in Date': check_in,
        'Check-out Date': check_out,
        'Total Price': total_price,
        'Room ID': room_id  # Include room ID in reservations data
    })

    # Save reservations data
    save_reservation_data(reservations,'/Users/niveditasaha/Downloads/Coursework syst. desgn./reservations_hotel.csv')

        
  
# this cancellation function I use from the text based file, it will also shows the refund details after the room cancellation
def cancel_reservation(reservations):
    reference_number = int(input("Enter your reference number: "))
    for room_id, bookings in reservations.items():
        for booking in bookings:
            if int(booking['Reference Number']) == reference_number:
                print("Reservation found:", booking)
                confirm = input("Confirm cancellation (yes/no): ").lower()
                if confirm == 'yes':
                    refund_amount = float(booking['Total Price']) * 0.7
                    print("Cancellation confirmed. Refund Amount:", refund_amount)
                    bookings.remove(booking)
                    return
                else:
                    print("Cancellation aborted.")
                    return
    print("Reservation not found.")

# Function to cancel reservation
def cancel_reservation_tkinter():
    def cancel_reservation(reference):
        new_reservations = []
        found = False
        for res in reservations:
            if res['Reference Number'] == str(reference):
                print (res)
                price = float(res['Total Price'])
                #cancel_reservation(reference)
                refund_amount = price * 0.7
                found = True
                messagebox.showinfo("Cancellation Successful", f'Cancellation Successful. Your Refund is : {refund_amount}')
            else:
                new_reservations.append(res)

        if not found:
            messagebox.showerror("Cancellation", "Reservation not found.")

        # Update reservations list with the new list
        reservations[:] = new_reservations  # Update existing list instead of creating a new one
        save_reservation_data(reservations, '/Users/niveditasaha/Downloads/Coursework syst. desgn./reservations_hotel.csv') 

        # Update room status display after canceling reservation
        #display_room_status()

    # Function to handle canceling reservation in tkinter-based system
    def OnClick_CancelReservation():
        reference = reference_entry.get()
        if not reference:
            messagebox.showerror("Error", "Please enter a reference number.")
        else:
            #return
            cancel_reservation(int(reference))

    # Open cancelation window
    cancel_window = Toplevel(root)
    cancel_window.title("Cancel a Reservation")
    cancel_window.geometry("300x150")

    # User input field for reference number, after putting the reference details users can easily cancel their reservation
    tk.Label(cancel_window, text="Enter Reference Number:").pack(anchor=tk.W, padx=10, pady=5)
    reference_entry = tk.Entry(cancel_window)
    reference_entry.pack(anchor=tk.W, padx=10, pady=5)

    # Cancel button, after typing the reference number user can cancel their reservation by clicking this cancel button
    cancel_button = tk.Button(cancel_window, text="Cancel Reservation", command=OnClick_CancelReservation)
    cancel_button.pack(anchor=tk.W, padx=10, pady=5)

    


def cancel():
    cancel_reservation()

    # Function to quit the application
def kill():
    root.destroy()




    
# Create the main window
root = tk.Tk()
root.title("Hotel Booking")
root.geometry("1100x1200")

# Background image
bg_image = tk.PhotoImage(file=r"/Users/niveditasaha/Downloads/Coursework syst. desgn./IMG_0058.png")
tk.Label(root, image=bg_image).place(relheight=1, relwidth=1)


tk.Label(root, text='Welcome to My hotel!', font=('Georgia', 24)).pack()


# Create top menu, by clicking this menu user can book a room, cancel the reservation and quit the programm easily
topMenu = tk.Menu(root)
root.config(menu=topMenu)

clickhere = tk.Menu(topMenu)
topMenu.add_cascade(menu=clickhere, label="Click Here")
clickhere.add_command(label="Room Booking", command=book_room_tkinter)
clickhere.add_command(label="Cancel Reservation", command=cancel_reservation_tkinter)
clickhere.add_command(label="Quit", command=kill)



# Button to display room status
room_status_button = tk.Button(root, text='Check Room Status', command=display_room_status)
room_status_button.pack()


# Load reservations data
reservations = load_reservation_data()

root.mainloop()
