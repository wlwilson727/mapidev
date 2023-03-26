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
newencounterform_label = tk.Label(root, text='Enter New Encounter Information')
newencounterform_label.pack()

# Get a list of patients to choose from
cursor.execute("SELECT umrn, firstname, lastname FROM patients ORDER BY lastname")
patients = cursor.fetchall()

# Display the list of patients in a drop-down menu
selected_patient = tk.StringVar(root)
selected_patient.set(patients[0][0])  # Set the default value to the first patient's UMRN in the list
patient_menu = tk.OptionMenu(root, selected_patient, *[patient[0] for patient in patients])
patient_menu.pack()

# Create fields for encounter details
encounter_date_label = tk.Label(root, text='Encounter Date (MM/DD/YYYY):')
encounter_date_label.pack()
encounter_date_entry = tk.Entry(root)
encounter_date_entry.pack()

encounter_provider_label = tk.Label(root, text='Provider Name:')
encounter_provider_label.pack()
encounter_provider_entry = tk.Entry(root)
encounter_provider_entry.pack()

encounter_note_label = tk.Label(root, text='Encounter Note:')
encounter_note_label.pack()
encounter_note_entry = tk.Entry(root)
encounter_note_entry.pack()

encounter_hsmrn_label = tk.Label(root, text='HSMRN:')
encounter_hsmrn_label.pack()
encounter_hsmrn_entry = tk.Entry(root)
encounter_hsmrn_entry.pack()

def submit_encounter():
    # Get the values from the entry widgets
    selected_umrn = selected_patient.get()[0]
    encounter_date = encounter_date_entry.get()
    encounter_provider = encounter_provider_entry.get()
    encounter_note = encounter_note_entry.get()
    encounter_hsmrn = encounter_hsmrn_entry.get()

    try:
        # Get the next encounter ID from the sequence
        cursor.execute("SELECT NEXT VALUE FOR encounterid_seq")
        encounter_id = cursor.fetchone()[0]

        # Insert the new encounter into the database
        params = (encounter_id, selected_umrn, encounter_date, encounter_provider, encounter_note, encounter_hsmrn)
        cursor.execute("INSERT INTO encounters (encounter_id, umrn, encounter_date, provider, note, hsmrn) "
                       "VALUES (?, ?, CONVERT(datetime, ?, 101), ?, ?, ?)", params)
        
        conn.commit()

        # Show a message box to confirm that the encounter was added
        messagebox.showinfo("Encounter Added", "Encounter added successfully!")
    except Exception as e:
        # Handle any errors that might occur
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create a button to submit the encounter details
submit_button = tk.Button(root, text='Submit', command=submit_encounter)
submit_button.pack()

# Start the UI loop
root.mainloop()

# Close the database connection
conn.close()