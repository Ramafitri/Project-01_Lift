import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import time
import math
import sys

# function
# BAGIAN 1 
def start():
    global start_time, running
    start_time = time.time()
    running = True

def stop():
    global running
    running = False

# BAGIAN 2
list_data = []
total_weight = []
berat = 0
def add():
    global berat, list_data, total_weight, jalur
    a,b,c = int(entry_awal.get()), int(entry_tujuan.get()), int(entry_berat.get())
    data = [a,b,c]
    maximum_weight = 1000
    

    if data:
        berat = data[2]
        if data[0] != data[1] and 0 < data[0] < 8 and 0 < data[1] < 8:
            if (sum(total_weight)+berat) < maximum_weight:
                total_weight.append(berat)
                list_data.append(data)
                print("data", list_data)

                jalur.append(data[0])
                jalur.append(data[1])
                print("Jalur lift", jalur)
            else:
                showinfo(title="ALERT !", message="Lift sudah mencapai batas berat")
        else:
            showinfo(title="ALERT !", message= "Input Invalid, tujuan Anda mungkin berada di luar batas atau berada di lantai yang sama")
 
        entry_awal.delete(0, 'end')
        entry_tujuan.delete(0, 'end')
        entry_berat.delete(0, 'end')


def move():
    global jalur, k, i, y_0, y, p
    if jalur:
        gerak = jalur.pop(0)
        print(gerak)
        run_program(gerak)
    else:
        stop()
    
def run_program(gerak):
    global elapsed_time_ms, t1, rect_y, rect_x, vt, v_0, k, i, y_0, p, a
    
    y = (8 - gerak)*75

    v_max = ((2 * abs(a) * 1/3 * abs(y - y_0))**0.5)
    t = (2*v_max / abs(a)) + (abs(y - y_0) / (3 * v_max))
    t1 = ((2 * abs(y - y_0) / (3*abs(a)))**0.5 )
    t2 = (abs(y-y_0)) / (3*v_max)
    t3 = t - t1 - t2

    ### PERCEPATAN AWAL
    if y < y_0:
        a = -1.5 * 25
    else:
        a = 1.5 * 25

    ### RUMUS
    elapsed_time_ms += 1

    ### PERUBAHAN KECEPATAN
    a_c = a
    if t1*1000 <= elapsed_time_ms <= (t1 + t2)*1000:    
        a_c = 0
        v_0 = vt
        t2 = t1 + abs(y-y_0) / (3 * abs(v_0))
        
    # t2 ... t3
    elif (t1 + t2)*1000 <= elapsed_time_ms <= t*1000:
        if vt > 0:
            a_c = -1.5*25
        elif vt < 0:
            a_c = 1.5*25
        v_0 = vt
        i = t2

    vt = v_0 + a_c*(((elapsed_time_ms/1000-i)))
    rect_y += vt/1000
    rect.place(x=rect_x, y=rect_y)

    if elapsed_time_ms <= (t*1000):
        window.after(1, run_program, gerak)
    else:
        y_0 = y
        elapsed_time_ms = 0
        window.after(100, move)
        
### Variabel
v_0 = 0
a = 1.5       
y_0 = 300         
t2 = 0
i = 0
k = 0
vt = 0
p = 0

jalur = []

### window
window = tk.Tk()
window.title('Program Lift!')
window.geometry('900x600')
window.resizable(False,False)

### string variabel
LANTAI_AWAL = tk.StringVar()
LANTAI_TUJUAN = tk.StringVar()
BERAT = tk.StringVar()

elapsed_time_ms = 0

### user section
input_frame = ttk.Frame(master= window)

# awal
awal_frame = ttk.Frame(master= input_frame)
awal_frame.pack(anchor="w", padx= 30)

label_awal = ttk.Label(master= awal_frame, text= "Lantai awal\t: ", font="Roboto 15")
label_awal.pack(side='left')

entry_awal = ttk.Entry(master= awal_frame, textvariable=LANTAI_AWAL)
entry_awal.pack(side='left')

