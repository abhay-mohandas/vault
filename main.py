'''
BSD 3-Clause License

Copyright (c) 2022, Abhay Mohandas
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''


#! /usr/bin/python

import curses                       # curses module is used to draw/print text at any location in the window
import secrets                      # secret module is used to generate password. This is recommended over random module for passwords
from pyperclip import copy, paste   # pyperclip is used to copy and paste details to the clipboard
from sys import exit


screen=curses.initscr()             # Initializing the curses screen
curses.noecho()                     # Set to avoid printing input text on screen
curses.cbreak()                     # Disable input buffer to get instantaneous input values
curses.curs_set(0)                  # Hide curser for the window
screen.keypad(True)                 # Enable keypad to get arrow and other keys working

num_rows,num_cols=screen.getmaxyx() # Finds the maximum values of y and x of the current window size

highlight=curses.A_STANDOUT         # Text highlighting
bold=curses.A_BOLD                  # Bold text
normal=curses.A_NORMAL              # Normal text
italics=curses.A_ITALIC             # Italic text
underline=curses.A_UNDERLINE        # Underlines the text
dim=curses.A_DIM                    # Dims the text


ckey=screen.getch                   # 
skey=screen.getstr                  #
kkey=screen.getkey                  #
clear=screen.clear                  #
border=screen.border                #
refresh=screen.refresh              #
box=screen.box                      #
sleep=curses.napms                  #


special_char=("!","@","#","$","%","^","&","*","?",">","<",'(',')','_','-','+','=','|','`','~')
char=('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
num=('0','1','2','3','4','5','6','7','8','9')
list_char=(char,num,special_char)

#################################################################################################################################

#title function is used to print titles on screen
def title(title_name,type=screen):
    title_name= prefix+title_name+suffix
    y_pos=1
    middle_x=x_mid()
    x_padding=len(title_name)//2
    x_pos=middle_x-x_padding
    screen.addstr(y_pos,x_pos,title_name,bold|highlight|italics)

# center function is used to display text at the center of the screen
def center(y_offset,x_offset,string,style=normal,noshift=False,type=screen):
    y_pos=y_mid()+y_offset
    middle_x=x_mid()+x_offset
    if noshift:             # If noshift is true, then the beginning of the text is printed at the center,
        x_pos=middle_x      # else the middle of the text is printed at the center
    else:
        x_padding=len(string)//2
        x_pos=middle_x-x_padding
    type.addstr(y_pos,x_pos,string,style)

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

# highlight_checker is used to display and interact with options
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
        if len(binary[2:])<8:                       #
            padding=""                              # This section pads with additional zeros at the left side incase
            for y in range(8-len(binary[2:])):      # the lenght of the binary format is less than 8-bit
                padding+="0"                        #
            binary=binary[:2]+padding+binary[2:]    #
        bin_list.append(binary[2:])
    return bin_list

# matrix function generates and returns a 8x8 binary matrix of the given list
def matrix(run_list,default=8):                 
    return_list=[]
    while run_list:
        temp_list=[]
        if len(run_list)>=default:
            temp_list=run_list[:default]
            run_list=run_list[default:]
        else:
            temp_list=run_list                      #
            for _ in range(default-len(run_list)):  # This section handles the padding with blank space to complete
                temp_list.append("11111111")        # the 8x8 matrix if there are insufficient number of message
            run_list=0                              # bits
        return_list.append(temp_list)               #
    return return_list

# crypt_calc converts the given binary matrix to encrypted message. It also converts the encrypted text binary back 
# to original text. So this function handles both encryption and decryption
def crypt_calc(msg_mat):
    temp_mat2=[]
    for i in msg_mat:                           #
        z=0                                     #   Ex:
        temp_mat1=[]                            #      |0|1 1 0 0 1 1 0 <- input bits (row wise)
        for j in range(len(i)):                 #      |1|1 0 0 0 1 1 0 
            temp=""                             #      |1|1 1 0 0 0 0 0
            for x in i:                         #      |1|0 0 0 0 0 1 0
                temp+=x[z]                      #      |0|0 1 1 1 1 0 0
            temp_mat1.append(temp)              #      |1|1 0 0 0 0 0 0
            z+=1                                #      |0|1 0 0 1 1 0 0
        temp_mat2.append(temp_mat1)             #      |1|1 1 1 1 1 0 0
    final=""                                    #       ^
    for a in temp_mat2:                         #       |
        for b in a:                             #       output bits (column wise)
            final+=chr(int("0b"+b,2))           #
    return final                                #

# crypt handles and merges the encyption/decryption functions
def crypt(message):
    message=message.replace("\\r","\r")         # -Replacing '\\r' with '\r': Encryption Bug Fix/Mitigation
    message_list=str_to_bin(message)            # -convertion of strings to list of bits 
    mess_list_bin=matrix(message_list)          # -converting list of bits to matrix (list of lists)
    crypt_mess=crypt_calc(mess_list_bin)        # -return encrypted/decrypted message from the binary matrix
    crypt_mess=crypt_mess.replace("\r", "\\r")  # -Replacing '\r' with '\\r': Encryption Bug Fix/Mitigation
    return crypt_mess

#################################################################################################################################

#####################
### Login Section ###
#####################

# default_login is called if a Master password is found. 
# Master password is stored in .pass.crypt file along with other passwords
def default_login():
    passhash=""
    full_pass=""
    index=0
    passbox=screen.subwin(3,60,y_mid()-2,x_mid()-30)    # Create a Sub window over the screen
    clear()
    while True:
        border()
        passbox.border()
        title(TITLE)
        center(-3,0,"Enter Master Password",bold)
        center(-1,0,passhash,bold)
        refresh()
        curses.curs_set(1)                              # Turn on the visiblity of cursor
        passwd=ckey()
        curses.curs_set(0)                              # Turn off the visiblity of cursor
        clear()
        if passwd==10 or passwd==curses.KEY_ENTER:      #10 is ENTER key
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
        elif passwd==curses.KEY_LEFT or passwd==curses.KEY_RIGHT or passwd==curses.KEY_UP or passwd==curses.KEY_DOWN:
            continue
        full_pass+=chr(passwd)
        if len(passhash)<54:
            passhash+=passhide

# init_login is called if a Master password is not found. 
# A new .pass.crypt file is generated and New Master Password is encrypted and saved
def init_login():
    clear()
    full_pass1=""
    full_pass2=""
    passbox=screen.subwin(3,100,y_mid()-2,x_mid()-50)
    passhash=""
    while True:                                                 # Enter the New Master Password
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
        if passwd==10 or passwd==curses.KEY_ENTER:              #10 is ENTER key
            full_pass1=full_pass1.strip()
            if len(full_pass1)<6:                               # Check if the entered password has atleast 6 characters
                clear()                                         # If not, reset the screen with Warning Message
                center(1, 0, "Minimum 6 characters Required",dim)
                refresh()
                full_pass1=""
                passhash=""
                continue
            else:
                break
        elif passwd==curses.KEY_BACKSPACE:                      # Remove a character from the entered password
            full_pass1=full_pass1[:-1]
            passhash=passhash[:-1]
            continue
        elif passwd==27:                                        # 27 is ESC key
            return finish()
        elif passwd==curses.KEY_LEFT or passwd==curses.KEY_RIGHT or passwd==curses.KEY_UP or passwd==curses.KEY_DOWN:
            continue                                            # This prevents the use of arrow keys
        full_pass1+=chr(passwd)
        if len(passhash)<54:                                    # After the given characters, no more visual feedback is displayed
            passhash+=passhide                                  # This is to prevent errors from displaying more characters than possible
    passhash=""
    while True:
        clear()
        border()
        passbox.border()
        title(TITLE)
        center(-3,0,"Confirm The Master Password",bold)         # Ask to re-enter the Master Password to verify
        center(-1,0,passhash,bold)
        refresh()
        curses.curs_set(1)
        passwd=ckey()
        curses.curs_set(0)
        if passwd==10 or passwd==curses.KEY_ENTER:              # 10 is ENTER key
            break
        elif passwd==curses.KEY_BACKSPACE:                      # Remove a character from the entered password
            full_pass2=full_pass2[:-1]
            passhash=passhash[:-1]
            continue
        elif passwd==27:                                        # 27 is ESC key
            return finish()
        elif passwd==curses.KEY_LEFT or passwd==curses.KEY_RIGHT or passwd==curses.KEY_UP or passwd==curses.KEY_DOWN:
            continue
        full_pass2+=chr(passwd)
        if len(passhash)<54:
            passhash+=passhide
    clear()
    border()
    if full_pass1==full_pass2:                                  # If both the inputs match, then encrypt the Master Password
        center(0, 0, "New Master Password Saved!",bold)         # and save it to .pass.crypt file
        refresh()                                               # Else, Display a warning message and reset the screen after 
        sleep(delay)                                            # a specified delay
        file=open(".pass.crypt","w")   
        file.write(crypt("Master"))
        file.write("::::::::")
        file.write(crypt(full_pass1))
        file.write("\n########\n")
        file.close()
        clear()
        border()
        center(-1, 0, "Restart The Program To Reset To New Master Password",bold)
        center(+1, 0, "Press Any Key to Continue",dim)
        refresh()
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

# menu1 is the primary menu. It is displayed right after the correct Master Password is entered
def menu1():
    menu1_list=(("  Password Manager  ",pass_manager),(" Password Generator ",pass_gen),("      Settings      ",settings))
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
    pass_gen_options=(" Copy to Clipboard "," Re-Generate ")
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
    menu_list=(("   Add New Password   ",add_password),(" List Saved Passwords ",list_password))
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
            finish()
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
            finish()
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
        title("Password List")
        border()
        refresh()
        listpad.border()
        for x in range(len(usrnm_pass)):
            listpad.addstr(x+1,3,usrnm_pass[x][0],highlight_checker(x, checker))
        listpad.refresh(y_loc,0,3,x_mid()-(xlen//2),y_ref-2,x_ref-2)#x_mid()+25)
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
    long=x_mid()
    usrnbox=screen.subwin(3,long,y_mid()-4,x_mid()-(x_mid()//2)-25)
    passbox=screen.subwin(3,long,y_mid()-1,x_mid()-(x_mid()//2)-25)
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
        center(-3, -x_mid()+(4*(x_mid()//10))-20, 'Username:',bold)
        center(0, -x_mid()+(4*(x_mid()//10))-20, 'Password:',bold)
        center(-3, (-x_mid()//2)-20, username[:long-6],bold,True)
        center(0, (-x_mid()//2)-20, password[:long-6],bold,True)
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
    global delay,pass_gen_length,TITLE,prefix,suffix,passhide
    action_list=[100,2]
    checker=0
    while True:
        clear()
        border()
        center(-6, 0, "  Delay:  < "+str(delay)+" >  ",highlight_checker(0, checker))
        center(-4, 0, " Generator Password Lenght:  < "+str(pass_gen_length)+" >  ",highlight_checker(1, checker))
        center(-2, 0, "  Title:  '"+TITLE+"'  ",highlight_checker(2, checker))
        center(0, 0, "  Title Prefix:  '"+prefix+"'  ",highlight_checker(3, checker))
        center(2, 0, "  Title Suffix:  '"+suffix+"'  ",highlight_checker(4, checker))
        center(4, 0, "  Password Hider:  '"+passhide+"'  ",highlight_checker(5, checker))
        refresh()
        key=ckey()
        if key==curses.KEY_DOWN:
            checker+=1
            if checker>5:
                checker=0
        elif key==curses.KEY_UP:
            checker-=1
            if checker<0:
                checker=5
        elif key==curses.KEY_LEFT:
            if checker==0:
                delay-=action_list[checker]
            elif checker==1:
                pass_gen_length-=action_list[checker]
        elif key==curses.KEY_RIGHT:
            if checker==0:
                delay+=action_list[checker]
            elif checker==1:
                if pass_gen_length<64:
                    pass_gen_length+=action_list[checker]
        elif key==10:
            if checker==2:
                change_title(0)
            if checker==3:
                change_title(1)
            if checker==4:
                change_title(2)
            if checker==5:
                change_title(3)
            config_write()
        elif key==curses.KEY_BACKSPACE:
            config_write()
            return menu1()
        elif key==27:
            config_write()
            return finish()

def change_title(index):
    global TITLE,prefix,suffix,passhide
    option_list=["Enter New Title:",
                 "Enter New Prefix:",
                 "Enter New Suffix:",
                 "Enter New Hider:"]
    textbox=screen.subwin(3,x_mid(),y_mid()-1, x_mid()-(x_mid()//4))
    new_val=""
    while True:
        clear()
        border()
        textbox.border()
        center(0, -x_mid()//2, option_list[index],bold)
        center(0, -(x_mid()//4)+4, "'"+new_val+"'",bold,True)
        refresh()
        key=ckey()
        if key==curses.KEY_LEFT or key==curses.KEY_RIGHT or key==curses.KEY_UP or key==curses.KEY_DOWN:
            continue
        elif key==curses.KEY_BACKSPACE:
            if not new_val:
                return
            new_val=new_val[:-1]
        elif key==27:
            return finish()
        elif key==10:
            if index==0:
                TITLE=new_val
            elif index==1:
                prefix=new_val
            elif index==2:
                suffix=new_val
            elif index==3:
                passhide=new_val
            return
        else:
            new_val+=chr(key)


#################################################################################################################################
########################
### Config Section ###
########################


def config_read():
    global pass_gen_length,prefix,suffix,TITLE,delay,passhide
    file=open(".settings.config","r")
    conf_list= ("generated_password_lenght",
                "prefix",
                "suffix",
                "title",
                "delay",
                "password_hide")
    for x in file:
        x=x.strip()
        if x.startswith("#") or not(x):
            continue
        temp=x.split("=")
        defin=temp[0].strip()
        value=temp[1].strip()
        if not(value) or not(defin):
            continue
        if conf_list[0] in defin:
            if int(value)>64:
                pass_gen_length=64
                continue
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
    file=open(".settings.config","w")
    notice="#This is the program config file. This can be modified by editing (Not recommended) or can be done via settings within the program.\n#This is setup to avoid direct modification of the code file.\n#Comments can be added to the file by placing '#' at the beginning of the line.\n\n"
    file.write(notice)
    file.write("\n")
    init_conf_list=(("#Option to set the generated password lenght. Max lenght is limited to 68 characters to fit the screen.\n#Set a value from 8-64\n",
                            "generated_password_lenght= "+str(pass_gen_length)+"\n"),
                    ("#Option to set the prefix and suffix of the title. Include quotation for strings (Ex:' ##' and '## ')\n",
                            "prefix= '"+prefix+"'\n",
                            "suffix= '"+suffix+"'\n"),
                    ("#Option to set the program name. Default name is 'Vault' followed by its version. Include quotation for strings\n",
                            "title= '"+TITLE+"'\n"),
                    ("#Option to set delay in milliseconds for the displayed messages\n",
                            "delay= "+str(delay)+"\n"),
                    ("#Option to set the password hider. Default hider is '#' and can be empty to hide passwords completely. Include quotation for strings\n",
                            "password_hide= '"+passhide+"'\n"))
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
    center(0, 0, "Press Any Key To Load Default Configuration",dim)
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
    center(0, 0, "Press Any Key to Exit The Program",dim)
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
        while True:
            if not(username.endswith(chr(int("0b11111111",2)))):
                break
            username=username[:-1]
        passwd=crypt(temp[1]).strip()
        while True:
            if not(passwd.endswith(chr(int("0b11111111",2)))):
                break
            passwd=passwd[:-1]
        if username=="Master":
            mp=passwd
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

mp=""
usrnm_pass=[]
xlen=0
ylen=0

# Default Vaules
passhide="#"
pass_gen_length=18
prefix=" ##"
suffix="## "
TITLE="VAULT v5.3"
delay=2000             # In milliseconds

try:
    open(".settings.config","x")
    init_config()
    config_read()
except:
    try:
        config_read()
    except:
        config_error()

try:
    list_update_read()
    default_login()
except FileNotFoundError:
    open(".pass.crypt","x")
    init_login()
finish()