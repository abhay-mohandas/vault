#curses module is used to draw/print text at any location in the window
import curses 




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
clear=screen.clear                  #
border=screen.border                #
refresh=screen.refresh              #
box=screen.box
sleep=curses.napms

#################################################################################################################################
#title function is used to print titles on screen
def title(title_name):
   y_pos=1
   middle_x=x_mid()
   x_padding=len(title_name)//2
   x_pos=middle_x-x_padding
   screen.addstr(y_pos,x_pos,title_name,bold|highlight)
   #screen.refresh()

def center(y_offset,x_offset,string,style=normal):
   y_pos=y_mid()+y_offset
   middle_x=x_mid()+x_offset
   x_padding=len(string)//2
   x_pos=middle_x-x_padding
   screen.addstr(y_pos,x_pos,string,style)
   screen.refresh()

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
    passbox=screen.subwin(3,100,y_mid()-2,x_mid()-50)
    clear()
    while True:
        border()
        passbox.border()
        title("  VAULT  ")
        center(-3,0,"Enter Master Password",bold)
        center(-1,0,passhash,bold)
        refresh()
        curses.curs_set(1)
        passwd=ckey()
        curses.curs_set(0)
        clear()
        if passwd==10 or passwd==curses.KEY_ENTER: #10 is ENTER key
            if full_pass==mp:
                return
            clear()
            center(1, 0, "Incorrect Password!")
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
        if len(passhash)<84:
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
        title("  VAULT  ")
        center(-3,0,"Enter A New Master Password",bold)
        center(-1,0,passhash,bold)
        refresh()
        curses.curs_set(1)
        passwd=ckey()
        curses.curs_set(0)
        clear()
        if passwd==10 or passwd==curses.KEY_ENTER: #10 is ENTER key
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
        title("  VAULT  ")
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

    if full_pass1==full_pass2:
        clear()
        border()
        center(0, 0, "New Master Password Saved!",bold)
        refresh()
        sleep(4000)
        f=open(".mp.txt","w")   
        f.write(crypt(full_pass1))
        f.close()
        return
    else:
        clear()
        border()
        center(0, 0, "Passwords Doesn't Match! Try Again...")
        refresh()
        sleep(4000)
        return init_login()


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
