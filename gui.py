import tkinter as tk

# if you are still working under a Python 2 version, 
# comment out the previous line and uncomment the following line
# import Tkinter as tk

root = tk.Tk()
tk.Label(root, 
         text="Red Text in Times Font",
         fg = "red",
         font = "Times").pack(side="left")
tk.Label(root, 
         text="Green Text in Helvetica Font",
         fg = "light green",
         bg = "dark green",
         justify=tk.LEFT,
         padx = 10, 
         font = "Helvetica 16 bold italic").pack(side="left")
tk.Label(root, 
         text="Blue Text in Verdana bold",
         fg = "blue",
         bg = "yellow",
         font = "Verdana 10 bold").pack(side="left")
counter = 0 
def counter_label(label):
  def count():
    global counter
    counter += 2
    label.config(text=str(counter))
    label.after(1000, discount)
  def discount():
    global counter
    counter -= 1
    if counter==3:
        msg = tk.Message(root, text = "whatever_you_do")
        msg.config(bg='lightgreen', font=('times', 24, 'italic'))
        msg.pack()
    label.config(text=str(counter))
    label.after(1000, count)
  count()
 
 

root.title("Counting Seconds")
label = tk.Label(root, fg="green")
label.pack()
counter_label(label)
button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button.pack()
root.mainloop()
