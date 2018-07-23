import Tkinter
import ttk
import requests
import webbrowser

users = [
         'vici',
         'noxe'
         ]

rk_colors = ['blue', 'purple', 'orange', 'red']
rk_thresholds = [1900, 2100, 2400, 3000]


def OnDoubleClick(event):
    item = tree.selection()[0]
    idx = int(tree.item(item, "text")) - 1
    url = "http://codeforces.com/profile/" + users[idx]
    webbrowser.open_new(url)

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

def rankCol(rating):
    for idx in range(len(rk_colors)):
        if rating < rk_thresholds[idx]:
            return rk_colors[idx]
    return 'black'

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
    tree.item(children[idx], values = (users[idx], rating, maxRating), tags = (rankCol(rating)))

    for color in rk_colors:
        tree.tag_configure(color, foreground=color)

win = Tkinter.Tk()
tree = ttk.Treeview(win)
columns = ("name", "rating", "maxRating")
tree["height"] = 20
tree["columns"] = columns
tree.column("name", width = 100)
tree.column("rating", width = 100)
tree.column("maxRating", width = 100)
tree.bind("<Double-1>", OnDoubleClick)

for idx in range(len(users)):
    tree.insert("", idx, text = str(idx + 1) ,values=(users[idx], "", ""))

for col in columns:
    tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, True))

btn_upd = ttk.Button(win, text = "update", command = update)
tree.pack()
btn_upd.pack()
win.mainloop()