# tujuan
tujuan_frame = ttk.Frame(master= input_frame)
tujuan_frame.pack(anchor="w", padx=30)

label_tujuan = ttk.Label(master= tujuan_frame, text= "Lantai tujuan\t: ", font="Roboto 15")
label_tujuan.pack(side='left')

entry_tujuan = ttk.Entry(master= tujuan_frame, textvariable=LANTAI_TUJUAN)
entry_tujuan.pack(side='left')

# berat
berat_frame = ttk.Frame(master= input_frame)
berat_frame.pack(anchor="w", padx=30)

label_berat = ttk.Label(master= berat_frame, text= "Berat badan\t: ", font="Roboto 15")
label_berat.pack(side='left')

entry_berat = ttk.Entry(master= berat_frame, textvariable=BERAT)
entry_berat.pack(side='left')

# button
button_add = ttk.Button(master= input_frame, text = "Tambahkan orang", command= add)   # menambahkan data orang
button_add.pack(pady=5,ipadx=140)

button_start = ttk.Button(master= input_frame, text = "Jalankan!", command= move)      # VISUALISASIKAN!
button_start.pack(pady=5,ipadx=155)

### visualization section
visual_frame = ttk.Frame(master=window)

# line
line_x = 40

# lt 7
text7 = tk.Label(master=visual_frame,text="Floor 7", font="Roboto 10 italic")
text7.place(x=420-18, y=75 - 20)
line7 = tk.Frame(master=visual_frame, bg='black',height=2,width=420)
line7.place(x=line_x,y=75)

# lt 6
text6 = tk.Label(master=visual_frame,text="Floor 6", font="Roboto 10 italic")
text6.place(x=420-18, y=150 - 20)
line6 = tk.Frame(master=visual_frame, bg='black',height=2,width=420)
line6.place(x=line_x,y=150)

# lt 5
text5= tk.Label(master=visual_frame,text="Floor 5", font="Roboto 10 italic")
text5.place(x=420-18, y=225 - 20)
line5 = tk.Frame(master=visual_frame, bg='black',height=2,width=420)
line5.place(x=line_x,y=225)

# lt 4
text4 = tk.Label(master=visual_frame,text="Floor 4", font="Roboto 10 italic")
text4.place(x=420-18, y=300- 20)
line4 = tk.Frame(master=visual_frame, bg='black',height=2,width=420)
line4.place(x=line_x,y=300)

# lt 2
text3 = tk.Label(master=visual_frame,text="Floor 3", font="Roboto 10 italic")
text3.place(x=420-18, y=375- 20)
line3 = tk.Frame(master=visual_frame, bg='black',height=2,width=420)
line3.place(x=line_x,y=375)

# lt 2
text2 = tk.Label(master=visual_frame,text="Floor 2", font="Roboto 10 italic")
text2.place(x=420-18, y=450 - 20)
line2 = tk.Frame(master=visual_frame, bg='black',height=2,width=420)
line2.place(x=line_x,y=450)

# lt 1
text1 = tk.Label(master=visual_frame,text="Floor 1", font="Roboto 10 italic")
text1.place(x=420-18, y=525 - 20)
line1 = tk.Frame(master=visual_frame, bg='black',height=2,width=420)
line1.place(x=line_x,y=525)

# rect
rect_h = 30
rect_w = 20

rect_x = 10
rect_y = 300-rect_h

rect = tk.Frame(master=visual_frame, bg="gray80", relief=tk.FLAT ,height=rect_h, width=rect_w)
rect.place(x=rect_x, y=rect_y)

rect['highlightbackground'] = 'gray50'
rect['highlightthickness'] = 2

### terminate
input_frame.place(x=450,y=100, height=460, width=450)
visual_frame.place(x=0,y=50,height=600,width=450)

### title
title_label = ttk.Label(master= window, text= 'PROGRAM LIFT!', font='Roboto 24 bold')
title_label.pack(padx=10, pady=10)

### main loop
window.mainloop()







