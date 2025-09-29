import PySimpleGUI as sg
import webbrowser as wb
import mysql.connector as sql
import bcrypt as phash
from datetime import datetime
import re
import requests
from io import BytesIO
from PIL import Image

ver = '1.5.0'

#bypassloginmertdebug = True

colors = {'grey':'#23272a', 'green-b':'#406ba1', 'madebywsd':'#505457', 'green-b-not-available':'#8cb8a4', 'undername':'#696d70'}

accountdetails = {
    "accountName":"",
    "charName":"",
    "charRank":"",
    "charBeosztas":"",
    "adminLevel":,
    "pfplink":"",
    "pfpdata":b""
}

try:
    database = sql.connect(host="localhost", user="root", password="", database="lrszapp")
except sql.Error:
    sg.popup("Adatbázis hiba! Kérlek vedd fel a kapcsolatot az alosztályvezetőkkel, vagy WSD-vel.", icon='img/icon.ico', title="lrsz app | Adatbázis hiba", button_color=colors['green-b'], background_color=colors['grey'])
    #print("Adatbázis nemmegy helo")
    exit()
    

cursor=database.cursor()
def login(account, password):
    cursor.execute("SELECT accPass FROM accounts WHERE accName=%s", (account,))
    eredmeny = cursor.fetchone()
    if eredmeny is not None:
        if phash.checkpw(password.encode("utf-8"), eredmeny[0].encode("utf-8")):
            return "oks"
        else:
            return "nemoks"
    else:
        return "nonetype"
    

def pfpfrissit():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    #print(accountdetails['pfplink'])

    response = requests.get(accountdetails['pfplink'], headers=headers)

    kepbyteokban = response.content

    #print(kepbyteokban)
    kep = Image.open(BytesIO(kepbyteokban)).resize((100,100))

    byte_io = BytesIO()
    kep.save(byte_io, format="PNG")
    #kep.save("asd.png", format="PNG")

    byte_io.seek(0)

    #calc_window()
    return byte_io.read()

