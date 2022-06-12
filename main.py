
import curses #curses module is used to draw/print text at any location in the window
import random,secrets
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

delay=3000                          # In milliseconds


ckey=screen.getch                   # 
skey=screen.getstr                  #
kkey=screen.getkey
clear=screen.clear                  #
border=screen.border                #
refresh=screen.refresh              #
box=screen.box
sleep=curses.napms


special_char=["!","@","#","$","%","^","&","*","?",">","<"]
char=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
num=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
list_char=[char,num,special_char]
pass_lenght=30

#################################################################################################################################

#title function is used to print titles on screen
def title(title_name,type=screen):
    title_name= " ##"+title_name+"## "
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

def highlight_checker(index,value,control=1):
    if control:
        if index==value:
            return bold|highlight
    return bold

#################################################################################################################################

##########################
### Encryption section ###
##########################

# Note: This is a custom keyless encryption

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

def default_login(passhide="#"):
    passhash=""
    full_pass=""
    index=0
    passbox=screen.subwin(3,60,y_mid()-2,x_mid()-30)
    clear()
    while True:
        border()
        passbox.border()
        title("VAULT")
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
            return
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
        title("VAULT")
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
            return
        full_pass1+=chr(passwd)
        if len(passhash)<84:
            passhash+=passhide
    passhash=""
    while True:
        clear()
        border()
        passbox.border()
        title("VAULT")
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
            return
        full_pass2+=chr(passwd)
        if len(passhash)<84:
            passhash+=passhide
    clear()
    border()
    if full_pass1==full_pass2:
        center(0, 0, "New Master Password Saved!",bold)
        refresh()
        sleep(delay)
        f=open(".mp.txt","w")   
        f.write(crypt(full_pass1))
        f.close()
        return default_login()
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
    menu1_list=[["  Password Manager  ",pass_manager],[" Password Generator ",pass_gen],["      Settings      ",config]]
    checker=0
    while True:
        clear()
        border()
        title("VAULT")
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
            return
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
    for a in range(pass_lenght):
        x=secrets.choice(list_char)
        y=secrets.choice(x)
        password+=y
    passbox=screen.subwin(3,pass_lenght+10,y_mid()-2,x_mid()-((pass_lenght//2)+5))
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
            return
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
            return
        elif key==10 or key==curses.KEY_ENTER:
            return menu_list[checker][1]()
        elif key==curses.KEY_BACKSPACE:
            return menu1()


def add_password():
    username=enter_username()
    password=enter_password()
    file=open(".list.txt","a")
    file.write(crypt(username))
    file.write("::::::::")
    file.write(crypt(password))
    file.write("\n########\n")
    file.close()
    clear()
    border()
    center(-2, 0, "New Entry Saved!",bold)
    refresh()
    sleep(3000)
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

def list_password():
    clear()
    refresh()
    usrnm_pass=[]
    xlen=0
    file=open(".list.txt","r")
    read_file=file.read()
    read_file=read_file.split("########")
    for x in read_file:
        x=x.strip()
        if not x:
            break
        temp=x.split("::::::::")
        username=crypt(temp[0]).strip()
        if xlen<len(username):
            xlen=len(username)+6
        passwd=crypt(temp[1]).strip()
        usrnm_pass.append([username,passwd])
    y_max,x_max=yx_total(1,1)
    #listpad=screen.subwin(5,x_mid()-20)
    #listpad.overlay(screen)
    checker=0
    keep_track=0
    y_loc=0
    count=len(usrnm_pass)
    listpad=curses.newpad(count+2,xlen)
    listpad.keypad(True)
    while True:
        y_ref,x_ref=yx_total(1,1)
        listpad.clear()
        clear()
        title("Password List")
        border()
        refresh()
        listpad.border()
        for x in range(len(usrnm_pass)):
            #listpad.addstr(x,0,usrnm_pass[x][0],highlight_checker(x, checker))
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
            pass
        elif key==curses.KEY_BACKSPACE:
            return pass_manager()




#################################################################################################################################
########################
### Settings Section ###
########################


def config():
    pass














#################################################################################################################################


try:
    open(".mp.txt","x")
    open(".list.txt","x")
    init_login()
except:
    masterPassword=open(".mp.txt","r")
    passwordList=open(".list.txt","r")
    masterPassword=masterPassword.read()
    masterPassword=masterPassword.strip()
    mp=crypt(masterPassword)
    mp=mp.strip()
    default_login()
finish()
