import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import math
import sys

"""
    KAMUS GLOBAL
        v_0 : float                         # kecepatan awal
        y_0 : float                         # default position
        i : int                             # mengatur pengurangan pada vt akhir (akselerasi diturunkan untuk membuat lift berhenti) : line 
        vt : float                          # initial velocity
        b : int                             # mengatur pengurangan berat agar berat dari orang yang sudah keluar tidak ikut dihitung : line 
        berat : float                       # inisiasi berat 
        elapsed_time_ms : float             # inisiasi elapsed time milisecond
        maximum_weight : int                # inisiasi berat maksimum 

        jalur : array of int                # inisiasi array jalur
        list_data : array of int            # inisiasi array data 
        total_weight : array of int         # inisiasi array total berat 

        LANTAI_AWAL : str
        LANTAI_TUJUAN : str
        BERAT : str
"""

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
        6. Skala (y : pixel) = (1 : 25)
"""

"""
    DESKRIPSI FUNGSI :
        1. enable_button() dan disable_button() -> mengaktifkan / menonaktifkan button ketika program berjalan 
        2. selisihAwal(data_gerak, pos)         -> menghitung selisih antara lantai saat itu dengan lantai yang akan dituju 
                                                    untuk pencarian jarak lantai terdekat dengan parameter (data_gerak, pos) dalam perhitungan algoritma jalur
        3. updateData(pos, gerak, data_gerak)   -> menambah urutan gerak dan mengurangi data_gerak jika sudah dilalui dengan parameter (pos, gerak, data_gerak)
                                                    dalam perhitungan algoritma jalur
        4. position(data_gerak, pos)            -> mencari posisi yang akan dituju dengan pertimbangan jarak lantai terdekat setelah dihitung oleh selisihAwal(data_gerak, pos)
                                                    dengan parameter (data_gerak, pos) dalam perhitungan algoritma jalur
        5. jalurLift(data_gerak)                -> main function dari perhitungan algoritma jalur untuk mencari array jalur selanjutnya dengan menggunakan 
                                                    pengulangan fungsi position dan updateData
        6. format_time(miliseconds)             -> mengatur format untuk indikator waktu dengan parameter (elapsed_time_ms as miliseconds)
        7. format_speed(vt)                     -> mengatur format untuk indikator speed dengan parameter (vt) 
        8. format_floor(rect_y)                 -> mengatur format untuk indikator lantai dengan parameter (rect_y)
        9. add()                                -> MAIN FUNCTION
                                                    - fungsi untuk menyimpan data dari input pengguna kemudian mengkalkulasikan urutan jalur selanjutnya 
                                                    - mengkalkulasikan massa sehingga beban lift tidak melebihi maksimum massa yang ditentukan (1000 kg) 
                                                    - memunculkan alert untuk input diluar kriteria
                                                    - mereset entry untuk pengisian selanjutnya
        10. move()                              -> MAIN FUNCTION
                                                    - mereset indikator waktu dan speed
                                                    - menginisiasikan disable_button() sehingga user tidak dapat menambahkan data ketika program berjalan
                                                    - menyimpan rumus kinematika untuk pergerakan lift pada fungsi run_program(gerak, a, y, v_max, t1, t2, t3, t)
        11. run_program(gerak, a, y, v_max, t1, t2, t3, t)      -> Pergerakan lift
                                                                    - mengatur update posisi koordinat dari lift
                                                                    - mengatur waktu (elapsed time in miliseconds)
                                                                    - mengatur update indikator time, speed, floor
                                                                    - mengatur pengurangan berat ketika user sudah keluar lift (not optimal)
