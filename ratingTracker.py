import Tkinter
import ttk
import requests

users = [
         'vici',
         'noxe'
         ]

win = Tkinter.Tk()
tree = ttk.Treeview(win)
columns = ("name", "rating", "maxRating")
tree["height"] = 20
tree["columns"] = columns
tree.column("name", width = 100)
tree.column("rating", width = 100)
tree.column("maxRating", width = 100)

for idx in range(len(users)):
    tree.insert("", idx, text = str(idx + 1) ,values=(users[idx], "", ""))

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

def update():
    children = tree.get_children()
    str = ''
    for idx in range(len(users)):
        if idx == 0:
            str += users[idx]
        else:
            str += ';' + users[idx]

re = requests.get('http://codeforces.com/api/user.info?handles=' + str)
for idx in range(len(users)):
    rating = re.json()['result'][idx]['rating']
    maxRating = re.json()['result'][idx]['maxRating']
    tree.item(children[idx], values = (users[idx], rating, maxRating))

for col in columns:
    tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, True))

btn_upd = ttk.Button(win, text = "update", command = update)
tree.pack()
btn_upd.pack()
win.mainloop()
