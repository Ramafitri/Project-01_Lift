import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import time
import math
import sys

"""
    ALGORITMA :
        Objective : Membuat lift paling tercepat dan ternyaman
        1. User akan memberi input pada input section berupa lantai awal, lantai tujuan, dan berat
        2. Input user akan disimpan di list_data berupa nested list
        3. Tiap list pada list_data akan dieksekusi satu persatu dimulai dari lantai awal input pertama\
        4. Default position lift akan berada di tengah-tengah jarak total lantai, yakni di lantai 4
        5. Lift bergerak dengan :
                1/3 bagian y -> a (+) untuk berakselerasi agar mencapai kecepatan maksimum;  
                1/3 bagian y -> a (0) untuk menjaga kecepatan konstan agar nyaman;
                1/3 bagian y -> a (-) untuk berhenti. 
            dengan y sebagai jarak
"""

#### FUNCTION
### FUNGSI ADD DATA & SAVE DATA
def add():
    global berat, list_data, total_weight, jalur, maximum_weight                        # mengambil variabel global
    a,b,c = int(entry_awal.get()), int(entry_tujuan.get()), int(entry_berat.get())      # mengambil value dari input section
    data = [a,b,c]                                                                      # inisiasi list tiap satu orang

    # jika data ada
    if data:
        berat = data[2]

        """
            Kriteria data yang akan dijalankan :
                1. lantai awal tidak sama dengan posisi lift awal
                2. lantai tujuan harus berada diantara batas lantai gedung
            jika tidak akan dimunculkan alert dan data yang baru saja diinput akan direset, data yang sudah di save tidak akan ikut direset
        """
        if data[0] != data[1] and 0 < data[0] < 8 and 0 < data[1] < 8:          
            if (sum(total_weight)+berat) < maximum_weight:
                total_weight.append(berat)
                list_data.append(data)
                print("\ndata", list_data)      # menunjukkan list data pada terminal

                jalur.append(data[0])           
                jalur.append(data[1])
                print("\nJalur lift", jalur)    # menunjukkan list jalur yang akan ditempuh lift
            else:
                showinfo(title="ALERT !", message="Lift sudah mencapai batas berat")    # alert jika tidak memenuhi kriteria
        else:
            showinfo(title="ALERT !", message= "Input Invalid, tujuan Anda mungkin berada di luar batas atau berada di lantai yang sama")

        # reset frame input section
        entry_awal.delete(0, 'end')
        entry_tujuan.delete(0, 'end')
        entry_berat.delete(0, 'end')

### FUNGSI GERAK LIFT OLEH KESELURUHAN INPUT
def move():
    global jalur, k, i, y_0, y, p, b, total_weight, a

    # jika jalur ada
    if jalur:
        if ((8-jalur[0])*75) == y_0:        # jika jalur sama dengan posisi awal lift, maka value akan di pop (dibuang)
            jalur.pop(0)

        ## PERCEPATAN AWAL
        if (8-jalur[0])*75 < y_0:
            a = -1.5 * 25
        if (8-jalur[0])*75 > y_0:
            a = 1.5 * 25

        # Gerakan menujul lantai tujuan (gerak merepresentasikan lantai tujuan)
        gerak = jalur.pop(0)
        y = (8 - gerak)*75                  # y : koordinat lantai tujuan

        ## RUMUS  
        v_max = ((2 * abs(a) * 1/3 * abs(y - y_0))**0.5)            # v_max = kecepatan maksimum yang akan ditempuh lift = velocity ketika t1 atau 1/3 y
        t = (2*v_max / abs(a)) + (abs(y - y_0) / (3 * v_max))       # t total satu gerakan lift

        t1 = ((2 * abs(y - y_0) / (3*abs(a)))**0.5 )                # t1 = time saat menempuh jarak 1/3 y
        t2 = (abs(y-y_0)) / (3*v_max)                               # t2 = time saat menempuh jarak 2/3 y
        t3 = t - t1 - t2                                            # t3 = time saat menempuh jarak 3/3 y

        ## RUN PROGRAM : GERAK LIFT 
        run_program(gerak, a, y, v_max, t1, t2, t3, t)



def run_program(gerak, a, y, v_max, t1, t2, t3, t):
    global elapsed_time_ms, rect_y, rect_x, vt, v_0, y_0, p, b, total_weight, a_c, i

    ## ELAPSED TIME
    elapsed_time_ms += 1
    
    ### PERUBAHAN KECEPATAN
    # t0...t1 : kecepatan dinaikkan 
    if elapsed_time_ms == 1:
        a_c = a

    # t1...t2 : kecepatan konstan
    elif t1*1000 - 1 <= elapsed_time_ms <= t1*1000 :    
        a_c = 0
        v_0 = vt
        
    # t2 ... t3 : kecepatan diturunkan
    elif (t1 + t2)*1000 - 1  <= elapsed_time_ms <= (t1 + t2)*1000:
        if v_0 > 0:
            a_c = -1.5*25
        if v_0 < 0:
            a_c = 1.5*25
        v_0 = vt
        i = t2 + t1
    
    # terminasi kecepatan akhir
    vt = v_0 + a_c*(((elapsed_time_ms/1000-i)))

    # update posisi rectangle (lift)
    rect_y += vt/1000
    rect.place(x=rect_x, y=rect_y)

    ## pengulangan tiap 1 ms selama waktu yang ditempuh <= t total
    if elapsed_time_ms <= (t*1000):
        window.after(1, run_program, gerak, a, y, v_max, t1, t2, t3, t)

    ## ketika sudah menlakukan pergerakan naik/turun, akan direset untuk melanjutkan ke tujuan berikutnya
    else:
        ### RESET
        vt = 0
        v_0 = 0
        y_0 = y
        elapsed_time_ms = 0
        i = 0

        ### REDUCE WEIGHT       
        b += 1
        if b == 2:
            total_weight.pop(0)
            b = 0
        window.after(1000, move)

