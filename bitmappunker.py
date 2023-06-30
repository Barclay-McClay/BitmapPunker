import csv
from tkinter import *
from tkinter import filedialog , ttk
import webbrowser, time, os, atexit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image


SORT_ORDER = {}
viewURL = "https://bitfeed.live/block/height/"

COLOURS = {
    "darkTone": "#11140F",
    "midTone": "#313338",
    "lightTone": "#383A40",
    "highlights": "#CECECE"
}

#Create an instance of tkinter frame
window = Tk()
window.title("Bitmap Punker")
window.config(background=COLOURS['darkTone'])
window.iconbitmap('gridIcon.ico')

# FUNCTIONS
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("Directory created successfully.")
    else:
        print("Directory already exists.")

def open_file_dialog():
    # Open the file dialog
    return filedialog.askopenfilename()

def openBrowser():
    selected_item = tree.selection()
    if selected_item:
        column_value = tree.set(selected_item, 1)
        webbrowser.open_new_tab(viewURL+column_value)

def screenshotBrowser():
    lbStatus.configure(text="Screenshotting... Please Wait ⏳",fg=COLOURS['highlights'])
    window.update()
    selected_item = tree.selection()
    if selected_item:
        linkValue = f"{viewURL}{tree.set(selected_item, 1)}"
        driver.get(linkValue)
        time.sleep(6)
        create_directory("screenshots")
        filepath = f"screenshots/bitmapPunk_{tree.set(selected_item, 1)}.png"
        driver.save_screenshot(filepath)
        # Open the PNG image
        with Image.open(filepath) as image:
            crop_coords = (160, 90, 560, 440)
            cropped_image = image.crop(crop_coords)
            cropped_image.save(filepath)
        lbStatus.configure(text=f"Saved to: {filepath}",fg=COLOURS['highlights'])

def sort_treeview(column):
    # Clear existing items in the Treeview
    tree.delete(*tree.get_children())
    # Get the index of the selected column
    column_index = tree["columns"].index(column)
    # Sort the data based on the selected column and sort order
    rev = False if SORT_ORDER[column] == 'asc' else True
    sorted_data = sorted(OUTPUT, key=lambda x: x[column_index], reverse=rev)
    # Insert sorted data into the Treeview
    for i, item in enumerate(sorted_data):
        tree.insert(
            "",
            index=END,
            text=str(i + 1),
            values=item
        )
    
def on_header_click(event, column):
  # Get the current sort order of the column
    current_order = SORT_ORDER.get(column, "")
    # Toggle the sort order between ascending and descending
    new_order = "asc" if current_order == "desc" else "desc"
    # Clear the existing sort indicator arrow
    for col in tree["columns"]:
        tree.heading(col, text=col)
    # Add the sort indicator arrow to the clicked column
    arrow = " ▲" if new_order == "asc" else " ▼"
    tree.heading(column, text=column + arrow)
    # Update the sort order for the clicked column
    SORT_ORDER[column] = new_order
    # Sort the Treeview based on the clicked column and order
    sort_treeview(column)

def autoPilot():
    lbStatus.configure(text="Screenshotting... Please Wait",fg=COLOURS['highlights'])
    for item_id in tree.get_children():
        item_data = tree.item(item_id)
        blockID = item_data["values"][1]
        tree.selection_set(item_id)
        if not os.path.exists(f"screenshots/bitmapPunk_{blockID}.png"):        
            screenshotBrowser()

def fillTree():
    tree.delete(*tree.get_children())
    # Insert data into the Treeview
    for i, item in enumerate(OUTPUT):
        tree.insert(
            "",
            index=END,
            text=str(i + 1),
            values=item
        )

#############################################################################################################################################
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (optional)
chrome_options.add_argument("webdriver.chrome.driver=chromedriver.exe")  # Specify the path to the WebDriver
driver = webdriver.Chrome(options=chrome_options)