"""

#### FUNCTION
### ENABLE / DISABLE BUTTON
def enable_button():
    button_add.config(state="active")
    button_start.config(state="active")

def disable_button():
    button_add.config(state="disabled")
    button_start.config(state="disabled")

### FUNGSI ALGORITMA JALUR
def selisihAwal(data_gerak, pos):

    """
        KAMUS LOKAL
            selisih : array of int
    """

    selisih = [abs(pos-subdata[0]) for subdata in data_gerak if subdata]
    return selisih    

def updateData(pos, gerak, data_gerak):

    gerak.append(pos)
    for i in range(len(data_gerak)):
        if pos == data_gerak[i][0]:
            data_gerak[i].pop(0)
    data_gerak = [subdata for subdata in data_gerak if subdata]
    return data_gerak

def position(data_gerak, pos):
    selisih = selisihAwal(data_gerak, pos)
    orang = selisih.index(min(selisih))
    pos = data_gerak[orang][0]
    return pos

def jalurLift(data_gerak):

    """
        KAMUS LOKAL
            pos : int                   # position -> menunjukkan posisi lantai untuk perhitungan algoritma jalur
            gerak : array of int        # array dari lantai yang akan dituju
    """

    global y_0
    gerak = []
    pos = int(y_0/75) 
    pos = position(data_gerak, pos)

    while data_gerak:
        pos = position(data_gerak, pos)
        data_gerak = updateData(pos, gerak, data_gerak)
    return gerak, data_gerak

### FORMATTING
def format_time(milliseconds):

    """
        KAMUS LOKAL
            hours, second, miliseconds, minute : floor
    """

    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"

def format_speed(vt):

    """
        KAMUS LOKAL
            speed : floor
    """

    speed = abs(vt / 25) 
    return f"{speed:.2f}"

def format_floor(rect_y):

    """
        KAMUS LOKAL
            floor : floor
    """

    if rect_y <= 75:
        floor = 7
    elif 75 < rect_y <= 150:
        floor = 6
    elif 150 < rect_y <= 225:
        floor = 5
    elif 225 < rect_y <= 300:
        floor = 4
    elif 300 < rect_y <= 375:
        floor = 3
    elif 375 < rect_y <= 450:
        floor = 2
    elif 450 < rect_y <= 525:
        floor = 1
    return floor

### FUNGSI ADD DATA & SAVE DATA
def add():

    """
        KAMUS LOKAL 
            a,b,c : int
            data : array [a,b,c] of int
    """

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
            jika tidak, akan dimunculkan alert dan data yang baru saja diinput akan direset, data yang sudah di save tidak akan ikut direset
        """
        
        if data[0] != data[1] and 0 < data[0] < 8 and 0 < data[1] < 8:          
            if (sum(total_weight)+berat) < maximum_weight:
                total_weight.append(berat)  
                list_data.append(data)                                             

                data_gerak = [[subdata[0], subdata[1]] for subdata in list_data]
                jalur, data_gerak = jalurLift(data_gerak)

                # print("\nJalur lift", jalur)                                        # menunjukkan list jalur yang akan ditempuh lift
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
    global jalur, k, i, y_0, y, p, b, total_weight, a, list_data

    SPEED.set("0.00")
    ELPAPSEDTIME.set("00:00.000")
    disable_button()

    """
        KAMUS LOKAL
            y : int
            v_max : float
            t : float
            t1 : float
            t2 : float
            t3 : float
    """

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
        t3 = t1                                           # t3 = time saat menempuh jarak 3/3 y

        ## RUN PROGRAM : GERAK LIFT 
        run_program(gerak, a, y, v_max, t1, t2, t3, t)
    else:
        enable_button()
        list_data = []

def run_program(gerak, a, y, v_max, t1, t2, t3, t):
    global elapsed_time_ms, rect_y, rect_x, vt, v_0, y_0, p, b, total_weight, a_c, i

    """
        KAMUS LOKAL
            a_c : float
    """

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

    # update indikator
    time_update = format_time(elapsed_time_ms)
    speed_update = format_speed(vt)
    floor_update = format_floor(rect_y)

    ELPAPSEDTIME.set(time_update)
    SPEED.set(speed_update)
    FLOOR.set(floor_update)

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
        window.after(2000, move)

### VARIABEL
v_0 = 0                 # kecepatan awal
y_0 = 300               # default position
i = 0                   # mengatur pengurangan pada vt akhir (akselerasi diturunkan untuk membuat lift berhenti) : line 87
vt = 0                  # initial velocity
b = 0                   # mengatur pengurangan berat agar berat dari orang yang sudah keluar tidak ikut dihitung : line 103
berat = 0               # inisiasi berat 
elapsed_time_ms = 0     # inisiasi elapsed time milisecond
maximum_weight = 1000   # inisiasi berat maksimum 

list_data = []          # inisiasi array data 
jalur = []              # inisiasi array jalur
total_weight = []       # inisiasi array total berat 