### VARIABEL
v_0 = 0                 # kecepatan awal
y_0 = 300               # default position
i = 0                   # mengatur pengurangan pada vt akhir (akselerasi diturunkan untuk membuat lift berhenti) : line 87
vt = 0                  # initial velocity
b = 0                   # mengatur pengurangan berat agar berat dari orang yang sudah keluar tidak ikut dihitung : line 103
berat = 0               # inisiasi berat 
elapsed_time_ms = 0     # inisiasi elapsed time milisecond
maximum_weight = 1000   # inisiasi berat maksimum 

jalur = []              # inisiasi array jalur
list_data = []          # inisiasi array data 
total_weight = []       # inisiasi array total berat 


#### TKINTER
### WINDOW
window = tk.Tk()
window.title('Program Lift!')
window.geometry('900x600')
window.resizable(False,False)

### STRING VARIABEL TKINTER
LANTAI_AWAL = tk.StringVar()
LANTAI_TUJUAN = tk.StringVar()
BERAT = tk.StringVar()

### USER SECTION
input_frame = ttk.Frame(master= window)
teks_input = ttk.Label(master=window, text='USER SECTION', font='Roboto 13 bold')
teks_input.place(x=740,y=70)

# lantai awal
awal_frame = ttk.Frame(master= input_frame)
awal_frame.pack(anchor="w", padx= 30)

label_awal = ttk.Label(master= awal_frame, text= "Lantai awal\t: ", font="Roboto 15")
label_awal.pack(side='left')

entry_awal = ttk.Entry(master= awal_frame, textvariable=LANTAI_AWAL)
entry_awal.pack(side='left')

# lantai tujuan
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

# text
kelompok_x = 0.45
kelompok = ttk.Label(master=input_frame, text='KELOMPOK 1', font='Roboto 15 bold')
kelompok.place(relx=kelompok_x, y=290 )
kelompok = ttk.Label(master=input_frame, text='1. Faiz Yasyukur Ilham / 16923091', font='Roboto 10 italic')
kelompok.place(relx=kelompok_x, y=320 )
kelompok = ttk.Label(master=input_frame, text='2. Kristofer Adrian / 16923143', font='Roboto 10 italic')
kelompok.place(relx=kelompok_x, y=340 )
kelompok = ttk.Label(master=input_frame, text='3. Muhammad Ahda Sabita / 16923219', font='Roboto 10 italic')
kelompok.place(relx=kelompok_x, y=360 )
kelompok = ttk.Label(master=input_frame, text='4. Nurman Tangguh / 16923267', font='Roboto 10 italic')
kelompok.place(relx=kelompok_x, y=380 )
kelompok = ttk.Label(master=input_frame, text='5. Rama Fitriansyah / 16923279', font='Roboto 10 italic')
kelompok.place(relx=kelompok_x, y=400 )
kelompok = ttk.Label(master=input_frame, text='6. David Ramadan / 16923283', font='Roboto 10 italic')
kelompok.place(relx=kelompok_x, y=420 )

### VISUALIZATION SECTION
visual_frame = ttk.Frame(master=window)
teks_visual = ttk.Label(master=window, text='VISUAL SECTION', font='Roboto 13 bold')
teks_visual.place(x=20,y=70)

## line : lantai
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

## rectangle : lift
# default size
rect_h = 30
rect_w = 20

# default posisition
rect_x = 10
rect_y = 300-rect_h

rect = tk.Frame(master=visual_frame, bg="gray80", relief=tk.FLAT ,height=rect_h, width=rect_w)
rect.place(x=rect_x, y=rect_y)

rect['highlightbackground'] = 'gray50'      
rect['highlightthickness'] = 2

### SECTION TERMINATION
input_frame.place(x=450,y=140, height=460, width=450)
visual_frame.place(x=10,y=70,height=600,width=450)

### TITLE
title_label = ttk.Label(master= window, text= 'PROGRAM LIFT!', font='Roboto 24 bold')
header_label = ttk.Label(master=window, text= 'KU1102 Bapak Yohanes Bimo Dwianto, M.T.', font='Roboto 12 italic')
title_label.pack(pady=5)
header_label.pack()

### WINDOW MAIN LOOP
window.mainloop()