with open(open_file_dialog(), 'r', encoding='utf-8') as file:
    data = list(csv.reader(file))
    for row in data:
        row[1] = ''.join(char for char in row[1] if char.isdigit()) # Sanitize IDs
OUTPUT=data

FrTree = Frame(window,background=COLOURS['lightTone'])
FrButtons = Frame(window,background=COLOURS['lightTone'])

# Create a new style for the Treeview
TreeStyle = ttk.Style()
TreeStyle.configure("Custom.Treeview",
                background=COLOURS["midTone"],
                foreground=COLOURS["highlights"],  
                font=("Consolas", 10) 
                )
headerStyle = ttk.Style()
headerStyle.configure("Custom.Treeview.Heading",
                background=COLOURS["darkTone"],  # Set the background color
                font=("Consolas", 10, "bold")   # Set the font
                )
# Create a Treeview widget to display the data
tree = ttk.Treeview(FrTree, style="Custom.Treeview")
tree["columns"] = (
    "Inscription ID",
    "Block Number",
    "Date",
    "Value",
    "Bytes",
    "Transactions",
    "Sub K Range",
    "Negative Punk",
    "Historical Punk",
    "Perfect Punk",
    "Bitfeed Link",
    "Unisat Link"
)

for column in tree["columns"]:
    tree.heading(column, text=column, anchor=CENTER)#, style="Custom.Treeview.Heading")

# Define column widths
tree.column("#0", width=1, minwidth=1, anchor=CENTER)
tree.column("Inscription ID", width=50, minwidth=50, anchor=CENTER)
tree.column("Block Number", width=60, minwidth=60, anchor=CENTER)
tree.column("Date", width=100, minwidth=80, anchor=CENTER)
tree.column("Value", width=80, minwidth=80, anchor=CENTER)
tree.column("Bytes", width=80, minwidth=80, anchor=CENTER)
tree.column("Transactions", width=80, minwidth=80, anchor=CENTER)
tree.column("Sub K Range", width=80, minwidth=100, anchor=CENTER)
tree.column("Negative Punk", width=50, minwidth=50, anchor=CENTER)
tree.column("Historical Punk", width=80, minwidth=50, anchor=CENTER)
tree.column("Perfect Punk", width=50, minwidth=50, anchor=CENTER)
tree.column("Bitfeed Link", width=80, minwidth=80, anchor=CENTER)
tree.column("Unisat Link", width=80, minwidth=80, anchor=CENTER)

# Fill tree
fillTree()

# Create clickable column headers
for i, column in enumerate(tree["columns"]):
    tree.heading(column, text=column)
    tree.heading(column, command=lambda col=column: on_header_click(event=None, column=col))

# Create Action buttons
bWebView = Button(FrButtons,text="Web View 🌐",command=openBrowser,bg=COLOURS["midTone"],fg=COLOURS["highlights"],relief=GROOVE)
bScreenshot = Button(FrButtons,text="Screenshot 📷",command=screenshotBrowser,bg=COLOURS["midTone"],fg=COLOURS["highlights"],relief=GROOVE)
bAuto = Button(FrButtons,text="Auto-pilot 🤖",command=autoPilot,bg=COLOURS["midTone"],fg=COLOURS["highlights"],relief=GROOVE)

bWebView.pack(side=LEFT)
bScreenshot.pack(side=LEFT)
bAuto.pack(side=LEFT)

lbStatus = Label(FrButtons,text="Ready",fg=COLOURS["highlights"],bg=COLOURS["lightTone"])
lbStatus.pack(side=RIGHT)

# Add Treeview to a Scrollbar
scrollbar = Scrollbar(FrTree, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
# Pack the Treeview and Scrollbar
tree.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

FrButtons.pack(side=TOP,fill=X,expand=True)
FrTree.pack(side=BOTTOM,fill=BOTH,expand=True)


atexit.register(lambda: driver.quit())
window.mainloop()