#### TKINTER
### WINDOW
window = tk.Tk()
window.title('Program Lift!')
window.geometry('895x700')
window.resizable(False,False)

### STRING VARIABEL TKINTER
LANTAI_AWAL = tk.StringVar()
LANTAI_TUJUAN = tk.StringVar()
BERAT = tk.StringVar()
ELPAPSEDTIME = tk.StringVar()
SPEED = tk.StringVar()
FLOOR = tk.StringVar()

### USER SECTION
input_frame = ttk.Frame(master= window)
teks_input = ttk.Label(master=window, text='USER SECTION', font='Roboto 13 bold')
teks_input.place(x=760,y=110)

## user input
user_frame = tk.Frame(master=input_frame, width=400, height=100, highlightbackground='gray70', highlightthickness=2)
user_frame.pack_propagate(False)
user_frame.pack(padx=5,anchor='w')

# lantai awal
awal_frame = ttk.Frame(master= user_frame)
awal_frame.pack(anchor="w", pady=3, padx=2)

label_awal = ttk.Label(master= awal_frame, text= "Lantai awal\t: ", font="Roboto 15")
label_awal.pack(side='left')

entry_awal = ttk.Entry(master= awal_frame, textvariable=LANTAI_AWAL)
entry_awal.pack(side='left')

# lantai tujuan
tujuan_frame = ttk.Frame(master= user_frame)
tujuan_frame.pack(anchor="w", pady=3, padx=2)

label_tujuan = ttk.Label(master= tujuan_frame, text= "Lantai tujuan\t: ", font="Roboto 15")
label_tujuan.pack(side='left')

entry_tujuan = ttk.Entry(master= tujuan_frame, textvariable=LANTAI_TUJUAN)
entry_tujuan.pack(side='left')

# berat
berat_frame = ttk.Frame(master= user_frame)
berat_frame.pack(anchor="w", pady=3, padx=2)

label_berat = ttk.Label(master= berat_frame, text= "Berat badan\t: ", font="Roboto 15")
label_berat.pack(side='left')

entry_berat = ttk.Entry(master= berat_frame, textvariable=BERAT)
entry_berat.pack(side='left')

## indicator and button
indicatton_frame = tk.Frame(master=input_frame, height=160)
indicatton_frame.pack_propagate(False)
indicatton_frame.pack(padx=5,pady=10, fill='x')

indicator_frame = tk.Frame(master=indicatton_frame, width=300, highlightbackground='gray70', highlightthickness=2)
indicator_frame.pack_propagate(False)
indicator_frame.pack(pady=5, expand=True, fill='y', side='left')

button_frame = tk.Frame(master=indicatton_frame, width=150)
button_frame.pack_propagate(False)
button_frame.pack(expand=True, fill='y', side='left')

# button
button_add = tk.Button(master= button_frame, text = "TAMBAHKAN", font="Roboto 10 bold", command= add)   # menambahkan data orang
button_add.pack(expand=True, fill='x', padx=8,pady=5, ipady=20)

button_start = tk.Button(master= button_frame, text = "JALANKAN!",font="Roboto 10 bold ", command= move)      # VISUALISASIKAN!
button_start.pack(expand=True, fill='x', padx=8, pady=5, ipady=20)

# indicator
#   time
time_frame = tk.Frame(master=indicator_frame,height= 50)
time_frame.pack_propagate(False)
time_frame.pack(pady=5, fill='x')

time_label = ttk.Label(master=time_frame, text="Elapsed Time : ", font="Courier 12")
time_label.pack(side='left')

ELPAPSEDTIME.set("00:00:00.000")
timeIndicator_label = ttk.Label(master=time_frame, textvariable=ELPAPSEDTIME, font="Courier 12")
timeIndicator_label.pack(side='left')

#   speed
speed_frame = tk.Frame(master=indicator_frame,height= 50)
speed_frame.pack_propagate(False)
speed_frame.pack(padx=5, fill='x')

speed_label = ttk.Label(master=speed_frame, text="Speed (m/s)  : ", font="Courier 12")
speed_label.pack(side='left')

SPEED.set("0.00")
speedIndicator_label = ttk.Label(master=speed_frame, textvariable=SPEED, font="Courier 12")
speedIndicator_label.pack(side='left')

#   floor
floor_frame = tk.Frame(master=indicator_frame,height= 50)
floor_frame.pack_propagate(False)
floor_frame.pack(padx=5, pady=5, fill='x')

