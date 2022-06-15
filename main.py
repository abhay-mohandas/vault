
import curses #curses module is used to draw/print text at any location in the window
import secrets
from pyperclip import copy, paste



screen=curses.initscr() # Initializing the curses screen
curses.noecho()         # Set to avoid printing input text on screen
curses.cbreak()         # Disable input buffer to get instantaneous input values
curses.curs_set(0)      # Hide curser for the window
screen.keypad(True)     # Enable keypad

num_rows,num_cols=screen.getmaxyx() # Finds the maximum values of y and x of the current window size

highlight=curses.A_STANDOUT         # Text highlighting
bold=curses.A_BOLD                  # Bold text
normal=curses.A_NORMAL              # Normal text
italics=curses.A_ITALIC             # Italic text
underline=curses.A_UNDERLINE
dim=curses.A_DIM


ckey=screen.getch                   # 
skey=screen.getstr                  #
kkey=screen.getkey
clear=screen.clear                  #
border=screen.border                #
refresh=screen.refresh              #
box=screen.box
sleep=curses.napms


special_char=["!","@","#","$","%","^","&","*","?",">","<",'(',')','_','-','+','=','|','`','~']
char=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
num=['0','1','2','3','4','5','6','7','8','9']
list_char=[char,num,special_char]


#################################################################################################################################

#title function is used to print titles on screen
def title(title_name,type=screen):
    title_name= prefix+title_name+suffix
    y_pos=1
    middle_x=x_mid()
    x_padding=len(title_name)//2
    x_pos=middle_x-x_padding
    screen.addstr(y_pos,x_pos,title_name,bold|highlight|italics)
   #screen.refresh()

def center(y_offset,x_offset,string,style=normal,noshift=False,type=screen):
    y_pos=y_mid()+y_offset
    middle_x=x_mid()+x_offset
    if noshift==True:
        x_pos=middle_x
    else:
        x_padding=len(string)//2
        x_pos=middle_x-x_padding
    type.addstr(y_pos,x_pos,string,style)
    #screen.refresh()

# x_mid function is used to find the middle value of the total x value of the current window size
def x_mid():
    y,x=yx_total(0,1)
    return x//2

# y_mid function is used to find the middle value of the total y value of the current window size
def y_mid():
    y,x=yx_total(1,0)
    return y//2

# yx_total is used to return maximum value of y and x of the current window size. Returned value depends on the parameters
def yx_total(y=0,x=0):
   ys,xs=screen.getmaxyx()
   if not(x):
      return ys,0
   elif not(y):
      return 0,xs
   return ys,xs
   
# finish function is used to reset the initial state of the window and terminal the program
def finish():
   curses.echo()
   curses.nocbreak()
   curses.curs_set(1)
   screen.keypad(False)
   curses.endwin()
   exit()

def highlight_checker(index,value,control=1):
    if control:
        if index==value:
            return bold|highlight
    return bold

#################################################################################################################################

##########################
### Encryption section ###
##########################

# Note: This is a custom keyless encryption written from scratch

# str_to_bin takes the characters in a string and returns a list of individual character in 7-bit binary format 
def str_to_bin(in_string):
    bin_list=[]
    for x in in_string:
        binary=ord(x)
        binary=bin(binary)
        if len(binary[2:])<7:                       #
            padding=""                              # This section pads with additional zeros at the left side incase
            for y in range(7-len(binary[2:])):      # the lenght of the binary format is less than 7-bit
                padding+="0"                        #
            binary=binary[:2]+padding+binary[2:]    #
        bin_list.append(binary[2:])
    return bin_list

# matrix function generates and returns a 7x7 binary matrix of the given list
def matrix(run_list,default=7):                 
    return_list=[]
    while run_list:
        temp_list=[]
        if len(run_list)>=default:
            temp_list=run_list[:default]
            run_list=run_list[default:]
        else:
            temp_list=run_list                      #
            for _ in range(default-len(run_list)):  # This section handles the padding with blank space to complete
                temp_list.append("0100000")         # the 7x7 matrix if there are insufficient number of message
            run_list=0                              # bits
        return_list.append(temp_list)               #
    return return_list