# kalkulátor ablak layout
layoutCalcTab = [
    # ----------------------------- FŐ, FELSŐ RÉSZ, Ő NEM FOG VÁLTOZNI MAJD -----------------------------
    #[
    #    sg.Text("", background_color=colors['grey'], font='Calibri 11', key="-ACC_DATA-"),
    #],

    #[
    #    sg.Text("", background_color=colors['grey'], font='Calibri 11', key="-RANK_DATA-")
    #],

    #[
        #sg.Text('asd', font='Calibri 5', text_color=colors['grey'], background_color=colors['grey']), # space lol haha 
        #sg.Image('img/acc3.png', size=(50, 50), background_color=colors['grey'], key='-ACC_IMG-', enable_events = True),
    #    sg.Button('', image_source='img/acc3.png', button_color=colors['grey'], border_width=0, key='-ACC_BUTT-', enable_events=True)
    #],

    #[
    #    sg.Push(background_color=colors['grey']),
    #    sg.Image('img/icon2.png', background_color=colors['grey']),
    #    sg.Text('lrszapp', font='Calibri 22', background_color=colors['grey']),
    #    sg.Push(background_color=colors['grey']),
    #],

    [
       sg.Text('asd', font='Calibri 5', text_color=colors['grey'], background_color=colors['grey']), # space lol haha 
    ],

    [
        sg.Push(background_color=colors['grey']), # push for align
        sg.Text('', text_color=colors['green-b'], tooltip='', background_color=colors['grey'], font='Calibri 25'), #text
        sg.Push(background_color=colors['grey']), # push for align
        sg.Image('img/logo.png', background_color=colors['grey'], key='-LOGO_IMG-', enable_events = True), #logo
        sg.Push(background_color=colors['grey']), # push for align
        sg.Text('', background_color=colors['grey'], font='Calibri 25'), #text2
        sg.Push(background_color=colors['grey']), # push for align
    ], # logo, ketto diszito szoveg

    #[
        #sg.Push(background_color=colors['grey']), # push for align
        #sg.Text('a', background_color=colors['grey'], font='Calibri 15',),
        #sg.Push(background_color=colors['grey']) # push for align
   # ], #szoveg gomb felett

    #[
   #     sg.Push(background_color=colors['grey']), # push for align
   #     sg.Button('Kalkulátor', border_width=0, button_color=colors['green-b-not-available'], disabled=True, size=(26, 1), font="Calibri 18", key='-MODE_CALC-'),
   #     sg.Push(background_color=colors['grey']), # push for align
   #     sg.Button('Jelentésíró', border_width=0, button_color=colors['green-b'], size=(26, 1), font="Calibri 18", key='-MODE_REP-', disabled=True),
   #     sg.Push(background_color=colors['grey']), # push for align
   # ], #ket gomb


    [sg.Text('asd', font='Calibri 25', text_color=colors['grey'], background_color=colors['grey'])], # space lol haha

    # ----------------------------- INNENTŐL LEFELE LESZ A MÓD SPECIFIKUS CUCCOK -----------------------------

    [ # Kezdés text, és két input field. 
        sg.Push(background_color=colors['grey']),
        sg.Text('   Kezdés:       ', font='Calibri 14', background_color=colors['grey']), 
        sg.Input( border_width=0, size=(32, 1), justification="center", key='-INPUT_T_START-'), 
        sg.Button('', image_source='img/naptar2.png', button_color=colors['grey'], border_width=0, enable_events=True, key='-START_DATE_BUT-'),
        sg.Button('', image_source='img/naptar3.png', button_color=colors['grey'], border_width=0, enable_events=True, key='-START_DATE_TIME_BUT-'),
        #sg.Text('óra', font='Calibri 10', background_color=colors['grey']), 
        #sg.Input(border_width=0, size=(3, 1), justification="center", key='-INPUT_M_START-'), 
        #sg.Text('perc', font='Calibri 10', background_color=colors['grey']),
        sg.Push(background_color=colors['grey'])

    ], 

    [ # A vége text, két input field
        sg.Push(background_color=colors['grey']),
        sg.Text('   Befejezés:  ', font='Calibri 14', background_color=colors['grey']), 
        sg.Input(border_width=0, size=(32, 1), justification="center", key='-INPUT_T_END-'), 
        sg.Button('', image_source='img/naptar2.png', button_color=colors['grey'], border_width=0, enable_events=True, key='-END_DATE_BUT-'),
        sg.Button('', image_source='img/naptar3.png', button_color=colors['grey'], border_width=0, enable_events=True, key='-END_DATE_TIME_BUT-'),
        #sg.Text('óra', font='Calibri 10', background_color=colors['grey']), 
        #sg.Input(border_width=0, size=(3, 1), justification="center", key='-INPUT_M_END-'), 
        #sg.Text('perc', font='Calibri 10', background_color=colors['grey']),
        sg.Push(background_color=colors['grey']),
    ],

    [ # Bizonyíték input field
        sg.Push(background_color=colors['grey']),
        sg.Text('Bizonyíték:  ', font='Calibri 14', background_color=colors['grey']), 
        sg.Input(border_width=0, size=(41,1), justification="center", key='-BIZI-'),
        sg.Push(background_color=colors['grey']),
    ],

    [ # feltöltés gomb
        sg.Push(background_color=colors['grey']),
        sg.Button('Számítás & Feltöltés', border_width=0,button_color=colors['green-b'], size=(26, 1), font="Calibri 18", key="-CALC_AND_UPLOAD-", enable_events=True),
        #sg.Text('a', font='Calibri 8', text_color=colors['grey'], background_color=colors['grey']),
        sg.Push(background_color=colors['grey']),
    ],

    [
        sg.Text('A számítás eredménye: ', font='Calibri 14', background_color=colors['grey'], expand_x=True, justification="center", visible=False, key="-RESULT_TEXT-")
    ],

    # szoveg
    # a szoveg alapbol ures lesz, kalkulalas utan lesz update-elve, 
    # nem visibilityvel lesz megoldva mint 0.49.5 elott. szar rendszer, raadasul buggos is

    [
        sg.Text('', font='Calibri 14', background_color=colors['grey'], expand_x=True, justification="center", visible=False, key="-CONGRAT_TEXT-"),
    ],

    [
        sg.VPush(background_color=colors['grey']),
        
    ],

    [
        sg.Text('Log:', pad=(30, 20), background_color=colors['grey'], visible=False, key="-ERROR_LOG-")
    ],
    
    [
        sg.Text("", text_color=colors['madebywsd'], background_color=colors['grey'], font='Arial 8', key="-ACC_DATA-"),
        #sg.Text("|", text_color=colors['madebywsd'], background_color=colors['grey'], font='Arial 8'),
        #sg.Text("", text_color=colors['madebywsd'], background_color=colors['grey'], font='Arial 8', key="-RANK_DATA-"),
        #sg.Text("|", text_color=colors['madebywsd'], background_color=colors['grey'], font='Arial 8'),
        #sg.Text("", text_color=colors['madebywsd'], background_color=colors['grey'], font='Arial 8', key="-BEOSZT_DATA-"),
        sg.Push(background_color=colors['grey']),
        sg.Text('Coded By WSD  |  V'+ver, font='Arial 8', justification='right', text_color=colors['madebywsd'], background_color=colors['grey'], enable_events=True, key='WSD')
    ]
]

