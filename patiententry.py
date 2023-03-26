import os
import pyodbc
import tkinter as tk
from tkinter import messagebox

# Get Environment Variable Password
password = os.environ.get('ODBC_PASSWORD')

if password is None:
    print("ODBC_PASSWORD environment variable is not set.")
else:
    # Connection string for MAPI EHR database (mapi-ehr-db)
    conn_str = (
        'Driver={SQL Server};'
        'Server=mapidev.database.windows.net;'
        'Database=mapi-ehr-db;'
        'UID=mapiadmin;'
        'PWD=' + password + ';'
    )

    # Connect to MAPI EHR database using connection string
    conn = pyodbc.connect(conn_str)

    # Create a cursor
    cursor = conn.cursor()

# Create a user interface
root = tk.Tk()
root.geometry('800x600')

# Display Form Title
newpatientform_label = tk.Label(root, text='Enter New Patient Information')
newpatientform_label.pack()

# Enter Patient First Name
#label
firstname_label = tk.Label(root, text='First Name')
firstname_label.pack()
#entry box
firstname_entry = tk.Entry(root)
firstname_entry.pack()

# Enter Patient Middle Name
#label
middlename_label = tk.Label(root, text='Middle Name')
middlename_label.pack()
#entry box
middlename_entry = tk.Entry(root)
middlename_entry.pack()

# Enter Patient Last Name
#label
lastname_label = tk.Label(root, text='Last Name')
lastname_label.pack()
#entry box
lastname_entry = tk.Entry(root)
lastname_entry.pack()

# Enter DOB
#label
dob_label = tk.Label(root, text='Date of Birth')
dob_label.pack()
#entry box
dob_entry = tk.Entry(root)
dob_entry.pack()

# Enter SSN
#label
ssn_label = tk.Label(root, text='SSN')
ssn_label.pack()
#entry box
ssn_entry = tk.Entry(root)
ssn_entry.pack()

# Enter Sex
#label
sex_label = tk.Label(root, text='Sex')
sex_label.pack()
#entry box
sex_entry = tk.Entry(root)
sex_entry.pack()

# Enter race
#label
race_label = tk.Label(root, text='Race')
race_label.pack()
#entry box
race_entry = tk.Entry(root)
race_entry.pack()

# Enter Address 1
#label
add1_label = tk.Label(root, text='Address 1')
add1_label.pack()
#entry box
add1_entry = tk.Entry(root)
add1_entry.pack()

# Enter Address 2
#label
add2_label = tk.Label(root, text='Address 2')
add2_label.pack()
#entry box
add2_entry = tk.Entry(root)
add2_entry.pack()

# Enter City
#label
city_label = tk.Label(root, text='City')
city_label.pack()
#entry box
city_entry = tk.Entry(root)
city_entry.pack()

# Enter State
#label
state_label = tk.Label(root, text='State')
state_label.pack()
#entry box
state_entry = tk.Entry(root)
state_entry.pack()

# Enter Zip
#label
zip_label = tk.Label(root, text='Zip')
zip_label.pack()
#entry box
zip_entry = tk.Entry(root)
zip_entry.pack()

# Add a label for the encounter note
    # note_label = tk.Label(root, text='Note')
    # note_label.pack()

# Add a text box for the encounter note
    # note_entry = tk.Text(root, height=4)
    # note_entry.pack()

# Add button to submit data
def submit_data():
    # Get input values from user
    firstname = firstname_entry.get()
    middlename = middlename_entry.get()
    lastname = lastname_entry.get()
    dob = dob_entry.get()
    ssn = ssn_entry.get()
    sex = sex_entry.get()
    race = race_entry.get()
    add1 = add1_entry.get()
    add2 = add2_entry.get()
    city = city_entry.get()
    state = state_entry.get()
    zip = zip_entry.get()
    # note = note_entry.get()

    # Insert data into database
    cursor.execute("INSERT INTO dbo.patients (firstname, middlename, lastname, dob, ssn, sex, race, address1, address2, city, state, zip) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", firstname, middlename, lastname, dob, ssn, sex, race, add1, add2, city, state, zip)
    # cursor.execute("INSERT INTO dbo.encounters (note) VALUES (?)", note)
    conn.commit()

    # Display UMRN and success message to user
    cursor.execute("SELECT @@IDENTITY AS umrn")
    row = cursor.fetchone()
    umrn = row[0]
    messagebox.showinfo('Success','Data added successfully!'.format(umrn))

submit_button = tk.Button(root, text='Submit', command=submit_data)
submit_button.pack()

root.mainloop()