# crypt_calc converts the given binary matrix to encrypted message. It also converts the encrypted text binary back 
# to original text. So this function handles both encryption and decryption
def crypt_calc(msg_mat):
    temp_mat2=[]
    for i in msg_mat:                           #
        z=0                                     #   Ex:
        temp_mat1=[]                            #       
        for j in range(len(i)):                 #      |1|1 0 0 0 1 1 <- input bits (row wise)
            temp=""                             #      |1|1 1 0 0 0 0
            for x in i:                         #      |1|0 0 0 0 0 1
                temp+=x[z]                      #      |0|0 1 1 1 1 0
            temp_mat1.append(temp)              #      |1|1 0 0 0 0 0
            z+=1                                #      |0|1 0 0 1 1 0
        temp_mat2.append(temp_mat1)             #      |1|1 1 1 1 1 0
    final=""                                    #       ^
    for a in temp_mat2:                         #       |
        for b in a:                             #       output bits (column wise)
            final+=chr(int("0b"+b,2))           #
    return final                                #

# crypt handles and merges the encyption/decryption functions
def crypt(message):
    message_list=str_to_bin(message)        # -convertion of strings to list of bits 
    mess_list_bin=matrix(message_list)      # -converting list of bits to matrix (list of lists)
    return crypt_calc(mess_list_bin)        # -return encrypted/decrypted message from the binary matrix

#################################################################################################################################

#####################
### Login Section ###
#####################

def default_login():
    passhash=""
    full_pass=""
    index=0
    passbox=screen.subwin(3,60,y_mid()-2,x_mid()-30)
    clear()
    while True:
        border()
        passbox.border()
        title(TITLE)
        center(-3,0,"Enter Master Password",bold)
        center(-1,0,passhash,bold)
        refresh()
        curses.curs_set(1)
        passwd=ckey()
        curses.curs_set(0)
        clear()
        if passwd==10 or passwd==curses.KEY_ENTER: #10 is ENTER key
            if full_pass==mp:
                return menu1()
            clear()
            center(1, 0, "Incorrect Password!",dim)
            refresh()
            full_pass=""
            passhash=""
            continue
        elif passwd==curses.KEY_BACKSPACE:
            full_pass=full_pass[:-1]
            passhash=passhash[:-1]
            continue
        elif passwd==27: # 27 is ESC key
            return finish()
        full_pass+=chr(passwd)
        if len(passhash)<54:
            passhash+=passhide

def init_login(passhide="#"):
    clear()
    full_pass1=""
    full_pass2=""
    passbox=screen.subwin(3,100,y_mid()-2,x_mid()-50)
    passhash=""
    while True:
        border()
        passbox.border()
        title(TITLE)
        center(-3,0,"Enter A New Master Password",bold)
        center(-1,0,passhash,bold)
        refresh()
        curses.curs_set(1)
        passwd=ckey()
        curses.curs_set(0)
        clear()
        if passwd==10 or passwd==curses.KEY_ENTER: #10 is ENTER key
            full_pass1=full_pass1.strip()
            if len(full_pass1)<6:
                clear()
                center(1, 0, "Minimum 6 characters Required",dim)
                refresh()
                full_pass1=""
                passhash=""
                continue
            else:
                break
        elif passwd==curses.KEY_BACKSPACE:
            full_pass1=full_pass1[:-1]
            passhash=passhash[:-1]
            continue
        elif passwd==27: # 27 is ESC key
            return finish()
        full_pass1+=chr(passwd)
        if len(passhash)<84:
            passhash+=passhide
    passhash=""
    while True:
        clear()
        border()
        passbox.border()
        title(TITLE)
        center(-3,0,"Confirm The Master Password",bold)
        center(-1,0,passhash,bold)
        refresh()
        curses.curs_set(1)
        passwd=ckey()
        curses.curs_set(0)
        if passwd==10 or passwd==curses.KEY_ENTER: #10 is ENTER key
            break
        elif passwd==curses.KEY_BACKSPACE:
            full_pass2=full_pass2[:-1]
            passhash=passhash[:-1]
            continue
        elif passwd==27: # 27 is ESC key
            return finish()
        full_pass2+=chr(passwd)
        if len(passhash)<84:
            passhash+=passhide
    clear()
    border()
    if full_pass1==full_pass2:
        center(0, 0, "New Master Password Saved!",bold)
        refresh()
        sleep(delay)
        file=open(".pass.crypt","w")   
        file.write(crypt("Master"))
        file.write("::::::::")
        file.write(crypt(full_pass1))
        file.write("\n########\n")
        file.close()
        center(-1, 0, "Restart The Program To Reset To New Master Password",bold)
        center(+1, 0, "Press Any Key to Continue",dim)
        ckey()
        return finish()
    else:
        center(0, 0, "Passwords Doesn't Match! Try Again...")
        refresh()
        sleep(delay)
        return init_login()