layoutLowAdminTab = [
    [sg.Text("szia - admin 1")]
]
layoutHighAdminTab = [
    [sg.Text("szia - admin 2")]
]

calcTab = sg.Tab("Kalkulátor", layoutCalcTab, background_color=colors['grey'])
#profileTab = sg.Tab("Profilod", layoutProfileTab, background_color=colors['grey'])
lowAdminTab = sg.Tab("Mentor", layoutLowAdminTab, background_color=colors['grey'])
highAdminTab = sg.Tab("Alosztályvezető", layoutHighAdminTab, background_color=colors['grey'])

tabs = [calcTab]

# login ablak layout
login_layout = [
    [
        sg.Text('', size=(1, 1), background_color=colors['grey'])
    ],

    [
        sg.Push(background_color=colors['grey']), # push for align
        #sg.Text('', text_color=colors['green-b'], tooltip='', background_color=colors['grey'], font='Calibri 25'), #text
        sg.Push(background_color=colors['grey']), # push for align
        sg.Image('img/logo.png', background_color=colors['grey'], key='-LOGO_IMG-', enable_events = True), #logo
        sg.Push(background_color=colors['grey']), # push for align
        #sg.Text('', background_color=colors['grey'], font='Calibri 25'), #text2
        sg.Push(background_color=colors['grey']), # push for align
    ], # logo

    #[sg.Text('sad', font='Calibri 25', text_color=colors['grey'], background_color=colors['grey'])], # space lol haha

    [ #felhasználónév-text
        sg.Push(background_color=colors['grey']),
        sg.Text('Felhasználónév', font='Calibri 14', background_color=colors['grey']), 
        sg.Push(background_color=colors['grey'])
    ],

    [ # felhasználónév-input
        sg.Push(background_color=colors['grey']),
        sg.Input(size=(28,2), justification="center", key="username", enable_events=True, border_width=0),
        sg.Push(background_color=colors['grey'])

    ], 

    [ # jelszó-text
        sg.Push(background_color=colors['grey']),
        sg.Text('Jelszó', font='Calibri 14', background_color=colors['grey']), 
        sg.Push(background_color=colors['grey']),
    ],

    [ # jelszó-input
        sg.Push(background_color=colors['grey']),
        sg.Input(size=(28,2), justification="center", key="password", password_char="*", enable_events=True, border_width=0),
        sg.Push(background_color=colors['grey'])

    ], 

    [ #hely
        sg.Push(background_color=colors['grey']),
    #    sg.Text('', font='Calibri 14', background_color=colors['grey']), 
    #    sg.Input(border_width=0, size=(29,1), justification="center", key='-BIZI-'),
        sg.Push(background_color=colors['grey']),
    ],

    [ # bejelentkezés gomb
        sg.Push(background_color=colors['grey']),
        sg.Button('Bejelentkezés', border_width=0,button_color=colors['green-b'], size=(26, 1), font="Calibri 18", key="-LOGIN-", enable_events=True),
        sg.Push(background_color=colors['grey']),
    ],

    [
        sg.Text('A számítás eredménye: ', font='Calibri 14', background_color=colors['grey'], expand_x=True, justification="center", visible=False, key="-RESULT_TEXT-")
    ],

    # szoveg
    # a szoveg alapbol ures lesz, kalkulalas utan lesz update-elve, 
    # nem visibilityvel lesz megoldva mint 0.49.5 elott. szar rendszer, raadasul buggos is

    [
        sg.Text('', font='Calibri 14', background_color=colors['grey'], expand_x=True, justification="center", visible=False, key="-CONGRAT_TEXT-"),
    ],

    #[
    #    sg.VPush(background_color=colors['grey']),
        
    #],

    [
        sg.Text('Log:', pad=(30, 20), background_color=colors['grey'], visible=False, key="-ERROR_LOG-")
    ],
    
    [
        sg.VPush(background_color=colors['grey']),  
    ],

    [
        sg.Push(background_color=colors['grey']),
        sg.Text('Coded By WSD  |  V'+ver, font='Arial 8', justification='right', text_color=colors['madebywsd'], background_color=colors['grey'], enable_events=True, key='WSD')
    ]
]
# register ablak layout
register_layout = [
    [
        sg.Text('', size=(1, 1), background_color=colors['grey'])
    ],

    [
        sg.Push(background_color=colors['grey']), # push for align
        #sg.Text('', text_color=colors['green-b'], tooltip='', background_color=colors['grey'], font='Calibri 25'), #text
        sg.Push(background_color=colors['grey']), # push for align
        sg.Image('img/logo.png', background_color=colors['grey'], key='-LOGO_IMG-', enable_events = True), #logo
        sg.Push(background_color=colors['grey']), # push for align
        #sg.Text('', background_color=colors['grey'], font='Calibri 25'), #text2
        sg.Push(background_color=colors['grey']), # push for align
    ], # logo

    [ # jelszó-text
        sg.Push(background_color=colors['grey']),
        sg.Text('Állítsd be a jelszavad', font='Calibri 14', background_color=colors['grey']), 
        sg.Push(background_color=colors['grey']),
    ],

    [ # jelszó-input
        sg.Push(background_color=colors['grey']),
        sg.Input(size=(28,2), justification="center", key="reg_password", password_char="*", enable_events=True, border_width=0),
        sg.Push(background_color=colors['grey'])

    ], 

    [ #hely
        sg.Push(background_color=colors['grey']),
        sg.Push(background_color=colors['grey']),
    ],

    [ # bejelentkezés gomb
        sg.Push(background_color=colors['grey']),
        sg.Button('Regisztráció', border_width=0,button_color=colors['green-b'], size=(26, 1), font="Calibri 18", key="-REGISTER-", enable_events=True),
        sg.Push(background_color=colors['grey']),
    ],

    [
        sg.Text('A számítás eredménye: ', font='Calibri 14', background_color=colors['grey'], expand_x=True, justification="center", visible=False, key="-RESULT_TEXT-")
    ],

    # szoveg
    # a szoveg alapbol ures lesz, kalkulalas utan lesz update-elve, 
    # nem visibilityvel lesz megoldva mint 0.49.5 elott. szar rendszer, raadasul buggos is

    #[
    #    sg.Text('', font='Calibri 14', background_color=colors['grey'], expand_x=True, justification="center", visible=False, key="-CONGRAT_TEXT-"),
    #],

    [
        sg.VPush(background_color=colors['grey']),
        
    ],

    [
        sg.Text('Log:', pad=(30, 20), background_color=colors['grey'], visible=False, key="-ERROR_LOG-")
    ],
    
    [
        sg.Push(background_color=colors['grey']),
        sg.Text('Coded By WSD  |  V'+ver, font='Arial 8', justification='right', text_color=colors['madebywsd'], background_color=colors['grey'], enable_events=True, key='WSD')
    ]
]
# lejelentések ablak layout
#test.py-ben van példa, illetve https://chatgpt.com/share/68061d9b-4880-800d-9e15-fbe54fc84895


