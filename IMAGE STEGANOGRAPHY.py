from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import os
from stegano import lsb

# Create the main Tkinter window
win = Tk()
win.geometry('700x480')
win.config(bg='black')
win.title("Message Hiding in Image")

# Declare hide_msg as a global variable to store the modified image
hide_msg = None

# Function to open an image file
def open_img():
    global open_file
    # Ask the user to select an image file
    open_file = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title='Select File Type',
        filetypes=(('PNG file', '*.png'), ('JPG file', '*.jpg'), ('All file', '*.txt'))
    )
    # Display the selected image in a Tkinter label
    img = Image.open(open_file)
    img = ImageTk.PhotoImage(img)
    lf1.configure(image=img)
    lf1.image = img

# Function to get a secret key from the user
def get_security_key():
    password = simpledialog.askstring("Security Key", "Enter Secret Key", show='*')
    return password

# Function to hide a message in the selected image
def hide():
    global hide_msg  # Declare hide_msg as a global variable
    password = get_security_key()
    if password:
        msg = text1.get(1.0, END)
        try:
            # Use stegano library to hide the message in the image
            hide_msg = lsb.hide(str(open_file), msg)
            # Show a success message
            messagebox.showinfo('Success', 'Your message is successfully hidden in an image, please save your image')
        except Exception as e:
            # Show an error message if hiding fails
            messagebox.showerror('Error', f'Failed to hide message: {str(e)}')
    else:
        # Show an error message if no password is provided
        messagebox.showerror('Error', 'Please enter Secret key')

# Function to save the modified image
def save_img():
    global hide_msg  # Declare hide_msg as a global variable
    if hide_msg:
        # Save the modified image with the hidden message
        hide_msg.save('Secret_file.png')
        # Show a success message
        messagebox.showinfo('Saved', 'Image has been successfully saved')
    else:
        # Show an error message if no image is available to save
        messagebox.showerror('Error', 'No image to save. Please hide a message first.')

# Function to reveal and display the hidden message in the image
def show():
    password = get_security_key()
    if password:
        # Use stegano library to reveal the hidden message in the image
        show_msg = lsb.reveal(open_file)
        # Display the revealed message in the Tkinter text widget
        text1.delete(1.0, END)
        text1.insert(END, show_msg)
    else:
        # Show an error message if no password is provided
        messagebox.showerror('Error', 'Please enter Secret key')

# Tkinter GUI setup

# Heading
Label(win, text='Message Hiding in Image', font='impack 30 bold', bg='black', fg='red').place(x=260, y=12)

# Frame 1
f1 = Frame(win, width=250, height=220, bd=5, bg='purple')
f1.place(x=50, y=100)
lf1 = Label(f1, bg='purple')
lf1.place(x=0, y=0)

# Frame 2
f2 = Frame(win, width=320, height=220, bd=5, bg='white')
f2.place(x=330, y=100)
text1 = Text(f2, font='ariel 15 bold', wrap=WORD)
text1.place(x=0, y=0, width=310, height=210)

# Label for Secret Key
Label(win, text='Enter Secret Key', font='10', bg='black', fg='yellow').place(x=250, y=330)

# Entry Widget for secret key
code = StringVar()
e = Entry(win, textvariable=code, bd=2, font='impact 10 bold ', show='*')
e.place(x=245, y=360)

# Buttons
open_button = Button(win, text='Open Image', bg='blue', fg='white', font='ariel 12 bold ', cursor='hand2',
                     command=open_img)
open_button.place(x=60, y=417)

save_button = Button(win, text='Save Image', bg='green', fg='white', font='ariel 12 bold ', cursor='hand2',
                     command=save_img)
save_button.place(x=190, y=417)

hide_button = Button(win, text='Hide Data', bg='red', fg='white', font='ariel 12 bold ', cursor='hand2', command=hide)
hide_button.place(x=380, y=417)

show_button = Button(win, text='Show Data', bg='orange', fg='white', font='ariel 12 bold ', cursor='hand2', command=show)
show_button.place(x=510, y=417)

# Start the Tkinter main loop
mainloop()