#################################################################################################################################
####################
### Menu Section ###
####################

def menu1():
    menu1_list=[["  Password Manager  ",pass_manager],[" Password Generator ",pass_gen],["      Settings      ",settings]]
    checker=0
    while True:
        clear()
        border()
        title(TITLE)
        y_offset=-2
        for x in menu1_list:
            center(y_offset, 0, x[0], highlight_checker(menu1_list.index(x), checker))
            y_offset+=2
        refresh()
        key=ckey()
        if key==curses.KEY_DOWN:
            checker+=1
            if checker>=len(menu1_list):
                checker=0
        elif key==curses.KEY_UP:
            checker-=1
            if checker<0:
                checker=len(menu1_list)-1
        elif key==27: # 27 is ESC key
            return finish()
        elif key==10 or key==curses.KEY_ENTER:
            return menu1_list[checker][1]()
        elif key==curses.KEY_BACKSPACE:
            return default_login()


#################################################################################################################################
##################################
### Password Generator Section ###
##################################

def pass_gen():
    password=""
    for a in range(pass_gen_length):
        x=secrets.choice(list_char)
        y=secrets.choice(x)
        password+=y
    passbox=screen.subwin(3,pass_gen_length+10,y_mid()-2,x_mid()-((pass_gen_length//2)+5))
    checker=0
    pass_gen_options=[" Copy to Clipboard "," Re-Generate "]
    clear()
    while True:
        border()
        passbox.border()
        title("Password Generator")
        center(-1, 0, password)
        center(2, -20, pass_gen_options[0],highlight_checker(0, checker))
        center(2, 20, pass_gen_options[1],highlight_checker(1, checker))
        refresh
        key=ckey()
        if key==curses.KEY_RIGHT:
            checker+=1
            if checker>=len(pass_gen_options):
                checker=0
        elif key==curses.KEY_LEFT:
            checker-=1
            if checker<0:
                checker=len(pass_gen_options)-1
        elif key==27: # 27 is ESC key
            return finish()
        elif key==10 or key==curses.KEY_ENTER:
            if checker==0:
                try:
                    copy(password)
                    center(-4, 0, "Password Copied!",dim)
                except:
                    center(-4, 0, "Failed To Copy To Clipboard",dim)
                refresh()
                continue
            elif checker==1:
                return pass_gen()
        elif key==curses.KEY_BACKSPACE:
            return menu1()
        clear()


#################################################################################################################################
################################
### Password Manager Section ###
################################


def pass_manager():
    checker=0
    menu_list=[["   Add New Password   ",add_password],[" List Saved Passwords ",list_password]]
    while True:
        clear()
        border()
        title("Password Manager")
        center(-1, 0, menu_list[0][0],highlight_checker(0, checker))
        center(1, 0, menu_list[1][0],highlight_checker(1, checker))
        refresh()
        key=ckey()
        if key==curses.KEY_UP:
            checker+=1
            if checker>=len(menu_list):
                checker=0
        elif key==curses.KEY_DOWN:
            checker-=1
            if checker<0:
                checker=len(menu_list)-1
        elif key==27: # 27 is ESC key
            return finish()
        elif key==10 or key==curses.KEY_ENTER:
            return menu_list[checker][1]()
        elif key==curses.KEY_BACKSPACE:
            return menu1()


#################################################################################################################################
############################
### Add Password Section ###
############################


def add_password():
    username=enter_username()
    password=enter_password()
    file=open(".pass.crypt","a")
    file.write(crypt(username))
    file.write("::::::::")
    file.write(crypt(password))
    file.write("\n########\n")
    file.close()
    clear()
    border()
    center(-2, 0, "New Entry Saved!",bold)
    refresh()
    sleep(delay)
    return pass_manager()


def enter_username(username='',password=''):
    passbox=screen.subwin(3,70,y_mid()-4,x_mid()-30)
    clear()
    while True:
        border()
        title("Add Username")
        passbox.border()
        center(-3,-40, "Enter Username:",bold)
        center(-3,-28, username,bold,True)
        refresh()
        curses.curs_set(1)
        key=ckey()
        curses.curs_set(0)
        if key==27: # 27 is ESC key
            return finish()
        elif key==10 or key==curses.KEY_ENTER:
            username=username.strip()
            if not username:
                center(0, 0, "Username cannot be blank!",dim)
                continue
            return username
        elif key==curses.KEY_BACKSPACE:
            if not username:
                return pass_manager()
            username=username[:-1]
        elif key==curses.KEY_LEFT or key==curses.KEY_RIGHT or key==curses.KEY_UP or key==curses.KEY_DOWN:
            pass
        else:
            username+=chr(key)
        clear()
        

def enter_password(password='',username=''):
    passbox=screen.subwin(3,70,y_mid()-4,x_mid()-30)
    clear()
    while True:
        border()
        title("Add Password")
        passbox.border()
        center(-3,-40, "Enter Password:",bold)
        center(-3,-28, password,bold,True)
        refresh()
        curses.curs_set(1)
        key=ckey()
        curses.curs_set(0)
        if key==27: # 27 is ESC key
            return finish()
        elif key==10 or key==curses.KEY_ENTER:
            password=password.strip()
            if not password:
                center(0, 0, "Password cannot be blank!",dim)
                continue
            return password
        elif key==curses.KEY_BACKSPACE:
            if not password:
                return pass_manager()
            password=password[:-1]
        elif key==curses.KEY_LEFT or key==curses.KEY_RIGHT or key==curses.KEY_UP or key==curses.KEY_DOWN:
            pass
        else:
            password+=chr(key)
        clear()

#################################################################################################################################
#############################
### List Password Section ###
#############################

def list_password():
    list_update_read()
    clear()
    refresh()
    if len(usrnm_pass)==0:
        border()
        center(-1,0, "No Password Entries Found! Add Passwords To Be Listed",bold)
        center(+1,0, "Enter Any Key to Continue",dim)
        refresh()
        ckey()
        return pass_manager()
    checker=0
    keep_track=0
    y_loc=0
    count=len(usrnm_pass)
    listpad=curses.newpad(count+2,xlen)
    listpad.keypad(True)
    while True:
        y_ref,x_ref=yx_total(1,1)
        listpad.clear()
        #clear()
        title("Password List")
        border()
        refresh()
        listpad.border()
        for x in range(len(usrnm_pass)):
            listpad.addstr(x+1,3,usrnm_pass[x][0],highlight_checker(x, checker))
        listpad.refresh(y_loc,0,3,x_mid()-(xlen//2),y_ref-2,x_mid()+25)
        key=listpad.getch()
        if key==curses.KEY_DOWN:
            if checker<count-1:
                checker+=1
                if checker>y_ref-7:
                    y_loc+=1
        elif key==curses.KEY_UP:
            if checker>0:
                checker-=1
            if y_loc>0:
                y_loc-=1
        elif key==27: # 27 is ESC key
            return finish()
        elif key==10 or key==curses.KEY_ENTER:
            return show_password(usrnm_pass[checker])
        elif key==curses.KEY_BACKSPACE:
            return pass_manager()

def show_password(pass_details):
    clear()
    y_max,x_max=yx_total()
    username,password=pass_details[0],pass_details[1]
    if xlen>ylen and xlen>50:
        long=xlen
    elif ylen>50:
        long=ylen
    else:
        long=50
    usrnbox=screen.subwin(3,long,y_mid()-4,x_mid()-(x_mid()//2)-5)
    passbox=screen.subwin(3,long,y_mid()-1,x_mid()-(x_mid()//2)-5)
    options=[["  Copy Username  ",copy,username],
             ["  Copy Password  ",copy,password],
             [" Update Username ",update_details,[1,username,password]],
             [" Update Password ",update_details,[0,username,password]],
             ["     Delete      ",delete_details,[username,password]]]
    checker=0
    while True:
        border()
        title("Details")
        usrnbox.border()
        passbox.border()
        center(-3, -x_mid()+(4*(x_mid()//10)), 'Username:',bold)
        center(0, -x_mid()+(4*(x_mid()//10)), 'Password:',bold)
        center(-3, -x_mid()//2, username,bold,True)
        center(0, -x_mid()//2, password,bold,True)
        option_spacing=y_mid()//4
        temp=(y_mid()//10)*6
        for x in range(len(options)):
            center(-temp+x, +(x_mid()//2), options[x][0],highlight_checker(x, checker))
            temp-=option_spacing
        refresh()
        key=ckey()
        if key==curses.KEY_DOWN:
            checker+=1
            if checker>(len(options)-1):
                checker=0
        elif key==curses.KEY_UP:
            checker-=1
            if checker<0:
                checker=len(options)-1
        elif key==27: # 27 is ESC key
            return finish()
        elif key==10 or key==curses.KEY_ENTER:
            function=options[checker][1]
            data=options[checker][2]
            if function==copy:
                try:
                    function(data)
                    center(-6, 0, "Copied Successfully!",dim)
                except:
                    center(-6, 0, "Failed To Copy To Clipboard",dim)
                continue
            return function(data)
        elif key==curses.KEY_BACKSPACE:
            return list_password()
        clear()


def update_details(data):
    global usrnm_pass
    condition,username,password=data
    databox=screen.subwin(3,x_mid()-(x_mid()//3),y_mid()-1, x_mid()-(x_mid()//4))
    if condition:
        mod,new_pass="",password
        header="Username"
    else:
        new_usrnm,mod=username,""
        header="Password"
    while True:
        clear()
        databox.border()
        border()
        title("Update "+header)
        center(0, -x_mid()+(x_mid()//2),"Enter the New "+header+":",bold,True)
        center(0, -x_mid()+((x_mid()//5)*4), mod,bold,True)
        refresh()
        curses.curs_set(1)
        key=ckey()
        curses.curs_set(0)
        if key==curses.KEY_BACKSPACE:
            if len(mod)>0:
                mod=mod[:-1]
            else:
                return list_password()
        elif key==10 or key==curses.KEY_ENTER:
            if condition:
                new_usrnm=mod
            else:
                new_pass=mod
            new_data=[new_usrnm,new_pass]
            index=usrnm_pass.index([username,password])
            usrnm_pass.pop(index)
            usrnm_pass.insert(index, new_data)
            list_update_write()
            return list_password()
        elif key==27:
            return finish()
        elif key==curses.KEY_LEFT or key==curses.KEY_RIGHT or key==curses.KEY_UP or key==curses.KEY_DOWN:
            continue
        else:
            mod+=chr(key)

def delete_details(data):
    global usrnm_pass
    checker=0
    while True:
        clear()
        border()
        center(-2, 0, "Confirm?",bold)
        center(1, -x_mid()//4, "  Yes  ",highlight_checker(0,checker))
        center(1, +x_mid()//4, "   No  ",highlight_checker(1,checker))
        key=ckey()
        if key==curses.KEY_RIGHT or key==curses.KEY_LEFT:
            if checker:
                checker=0
            else:
                checker=1
        elif key==10 or key==curses.KEY_ENTER:
            if checker:
                return list_password()
            else:
                index=usrnm_pass.index(data)
                usrnm_pass.pop(index)
                list_update_write()
                return list_password()
        elif key==curses.KEY_BACKSPACE:
            return list_password()


#################################################################################################################################
########################
### Settings Section ###
########################

def settings():
    pass

#################################################################################################################################
########################
### Config Section ###
########################


def config_read():
    global pass_gen_length,prefix,suffix,TITLE,delay,passhide
    file=open("settings.config","r")
    conf=file.read()
    conf_list= ["generated_password_lenght",
                "prefix",
                "suffix",
                "title",
                "delay",
                "password_hide"]
    conf=conf.split("\n")
    for x in conf:
        if x.startswith("#"):
            continue
        x=x.strip()
        if not x:
            continue
        temp=x.split("=")
        defin=temp[0].strip()
        value=temp[1].strip()
        if conf_list[0] in defin:
            pass_gen_length=int(value)
        elif conf_list[1] in defin:
            prefix=value[1:-1]
        elif conf_list[2] in defin:
            suffix=value[1:-1]
        elif conf_list[3] in defin:
            TITLE=value[1:-1]
        elif conf_list[4] in defin:
            delay=int(value)
        elif conf_list[5] in defin:
            passhide=value[1:-1]
    file.close()


def config_write():
    file=open("settings.config","w")
    notice="#This is the program config file. This can be modified by editing (Not recommended) or can be done via settings within the program.\n#This is setup to avoid direct modification of the code file.\n#Comments can be added to the file by placing '#' at the beginning of the line.\n\n"
    file.write(notice)
    file.write("\n")
    init_conf_list=[["#Option to set the generated password lenght. Max lenght is limited to 68 characters to fit the screen.\n#Set a value from 8-64\n",
                            "generated_password_lenght= "+str(pass_gen_length)+"\n"],
                    ["#Option to set the prefix and suffix of the title. Include quotation for strings (Ex:' ##' and '## ')\n",
                            "prefix= '"+prefix+"'\n",
                            "suffix= '"+suffix+"'\n"],
                    ["#Option to set the program name. Default name is 'Vault' followed by its version. Include quotation for strings\n",
                            "title= '"+TITLE+"'\n"],
                    ["#Option to set delay in milliseconds for the displayed messages\n",
                            "delay= "+str(delay)+"\n"],
                    ["#Option to set the password hider. Default hider is '#' and can be empty to hide passwords completely. Include quotation for strings\n",
                            "password_hide= '"+passhide+"'\n"]]
    for x in init_conf_list:
        for y in x:
            file.write(y)
            file.write("\n")
        file.write("\n\n")
    file.close()



def init_config(warning="No Configuration File Found!"):
    clear()
    border()
    center(-2, 0, warning,bold)
    center(0, 0, "Press Any Key To Load Default Configuration")
    refresh()
    key=ckey()
    config_write()
    clear()
    border()
    center(0, 0, "Default Configurations Are Loaded Successfully!",bold)
    refresh()
    sleep(delay)


def config_error():
    init_config("Warning! There Was An Error Loading The Configuration File!")
    clear()
    border()
    center(-2, 0, "Restart The Program To Run The Configuration File",bold)
    center(0, 0, "Press Any Key to Exit The Program")
    refresh()
    key=ckey()
    finish()


#################################################################################################################################
######################
### Update Section ###
######################

def list_update_read():
    global mp,usrnm_pass,xlen,ylen
    usrnm_pass=[]
    file=open(".pass.crypt","r")
    read_file=file.read()
    read_file=read_file.split("########")
    for x in read_file:
        x=x.strip()
        if not x:
            break
        temp=x.split("::::::::")
        username=crypt(temp[0]).strip()
        passwd=crypt(temp[1]).strip()
        if username=="Master":
            mp=passwd
            track=False
            continue
        if xlen<len(username):
            xlen=len(username)+6
        if ylen<len(passwd):
            ylen=len(passwd)+6
        usrnm_pass.append([username,passwd])


def list_update_write():
    file=open(".pass.crypt","w")
    file.write(crypt("Master"))
    file.write("::::::::")
    file.write(crypt(mp))
    file.write("\n########\n")
    for x in usrnm_pass:
        file.write(crypt(x[0]))
        file.write("::::::::")
        file.write(crypt(x[1]))
        file.write("\n########\n")
    file.close()

#################################################################################################################################
###############################
### Global Variable Section ###
###############################

passhide="#"
mp=""
usrnm_pass=[]
xlen=0
ylen=0

pass_gen_length=18

prefix=" ##"
suffix="## "
TITLE="VAULT v2"

delay=2000                          # In milliseconds


try:
    open("settings.config","x")
    init_config()
    config_read()
except:
    try:
        config_read()
    except:
        config_error()

try:
    open(".pass.crypt","x")
    init_login()
except:
    list_update_read()
    default_login()


finish()