def calc_window():
    kozep = sg.Column([
            [
                sg.Text(accountdetails['charName'], font=("Helvetica", 26), background_color=colors['grey'])
            ],
            [
                sg.Text(f"{accountdetails['charRank']} | {accountdetails['charBeosztas']}", font=("Helvetica", 14), text_color=colors['undername'], background_color=colors['grey'])
            ]
        ], background_color=colors['grey'], size=(650, 650), pad=((0, 0),(20, 0))
    )

    jobboldal = sg.Column([
            [
                sg.Image("img/logo.png", background_color=colors['grey'])
            ]
        ], background_color=colors['grey'], size=(160, 650)
    )   

    baloldal = sg.Column(
        [
            [
                #sg.Image(data=accountdetails['pfpdata'])
                sg.Image("asd.png")
            ],
            [
                sg.Text(accountdetails['accountName'], font=("Helvetica", 8), text_color=colors['undername'], background_color=colors['grey'], justification="center", size=16)
            ],
            [
                sg.Button("Profilkép beállítása", auto_size_button=False, size=(12, 2), border_width=0, button_color=colors['green-b'], key='-PFP_BUT-', enable_events=True)
            ]
        ], background_color=colors['grey'], size=(120, 650), element_justification="top", pad=((10, 0),(20, 0))
    )

    layoutProfileTab = [
        [baloldal, kozep, sg.Push(background_color=colors['grey']), jobboldal]
    ]

    tabs.append(sg.Tab("Profilod", layoutProfileTab, background_color=colors['grey']))

    if accountdetails['adminLevel'] == 1:
        tabs.append(lowAdminTab)
        #print("appendelve a low admin")
    elif accountdetails['adminLevel'] == 2:
        #print("appendelve a high admin")
        tabs.append(highAdminTab)

    layoutMain = [
        [sg.TabGroup([tabs], expand_x=True, expand_y=True, background_color=colors['grey'], border_width=0, selected_background_color=colors['green-b'], tab_background_color=colors['grey'], title_color="#ffffff")]
    ]

    mw = sg.Window(
    'lrszapp',
    layoutMain, 
    icon='img/icon.ico', 
    size=(1000, 650), 
    resizable=False, 
    margins=(0, 0), 
    background_color=colors['grey'])

    whileFlag = False

    def errorText(text):
        szoveg = str(text)
        mw['-ERROR_LOG-'].update(visible=True)
        mw['-ERROR_LOG-'].update('Log: ' + szoveg)

    def calc():
        mw['-ERROR_LOG-'].update(visible=False)


        if len(values['-INPUT_T_START-'])<=0 or len(values['-INPUT_T_END-'])<=0 or len(values['-BIZI-'])<=0:
            errorText("Nem töltötted ki mindegyik mezőt!")
            #print(len(values['-INPUT_T_START-']))
            #print(len(values['-INPUT_T_END-']))
            #print(len(values['-BIZI-']))
        else:
            badValue = False
            time1 = values['-INPUT_T_START-']
            time2 = values['-INPUT_T_END-']
            time_format = "%Y-%m-%d %H:%M:%S"
            try:
                time1 = datetime.strptime(time1.strip(), time_format)
            except ValueError:
                errorText("Nem megfelelő idő formátum, vagy nem időt adtál meg! (helyes formátum: 2025-01-01 12:00:00)")
                badValue = True


            try:
                time2 = datetime.strptime(time2.strip(), time_format)
            except ValueError:
                errorText("Nem megfelelő idő formátum, vagy nem időt adtál meg! (helyes formátum: 2025-01-01 12:00:00)")
                badValue = True

            if not badValue:
                delta = time2 - time1

                minutes = delta.total_seconds() / 60
                bekuldes(minutes)

    def bekuldes(percek):
        #adatok hogy ne legyen kurva hosszú
        accName = str(accountdetails['accountName'])
        charName = str(accountdetails['charName'])
        startDate = str(values['-INPUT_T_START-'])
        endDate = str(values['-INPUT_T_END-'])
        deltaMin = int(percek)
        bizi = str(values['-BIZI-'])

        #print("ittvannak az adataim: " + accName + charName + startDate + endDate + deltaMin + bizi)

        try:
            cursor.execute("INSERT INTO reports (accName, charName, startDate, endDate, deltaMin, bizi) VALUES (%s, %s, %s, %s, %s, %s)", (accName, charName, startDate, endDate, deltaMin, bizi))
            database.commit()
        except Exception:
            hibatext = "Valami hiba történt. Kérlek, vedd fel a kapcsolatot az alosztályvezetővel, vagy WSD-vel."
            sg.popup(hibatext, icon='img/icon.ico', title="lrsz app | Adatbázis hiba", button_color=colors['green-b'], background_color=colors['grey'])
    while True:

    # -------- alap dolgok --------
        event, values = mw.read(timeout=100)

        if not whileFlag:
            mw["-ACC_DATA-"].update(f"logged in as: {accountdetails['accountName']}")
            #mw["-RANK_DATA-"].update(f"{accountdetails['charRank']}")
            #mw["-BEOSZT_DATA-"].update(f"{accountdetails['charBeosztas']}")
            whileFlag = True
        

        if event == sg.WIN_CLOSED:
            break
        # -------- end --------

        # -------- ha ráklikkelsz a logóra, megnyitja a jelentés részt fórumnál. ha már jelentésíró, legyen ilyen funkció is
        if event == '-LOGO_IMG-':
            wb.open('https://forum.see-game.com/forums/jelentesek.571/', 1, 1)
        # -------- end --------

        if event == '-ACC_BUTT-':
            print(f"{accountdetails['accountName']}, {accountdetails['charBeosztas']}, {accountdetails['charName']}, {accountdetails['charRank']}")

        if event == '-CALC_AND_UPLOAD-':
            if not len(values['-BIZI-'])<=0:
                #errorText("Ne felejtsd el csatolni a bizonyítékot!")
                pattern = r"^(https://|www\.)"
                if re.match(pattern, values['-BIZI-']):
                    mw["-ERROR_LOG-"].update(visible=False)
                    calc()
                else:
                    errorText("Nem linket csatoltál bizonyítéknak!")
            else:
                errorText("Nem csatoltál bizonyítékot!")


        if event == '-START_DATE_BUT-':
            mw['-INPUT_T_START-'].update(f'{datetime.now().strftime("%Y-%m-%d")} ')

        if event == '-END_DATE_BUT-':
            mw['-INPUT_T_END-'].update(f'{datetime.now().strftime("%Y-%m-%d")} ')

        if event == '-START_DATE_TIME_BUT-':
            mw['-INPUT_T_START-'].update(f'{datetime.now().strftime("%Y-%m-%d %H:%M")}:00')

        if event == '-END_DATE_TIME_BUT-':
            mw['-INPUT_T_END-'].update(f'{datetime.now().strftime("%Y-%m-%d %H:%M")}:00')

        if event == '-PFP_BUT-':
            # buggos még

            link = ""
            link = sg.popup_get_text("Kérlek add meg a profilkép direkt elérési linkjét! (pl: www.kep.hu/kep1.png)", icon='img/icon.ico', title="lrsz app | Profilkép beállítás", button_color=colors['green-b'], background_color=colors['grey'])
            if len(link)>0:
                pattern = r"^(https://|www\.)"
                if re.match(pattern, link):
                    csoda
                else:
                    sg.PopupOK("Nem linket adtál meg!", icon='img/icon.ico', title="lrsz app | Hiba", button_color=colors['green-b'], background_color=colors['grey'])
        
        
        
        
        #húsvéti tojás UwU >_< XDDDDDDDDDDDDDD
        if event == 'WSD':
            wb.open('https://i.postimg.cc/R069CSHg/unknown.png', 1, 1)
    mw.close()