floor_label = ttk.Label(master=floor_frame, text="floor\t     : ", font="Courier 12")
floor_label.pack(side='left')

FLOOR.set(4)
floorIndicator_label = ttk.Label(master=floor_frame, textvariable=FLOOR, font="Courier 12")
floorIndicator_label.pack(side='left')

# text
kelompok = ttk.Label(master=input_frame, text='KELOMPOK 1', font='Roboto 15 bold')
kelompok.place(y=410 )
anggota = ttk.Label(
    master=input_frame, 
    text='''1. Faiz Yasyukur Ilham / 16923091
2. Kristofer Adrian / 16923143
3. Muhammad Ahda Sabila / 16923219
4. Nurman Tangguh / 16923267
5. Rama Fitriansyah / 16923279
6. David Ramadan / 16923283
            ''', 
    font='Roboto 10 italic')
anggota.place(y=440 )

### VISUALIZATION SECTION
visual_frame = tk.Frame(master=window, highlightbackground="gray70", highlightthickness=2)
teks_visual = ttk.Label(master=window, text='VISUAL SECTION', font='Roboto 13 bold')
teks_visual.place(x=8,y=110)

## line : lantai
line_x = 40
height_line, width_line = 2, 410
# lt 7
text7 = tk.Label(master=visual_frame,text="Floor 7", font="Roboto 10 italic")
text7.place(x=420-18, y=75 - 20)
line7 = tk.Frame(master=visual_frame, bg='black',height=height_line, width=width_line)
line7.place(x=line_x,y=75)

# lt 6
text6 = tk.Label(master=visual_frame,text="Floor 6", font="Roboto 10 italic")
text6.place(x=420-18, y=150 - 20)
line6 = tk.Frame(master=visual_frame, bg='black',height=height_line, width=width_line)
line6.place(x=line_x,y=150)

# lt 5
text5= tk.Label(master=visual_frame,text="Floor 5", font="Roboto 10 italic")
text5.place(x=420-18, y=225 - 20)
line5 = tk.Frame(master=visual_frame, bg='black',height=height_line, width=width_line)
line5.place(x=line_x,y=225)

# lt 4
text4 = tk.Label(master=visual_frame,text="Floor 4", font="Roboto 10 italic")
text4.place(x=420-18, y=300- 20)
line4 = tk.Frame(master=visual_frame, bg='black',height=height_line, width=width_line)
line4.place(x=line_x,y=300)

# lt 2
text3 = tk.Label(master=visual_frame,text="Floor 3", font="Roboto 10 italic")
text3.place(x=420-18, y=375- 20)
line3 = tk.Frame(master=visual_frame, bg='black',height=height_line, width=width_line)
line3.place(x=line_x,y=375)

# lt 2
text2 = tk.Label(master=visual_frame,text="Floor 2", font="Roboto 10 italic")
text2.place(x=420-18, y=450 - 20)
line2 = tk.Frame(master=visual_frame, bg='black',height=height_line, width=width_line)
line2.place(x=line_x,y=450)

# lt 1
text1 = tk.Label(master=visual_frame,text="Floor 1", font="Roboto 10 italic")
text1.place(x=420-18, y=525 - 20)
line1 = tk.Frame(master=visual_frame, bg='black',height=height_line, width=width_line)
line1.place(x=line_x,y=525)

## rectangle : lift
# default size
rect_h = 30
rect_w = 20

# default posisition
rect_x = 10
rect_y = 300-rect_h

rect = tk.Frame(
    master=visual_frame, 
    bg="gray80",height=rect_h, 
    width=rect_w, 
    highlightbackground='gray50', 
    highlightthickness='2'
    )   
rect.place(x=rect_x, y=rect_y)

### SECTION TERMINATION
input_frame.place(x=480,y=140, height=540, width=420)
visual_frame.place(x=10,y=140,height=540,width=460)

### TITLE
title_label = ttk.Label(master= window, text= 'PROGRAM LIFT!', font='Roboto 24 bold')
header_label = ttk.Label(master=window, text= 'KU1102 Bapak Yohanes Bimo Dwianto, M.T.', font='Roboto 12 italic')
title_label.pack(pady=5)
header_label.pack()

### WINDOW MAIN LOOP
window.mainloop()







