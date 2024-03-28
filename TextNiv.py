import csv
from datetime import datetime

# Function to load room data from hotel_room.csv file
def load_room_data():
    rooms = {}
    with open('/Users/niveditasaha/Downloads/Coursework syst. desgn./hotel_room.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            rooms[int(row['Room ID'])] = {
                'Room Type': row['Room Type'],
                'Max People': int(row['Max People']),
                'Price': float(row['Price'])
            }
    return rooms

# Function to load reservations from reservations_hotel.csv file

def load_reservations():
    reservations = {}
    reference_id_counter = 0  # Default value for reference id counter
    try:
        with open('/Users/niveditasaha/Downloads/Coursework syst. desgn./reservations_hotel.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                room_id = int(row['Room ID'])
                if room_id not in reservations:
                    reservations[room_id] = []
                reservations[room_id].append(row)
        if reservations:  # If reservations are found, set reference_id_counter accordingly the given csv file, by putting the details of room id user can choose their room for booking
            reference_id_counter = max([int(res['Reference Number']) for res_list in reservations.values() for res in res_list], default=0) + 1
    except FileNotFoundError:
        print('File not Found')
    except ValueError:
        print("The room ID should be an number between 1-12")
    return reservations, reference_id_counter




# Function to save reservations to reservations_hotel.csv file
def save_reservations(reservations):
    with open('/Users/niveditasaha/Downloads/Coursework syst. desgn./reservations_hotel.csv', 'w', newline='') as file:
        if reservations:
            writer = csv.DictWriter(file, fieldnames=reservations[next(iter(reservations))][0].keys())
            writer.writeheader()
            for res_list in reservations.values():
                for res in res_list:
                 writer.writerow(res)

# Function to calculate the total price for a reservation based on dates
def calculate_price(check_in, check_out, room_price):
    days = (check_out - check_in).days
    return days * room_price

# Function to parse date string
def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d")
    


# Additional utility functions required for booking, this function displays the available rooms details

def find_available_rooms(rooms, reservations, check_in, check_out, num_people, room_type):
    available_rooms = []
    for room_id, room_info in rooms.items():
        if room_info['Max People'] >= num_people and room_info['Room Type'] == room_type:
            bookings = reservations.get(room_id, [])
            if all(parse_date(booking['Check-out Date']) <= check_in or parse_date(booking['Check-in Date']) >= check_out for booking in bookings):
                available_rooms.append(room_id)
    return available_rooms
# This functions for inputting the room booking details of users.
def book_room(rooms, reservations, reference_id_counter):
    name = input("Enter your name: ")
    num_people = int(input("Enter number of people: "))
    check_in_str = input("Enter check-in date (YYYY-MM-DD): ")
    check_out_str = input("Enter check-out date (YYYY-MM-DD): ")
    try:
        with open('hotel_room.csv', newline='') as csvfile:
            data = csv.DictReader(csvfile)
            print("-----Available Rooms-----")
            for row in data:
                print('[' + row['Room ID'] + ']',
                      row['Room Type'] )
    except FileNotFoundError:
        print("File not found. Check the path variable and filename")

    room_type = input("Enter room type: ")

    check_in = parse_date(check_in_str)
    check_out = parse_date(check_out_str)

    available_rooms = find_available_rooms(rooms, reservations, check_in, check_out, num_people, room_type)
    if not available_rooms:
        print("No available rooms matching your criteria.")
        return

    print("Available rooms:")
    for room_id in available_rooms:
        print(f"Room {room_id} - {rooms[room_id]['Room Type']} - ${rooms[room_id]['Price']} per night")

    room_choice = int(input("Enter room choice (Room ID): "))
    print(room_choice, available_rooms)
    if room_choice not in available_rooms:
        print("Invalid choice.")
        return

    total_price = calculate_price(check_in, check_out, rooms[room_choice]['Price'])
    reservation = {
        'Reference Number': reference_id_counter,
        'Name': name,
        'Room ID': room_choice,
        'Number of People': num_people,
        'Check-in Date': check_in_str,
        'Check-out Date': check_out_str,
        'Total Price': total_price
    }
    if room_choice not in reservations:
        reservations[room_choice] = []
    reservations[room_choice].append(reservation)

    print("Reservation successful!")
    print("Reference Number:", reference_id_counter)
    print("Reservation Information:", reservation)
    return reference_id_counter + 1  # Update the counter for the next reservation
# This function uses for cancellation and refund 
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

# Main function with program flow
def main():
    rooms = load_room_data()
    reservations, reference_id_counter = load_reservations()

    while True:
        print("\nMenu:")
        print("1. Book a room")
        print("2. Cancel a reservation")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            reference_id_counter = book_room(rooms, reservations, reference_id_counter)
            
        elif choice == '2':
            cancel_reservation(reservations)
        elif choice == '3':
            save_reservations(reservations)
            print("Reservations saved. Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 3.")

if __name__ == "__main__":
    main()