def login_window():
    mw = sg.Window(
        'lrszapp | Bejelentkezés',
        login_layout, 
        icon='img/icon.ico', 
        size=(450, 460), 
        resizable=False, 
        margins=(0, 0), 
        background_color=colors['grey']
    )

    #print(accountdetails['accountName'] + accountdetails['charName'] + accountdetails['charRank'] + accountdetails['charBeosztas'])

    while True:
        event, values = mw.read(timeout=1000)

        if event == sg.WIN_CLOSED:
            break

        if event == "-LOGIN-":
            cursor.execute("SELECT accName FROM accounts WHERE tempPass=1",)
            eredmeny = cursor.fetchall()
            tempAcc = False
            for x in eredmeny:
                if (x[0] == values["username"]):
                    tempAcc = True
                    break
                
            if not tempAcc:
                if login(values["username"], values["password"]) == "oks":

                    cursor.execute("SELECT nev, rang, beosztas, admin, pfplink FROM accounts WHERE accName=%s", (values["username"],))
                    eredmeny = cursor.fetchall()
                    #print(eredmeny[0][0] + eredmeny[0][1] + eredmeny[0][2] + str(eredmeny[0][3]))
                    accountdetails['accountName'] = values["username"]
                    accountdetails['charName'] = eredmeny[0][0].replace("_", " ")
                    accountdetails['charRank'] = eredmeny[0][1]
                    accountdetails['charBeosztas'] = eredmeny[0][2]
                    accountdetails['adminLevel'] = int(eredmeny[0][3])
                    accountdetails['pfplink'] = str(eredmeny[0][4])
                    accountdetails['pfpdata'] = pfpfrissit()
                    mw.close()
                    calc_window()
                elif login(values["username"], values["password"]) == "nonetype":
                    mw["-ERROR_LOG-"].update(visible=True)
                    mw["-ERROR_LOG-"].update('Nem található felhasználónév')
                elif login(values["username"], values["password"]) == "nemoks":
                    mw["-ERROR_LOG-"].update(visible=True)
                    mw["-ERROR_LOG-"].update('Hibás jelszó! Ha elfelejtetted a jelszavad, vedd fel a \nkapcsolatot az alosztályvezetőkkel.')
            else:
                mw.close()
                register_window(values["username"])

def register_window(accName):
    mw = sg.Window(
        'lrszapp | Regisztráció',
        register_layout, 
        icon='img/icon.ico', 
        size=(450, 400), 
        resizable=False, 
        margins=(0, 0), 
        background_color=colors['grey']
    )

    while True:
        event, values = mw.read(timeout=1000)

        if event == sg.WIN_CLOSED:
            break

        if event == "-REGISTER-":
            if len(values["reg_password"]) >= 8:
                mw["-ERROR_LOG-"].update(visible=False)
                salt = phash.gensalt()
                hashed_pw = phash.hashpw(values["reg_password"].encode("utf-8"), salt)
                cursor.execute("UPDATE accounts SET accPass = %s, tempPass = %s WHERE accName = %s", (hashed_pw, 0, accName))
                database.commit()

                #dictionarybe való mentések
                accountdetails['accountName'] = accName

                cursor.execute("SELECT nev, rang, beosztas, admin, pfplink FROM accounts WHERE accName=%s", (accName,))
                eredmeny = cursor.fetchall()
                #print(eredmeny[0][0] + eredmeny[0][1] + eredmeny[0][2])
                accountdetails['charName'] = eredmeny[0][0]
                accountdetails['charRank'] = eredmeny[0][1]
                accountdetails['charBeosztas'] = eredmeny[0][2]
                accountdetails['adminLevel'] = int(eredmeny[0][3])
                accountdetails['pfplink'] = str(eredmeny[0][4])
                accountdetails['pfpdata'] = pfpfrissit()
                #print(accountdetails['accountName'] + accountdetails['charName'] + accountdetails['charRank'] + accountdetails['charBeosztas'])

                mw.close()
                #time.sleep(0.1)
                calc_window()
            else:
                mw["-ERROR_LOG-"].update(visible=True)
                mw["-ERROR_LOG-"].update('Kérlek a jelszavad legyen legalább 8 karakter hosszú.')

if __name__ == "__main__":
    #login_window()
    calc_window()
    #debug()

