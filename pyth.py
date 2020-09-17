#Made: 7/9/18
#Modi: 20/9/18
#By: Jayden
#BombDrop.py
#See if I can make BombDrop using Tkinter. Also as a side note I realize I should have used far less global variables, this was my first real attempt at functions.

#Imports
import time #To allow pauses and to slow down game
from random import * #To place bombs randomly
from tkinter import * #To create the GUI
import pickle #To save info

#Fundumental Variable/list setup
stop_code = 0
highscore_info = [0, 0, 0, 0]

#Database import
pickle.dump(highscore_info, open( "highscore_BombDrop.p", "wb"))

#Feedback to IDLE
print("BombDrop booting on...")

#Code to restart BombDrop
def restart():
    global stop_code
    root.destroy() #Destroyes the GUI
    stop_code = 0

def power_click(input_code=0): #Powerup makes normal+ possible to beat
    global no_bomb_color
    global bomb_color
    global bombs
    global score
    global power_click_sites
    global end
    global cooldown
    global highscore
    global mode_xp
    global xp
    global pause_mode
    
    if input_code == 0 and cooldown == 0: #Makes sure that the user is allowed to activate the powerup
        pause(0) #Pause mode stops the game from running whilst the power mode is enabled
        
        for number in range(100): #This inverts the colors of the bombs to confuse the 
            if number in bombs: #Inverts the bomb colors
                exec("button{0}.configure(bg='{1}', command= lambda: power_click({0}))".format(number, no_bomb_color)) #Switchs the color using my button generation technology
                
            else: #Inverts the non-bomb buttons
                exec("button{0}.configure(bg='{1}', command= lambda: power_click({0}))".format(number, bomb_color)) #Same as above but with non-bomb buttons
                
    elif input_code in bombs and cooldown == 0: #What runs when the user clicks on a safe spot (The bomb locations)
        
        if input_code not in power_click_sites: #Prevents the user from clicking the same spot twice
            points = randint(1, 15) #Adds an element of randomness to the game by randomizing the amount of points given per click
            score += points #Adds the amount of points to the score
            top_label.configure(text="+{}p".format(points)) #Tells the user the amount of points gained per click
            power_click_sites.append(input_code) #Stores the location so that the user can't click on that spot during the minigame
            exec("button{0}.configure(bg='{1}', command= lambda: power_click({0}))".format(input_code, bomb_color)) #Changes the GUI to so that the clicked tile is hidden to prevent confusion with the user
            
    elif cooldown == 0: #Script that runs if the user clicks a non-bomb tile (That kills the user)
        if highscore < score: #Sees if the user has bet the highscore
                    
            top_label.configure(text="You have died, new highscore of {}".format(score), fg="red") #Notifies the user that they have a new highscore
            xp[1] += mode_xp #Gives them extra XP
            highscore = score #Saves the score as the new highscore
            pickle.dump(highscore, open( "highscore_BombDrop.p", "wb")) #Saves highscore to database
                    
        else: #Default response to loss
                    
            top_label.configure(text="YOU HAVE DIED, Score = {}".format(score), fg="red") #Tells user they have lost
            
        end = 1 #Ends the game
        power_click_sites = [] #Clear the clicked spots for next time the powerup is activated
        pause(1) #Unpauses the game
        cooldown = 50 #Stops the user from spamming the powerup
        
    if len(power_click_sites) >= len(bombs): #Checks to see if the user has completed the powerup 
        power_click_sites = [] #Clears powerup storage for next time
        root.after(timing, timer)
        pause_mode = 0
        pause_button.configure(command= lambda: pause(0), bg="green", fg="white", text="Pause")
        cooldown = 50 #Adds a cooldown to the powerup to prevent abuse
        
def pause(freeze): #Allows the user to pause the game
    global pause_mode
    
    if freeze == 0: #Checks if the game is already paused
        freeze = 1 #Stops the game
        pause_button.configure(command= lambda: pause(1), bg="red", fg="white", text="Play") #Changes the name of button to "play"
        
    else: #Runs if the game is already paused
        freeze = 0 #Unpauses the game
        pause_button.configure(command= lambda: pause(0), bg="green", fg="white", text="Pause") #Updates name of button to "Pause"
        root.after(timing, timer) #Reactivates feedback loop in timer to startup game again
        
    pause_mode = freeze #Saves mode

#double special event
def double_event():
    global end
    global event
    global bomb_color
    event = 1
    end = 1
    for number in range(100):
        if number in danger:
            exec("button{}.configure(bg='red', command=danger_double_event)".format(number))
        elif number in safe:
            exec("button{}.configure(bg='green', command=safe_double_event)".format(number))
        else:
            exec("button{}.configure(bg=bomb_color)".format(number))
    top_label.configure(text="Plus or Minus?")
def danger_double_event():
    global end
    global event
    global score
    global level

    choice = randint(0, 4)
    
    if choice == randint(0, 4):
        score += 100
        top_label.configure(text="You win!!! + 100p, new total: {}".format(score))
        end = -4
        event = -4
    else:
        score -= 100
        top_label.configure(text="You lose! - 100p :P. New total: {}".format(score))
        end = -4
        event = -4
def safe_double_event():
    global end
    global event
    top_label.configure(text="Really?")
    end = -4
    event = -4

#Saves and backs up information using pickle
def data_save():
    global xp
    global highscore
    global mode
    global user_data
    global save_color

    #Figures out which difficulty the player is on
    if mode == 0:
        difficulty_mode = 3
    else:
        difficulty_mode = mode - 1

    #Backing up players info
    highscore_info[difficulty_mode] = highscore #Retrieving Highscore
    pickle.dump(highscore_info, open("highscore_BombDrop.p", "wb")) #Saving Highscore
    pickle.dump(xp, open("xp_BombDrop.p", "wb")) #Saving xp
    user_data = [save_color, difficulty_mode] #Retrieving settings
    pickle.dump(user_data, open("user_cache_BombDrop.p", "wb")) #Saving settings/prefrences

#Switches the difficulty level
def switch_mode():
    
    #Lots of global variables *Bad
    global mode
    global highscore
    global on_bomb
    global replace_red
    global timing_difficulty
    global click_points
    global easy_highscore
    global normal_highscore
    global hard_highscore
    global score
    global level
    global stupid_highscore
    global mode_xp
    global no_bomb_color
    global trans_color

    if xp[0] >= 3: #Prevents Unknown button error
        #Main if/else statment for finding which mode to switch to
        if mode == 0: #Easy mode
            
            score = (level - 1) * 50 + 1 #Resets the score
            mode = 1
            mode_name = "Easy"
            difficulty_button.configure(text="Easy") #Updates the difficulty button on the GUI
            timing_difficulty = 3 #Speed the code updates the GUI
            click_points = 5 #Points earned every button click
            highscore = easy_highscore #Stores which mode the highscore should be pickled as.
            mode_xp = 1
        elif mode == 1: #Normal Mode
            
            score = (level - 1) * 50 + 1 #Resets score
            highscore = normal_highscore #Stores which mode needs to be pickled.
            click_points = 1 #Points per button click
            mode_name = "Normal"
            mode = 2
            difficulty_button.configure(text="Normal") #Updates difficulty button on GUI
            bomb_color = save_color #Changes the bomb color to be visible
            timing_difficulty = 4
            mode_xp = 2
        elif mode == 2: #Hard Mode
            
            click_points = 2 #Points per click
            score = (level - 1) * 50 + 1 #Resets the score to stop cheating/glitching tons of points.
            mode_name = "Hard"
            highscore = hard_highscore #Saves which mode user has selected
            mode = 3
            difficulty_button.configure(text="Hard") #Updates GUI
            bomb_color = no_bomb_color #Makes the bombs invisable
            timing_difficulty = 5 #Speed
            mode_xp = 7
        else: #Stupid mode (Near impossible)
            
            click_points = 1 #Points per click 
            score = (level - 1) * 50 + 1
            mode_name = "Stupid" #Mode name
            highscore = stupid_highscore #Selects the correct databases to save to
            mode = 0
            difficulty_button.configure(text="Stupid") #Updates GUI
            bomb_color = no_bomb_color #Makes the bombs invisable
            timing_difficulty = 6 #Speed
            mode_xp = 10
            trans_color = no_bomb_color

            #Makes all pre-existing bombs invisable
            try: #Prevents crashes
                for nuke in bombs: #Locates bombs
                    exec('button{}.configure(bg="{}")'.format(nuke, bomb_color)) #Makes the bombs invisable
            except NameError: #Unsure what causes this error
                top_label.configure(text="Welp, I almost crashed.") #Notifies the user that the game almost crashed
    else:
        score = (level - 1) * 50 + 1 #Resets the score
        mode = 1
        mode_name = "Easy"
        timing_difficulty = 2 #Speed the code updates the GUI
        click_points = 5 #Points earned every button click
        highscore = easy_highscore #Stores which mode the highscore should be pickled as.
    top_label.configure(text="{} Highscore is {}!".format(mode_name, highscore)) #Tells the user the highscore for their difficulty level

#Allows the user to reset their score and level
def reset():

    #Globalizes variables
    global reset_highscore
    global highscore_info
    global highscore
    global xp
    global end

    #If/else used to confirm reset (To stop incidents)
    if reset_highscore == 0: #0 meaning it is the first time the user has clicked the reset button
        
        reset_highscore = 1 #Tells the code to run the else statement next time
        top_label.configure(text="Click Reset again to confirm", fg="red") #Updates GUI
    else: #Actually resets users data

        #Resets variables/lists
        reset_highscore = 0
        highscore = 0
        highscore_info = [0, 0, 0]
        xp = [0, 0]

        #Updates GUI
        top_label.configure(text="Game ended due to reset", fg="red")

        #Updates databases
        data_save()

        #Stops game
        end = 1

#Function for changing the GUI's color
def background(color): #Background meaning GUI

    #Globalizes variables
    global bg_color
    global bomb_color
    global no_bomb_color
    global save_color
    global checker
    global possible_modes
    global trans_bomb
    global trans_color
    global mode

    #Remembers the users color prefrence so it can save it in the databases
    save_color = color
    if xp[0] >= 12:
        #Sees which color the user selected (Used instead of multiple functions running individual color changes as it is faster to run a elif statement)
        if color == "purple": #Checks if the color chosen is purple
            
            bg_color = "purple" #Selects the background buttons color (PURPLE)
            bomb_color = "pink" #Selects the background color for bombs (Only on normal and easy) (PINK)
            no_bomb_color = "mediumVioletRed" #Selects the background color for non-bomb sites (Only on normal and easy) (VIOLET-RED)
            difficulty_button.configure(bg="pink", fg="purple") #Changes the difficulty buttons color
            reset_button.configure(bg="pink", fg="purple") #Changes the reset buttons color
            trans_color = "magenta"
            
        elif color == "gray": #Checks if the chosen color is gray (Essentually resets color)
            
            bg_color = "green" #Selects the background buttons color (GREEN)
            bomb_color = "white" #Selects the background color for bombs (Only on normal and easy) (WHITE)
            no_bomb_color = "gray" #Selects the background color for non-bomb tiles (Only on normal and easy) (GRAY)
            difficulty_button.configure(bg="whiteSmoke", fg="black") #Changes the color of the Difficulty changer
            reset_button.configure(bg="whiteSmoke", fg="black") #Changes the color for the reset button & text
            trans_color = "light gray"
            
        elif color == "green": #Checks if the chosen color is green
            
            bg_color = "light green" #Same as line 173 (LIGHT GREEN)
            bomb_color = "lawnGreen" #Same as line 174 (LAWN GREEN)
            no_bomb_color = "green" #Same as line 175 (GREEN)
            difficulty_button.configure(bg="forestGreen", fg="lawnGreen") #Same as line 176
            reset_button.configure(bg="forestGreen", fg="lawnGreen") #Same as line 177
            trans_color = "forestGreen"
            
        elif color == "blue": #Checks if chosen color is blue
            
            bg_color = "blue" #Explanation on line 173 (BLUE)
            bomb_color = "dark blue" #Explanation on line 174 (DARK BLUE)
            no_bomb_color = "deepSkyBlue" #Explanation on line 175 (DEEP SKY BLUE)
            difficulty_button.configure(bg="royalBlue", fg="powderBlue") #Explanation on line 176
            reset_button.configure(bg="royalBlue", fg="powderBlue")#Explanation on line 177
            trans_color = "royalBlue"
            
        elif color == "yellow": #Checks if color is yellow
            
            bg_color = "gold" #Full explanation on line 173 (GOLD)
            bomb_color = "brown" #Full explanation on line 174 (BROWN)
            no_bomb_color = "dark orange" #Full explanation on line 175 (DARK ORANGE)
            difficulty_button.configure(bg="light yellow", fg="orange") #Full explanation on line 176
            reset_button.configure(bg="light yellow", fg="orange") #Full explanation on line 177
            trans_color = "light yellow"
            
    else:
        bg_color = "green" #Selects the background buttons color (GREEN)
        bomb_color = "black" #Selects the background color for bombs (Only on normal and easy) (WHITE)
        no_bomb_color = "white" #Selects the background color for non-bomb tiles (Only on normal and easy) (GRAY)
        trans_color = "gray"

    #Sets the background for the restart button
    stop_button.configure(bg=no_bomb_color)
    if mode == 0:
        trans_color = no_bomb_color

    #Updates the GUI with new colors
    for number in range(100): #There is 100 buttons on the board
        
        if number in bombs and mode in possible_modes: #Tests if the specificed button is on a bomb and user is in hard or stupid modes
            exec(replace_red.format(number, ',bg="{}" ,text="  "'.format(no_bomb_color))) #The exec() function allows me to run str as code. This allows me to generate code on demand

        elif number in trans_bomb: #Transition color to show user where the next bomb is going to drop
            exec("button{}.configure(bg='{}')".format(number, trans_color)) #Sets trans-bomb to the users preferred color
            
        elif number in bombs: #Tests if specified button is a bomb and user has selected easy or normal
            exec(replace_red.format(number, ',bg="{}" ,text="  "'.format(bomb_color))) #Generates  100 buttons with 1 line
            
        elif number in near_bombs: #Tests if specified button is next to a bomb
            exec(replace_orange.format(number, ',bg="{}" ,text="  "'.format(no_bomb_color))) #Same as Line 214
            
        else: #If there is nothing special about the button then it defaults
            exec(replace_green.format(number, ',bg="{}" ,text="  "'.format(no_bomb_color), bg_color)) #Same as line 214

#Updates the GUI when you level up. 
def level_update():

    #Global variables
    global color_tier
    global easy_attempt
    global reset_attempt
    global difficulty_button
    global reset_button

    #Script that checks which level you are on and what you gain with that.
    if xp[0] >= 12: # Checks to see if you are above or at level 12

        #Unlocks the first background switcher button (PINK)
        if color_tier <= 1:
            
            purple_background = Button(root, text="Pink", command= lambda: background("purple"), activebackground="white", bg="deepPink", fg="whiteSmoke") #setup for new button
            purple_background.grid(row=12, column = 0, columnspan = 2, pady=5) #Adds new button to GUI
            color_tier += 1 #Setup for next time the user levels up

        #Unlocks all other background buttons
        if xp[0] >= 14:

            #Reset button
            if color_tier <= 2:
                gray_background = Button(root, text="Gray", command= lambda: background("gray"), activebackground="white", bg="gray", fg="whiteSmoke") #Setup
                gray_background.grid(row=12, column = 2, columnspan = 2) #Adds button
                color_tier += 1 #Setup for next time

            if xp[0] >= 16: #Tests if user is above level 16

                #Green background button
                if color_tier <= 3:
                    
                    green_background = Button(root, text="Green", command= lambda: background("green"), activebackground="white", bg="forestGreen", fg="whiteSmoke") #Setup
                    green_background.grid(row=12, column = 4, columnspan = 2) #Adds Green button
                    color_tier += 1#Setup for next time

                if xp[0] >= 18: #Tests if user is above level 18

                    #Blue background color
                    if color_tier <= 4:
                        
                        blue_background = Button(root, text="Blue", command= lambda: background("blue"), activebackground="white", bg="dodgerBlue", fg="whiteSmoke") #Setup
                        blue_background.grid(row=12, column = 6, columnspan = 2) #Adds Blue button
                        color_tier += 1 #Setup for when function is next called

                    if xp[0] >= 20: #Tests if user is above level 20

                        #Yellow background button
                        if color_tier <= 5:
                            
                            yellow_background = Button(root, text="Yellow", command= lambda: background("yellow"), activebackground="white", bg="orange", fg="whiteSmoke") #Setup
                            yellow_background.grid(row=12, column = 8, columnspan = 2) #Adds yellow button to GUI
                            color_tier += 1 #Prevents the yellow button from being created twice

    #Tests if script should display the difficulty changer on the GUI
    if xp[0] >= 3:  #tests if the user is at or higher then level 3
        
        if easy_attempt < 1: #Stops the script from generating more then one difficulty button 
            difficulty_button = Button(root, text="Easy", command=switch_mode, bg="whiteSmoke") #Setup for difficulty button
            difficulty_button.grid(row=0, columnspan = 2, sticky = "w") #Runs new button in GUI
            easy_attempt += 1 #Records click
            
    if xp[0] >= 10: #Tests is the user is at or higher then level 10
        
        if reset_attempt < 1: #Stops the script from creating multiple reset buttons
            reset_button = Button(root, text="Reset", command=reset, activebackground="red", bg="whiteSmoke") #Setup for reset button
            reset_button.grid(row=0, columnspan = 10, sticky = "e") #Updates the GUI with new button
            reset_attempt += 1 #Records click and prevents duplicate buttons

#Code called when a 100 button (One inside the grid) is clicked
def button_code(num): #The function requires the code number to figure out where the button is located

    #Global variables
    global reset_highscore
    global go
    global tested_sites
    global click_points
    global pause_mode
    
    #Variable setup
    go += 1
    reset_highscore = 0

    #Chooses what to execute (Heart of function)
    if go > 1 and pause_mode == 0: #Makes sure this is the first time user has clicked on the board (To stop them dying instintally)

        #Global Variable setup
        global score
        global highscore
        global end
        global mode_xp

        #Heart of function
        if end == 0: #Makes sure the code is still running
            if num in bombs and num != latest_bomb: #Sees if the user has clicked on a bomb
                end = 1 #Stops the game
                if highscore < score: #Sees if the user has bet the highscore
                    
                    top_label.configure(text="You have died, new highscore of {}".format(score), fg="red") #Notifies the user that they have a new highscore
                    xp[1] += mode_xp #Gives them extra XP
                    highscore = score #Saves the score as the new highscore
                    pickle.dump(highscore, open( "highscore_BombDrop.p", "wb")) #Saves highscore to database
                    
                else: #Default response to loss
                    
                    top_label.configure(text="YOU HAVE DIED, Score = {}".format(score), fg="red") #Tells user they have lost

            elif num in tested_sites: #Checks if the user clicked on a previously clicked spot
                
                if len(tested_sites) < total_safe_spots: #Checks if there are any spots remaining
                    top_label.configure(text="Score: {} -Already clicked there.".format(score), fg="black") #Tells the user to stop clicking there
                    
                else: #Resets spots as the user has ran out of spaces to click
                    
                    tested_sites = [] #Resets tested spots
                    score += click_points #Adds more points to the score
                    top_label.configure(text="Score: {}".format(score), fg="black") #Tells the user their score
                    tested_sites.append(num) #Adds the clicked on spot to the tested spots list
                    xp[1] += mode_xp #Gives the user more xp
                
            else: #Default option
                
                score += click_points #Gives user points
                top_label.configure(text="Score: {}".format(score), fg="black") #Tells the user their score
                tested_sites.append(num) #Adds the clicked on spot to the tested spots list
                xp[1] += click_points #Gives the user xp
                
    elif pause_mode == 0: #Starts the game
        top_label.configure(text="Go!", fg="green") #Tells the user to start the game

def timer():
    global level_up
    global total_safe_spots
    global end
    global timing
    global timing_difficulty
    global advance_score
    global tested_sites
    global highscore
    global bomb_amount
    global win
    global level
    global game_level
    global no_bomb_color_checker
    global trans_bomb
    global trans_color
    global pause_mode
    global cooldown

    if end < 0:
        end += 1
    if pause_mode == 0:
        if end == 0:
            if total_safe_spots < 0:
                if score >= advance_score:
                    if level < 23:
                        xp[1] += 50
                        advance_score += 50
                        bombs.clear()
                        near_bombs.clear()
                        tested_sites.clear()
                        total_safe_spots = 100
                        level += 1
                        top_label.configure(text="Level {}!".format(level), fg="purple")
                        button9.configure(text=level, fg="white", bg="black")
                        game_level = 3
                    else:
                        print(level, xp[0])
                        end = 1
                        xp[1] += 1000
                        if score <= highscore:
                            top_label.configure(text="Game Complete!, score is {}.".format(score), fg="green")
                        else:
                            top_label.configure(text="Game Complete, new highscore of {}!".format(score), fg="green")
                            highscore = score
                            button12.configure(bg="black")
                        timing = 50
                        win = 1
                else:
                    end = 1
                    if highscore >= score:
                        top_label.configure(text="Not enough points, score: {}".format(score), fg="red")
                    else:
                        top_label.configure(text="Not enough points, highscore of {}.".format(score), fg="red")
                        xp[1] += 10
                for number in range(100):
                    exec(replace_green.format(number, ',bg="{}", text="  "'.format(bomb_color), bg_color))
            bomb_create()
            for number in range(100):
                if number != 0 or level_up < 1:
                    if number != 9 or game_level < 1:
                        if number in bombs and mode in possible_modes:
                            exec(replace_red.format(number, ',bg="{}" ,text="  "'.format(no_bomb_color)))
                        elif number in bombs:
                            exec(replace_red.format(number, ',bg="{}" ,text="  "'.format(bomb_color)))
                        elif number in trans_bomb:
                            exec("button{}.configure(bg='{}')".format(number, trans_color))
                        elif number in near_bombs:
                            exec(replace_orange.format(number, ',bg="{}" ,text="  "'.format(no_bomb_color)))
                        else:
                            exec(replace_green.format(number, ',bg="{}" ,text="  "'.format(no_bomb_color), bg_color))
            
            if level_up > 0:
                level_up -= 1
            if game_level > 0:
                game_level -= 1
            timing -= timing_difficulty
            if timing < 5:
                if bomb_amount > 4:
                    end = 1
                    if highscore >= score:
                        top_label.configure(text="Time ran out!, score: {}".format(score), fg="red")
                    else:
                        top_label.configure(text="Time ran out!, new highscore of {}".format(score), fg="red")
                        xp[1] += 10
                        highscore = score
                else:
                    timing = 500
                    bomb_amount *= 2
                    xp[1] += bomb_amount * 10
        elif win == 1:
            for number in range(100):
                if number != 0 or level_up < 1:
                    if number != 9 or game_level < 1:
                        if number in bombs and mode == 0:
                            exec(replace_red.format(number, ',bg="{}" ,text="  "'.format(no_bomb_color)))
                        elif number in bombs:
                            exec(replace_red.format(number, ',bg="{}" ,text="  "'.format(bomb_color)))
                        elif number in trans_bomb:
                            exec("button{}.configure(bg='{}', text="  ")".format(number, trans_color))
                        elif number in near_bombs:
                            exec(replace_orange.format(number, ',bg="{}" ,text="  "'.format(no_bomb_color)))
                        else:
                            exec(replace_green.format(number, ',bg="{}" ,text="  "'.format(no_bomb_color), bg_color))
            for number in range(100):
                if number in credit:
                    exec("button{}.configure(bg='black')".format(number))
            for location in range(len(credit)):
                if credit[location] < 100:
                    credit[location] += 10
                else:
                    credit[location] -= 100
            stop_button.configure(bg="green")
        elif event == 0:
            stop_button.configure(bg="red")
        if xp[1] >= xp[0] * 100 and end >= 0:
            xp[0] += 1
            xp[1] -= xp[0] * 5
            button0.configure(text=xp[0], fg="white", bg="black")
            level_up = 3
            level_update()
        data_save()
        if level < 23 and total_safe_spots < 0 and end >= 0:
            print(end)
            double_event()
        if cooldown > 0:
            if cooldown == 50:
                power_button.configure(text=" ||||")
            elif cooldown == 40:
                power_button.configure(text=" ||||")
            elif cooldown == 30:
                power_button.configure(text="  |||")
            elif cooldown == 20:
                power_button.configure(text="   ||")
            elif cooldown == 10:
                power_button.configure(text="    |")
            cooldown -= 1
        else:
            power_button.configure(text="Click++")
                
        root.after(timing, timer)
def bomb_create():
    global total_safe_spots
    global bombs
    global near_bombs
    global bomb_amount
    global latest_bomb
    global trans
    global bomb_location
    global stop
    global attempt
    global trans_bomb
    #Main bomb location
    if trans == 0:
        for i in range(bomb_amount):
            stop = 0
            attempt = 0
            while stop == 0 and attempt < 250:
                bomb_location = randint(0,101)
                if bomb_location in bombs or bomb_location in trans_bomb:
                    attempt += 1
                else:
                    stop = 1
                    trans_bomb.append(bomb_location)
        trans = 1
    else:
        for bomb in trans_bomb:
            latest_bomb = bomb
            total_safe_spots -= 1
            bombs.append(bomb)
            #Area around the bomb
            near_bombs.append(bomb + 1)#Right side
            near_bombs.append(bomb - 1)#Left side
            near_bombs.append(bomb + 10)#Top
            near_bombs.append(bomb - 10)#Bottom
            trans = 0
            trans_bomb = []
        
#Main script
while stop_code == 0:

    #Setup for GUI
    root = Tk()

    #Some Primary variables
    mode = "1"
    stop_code = 1
    
    #The code to create 100 buttons. (Instead of writing them individually.)
    no_bomb = 'button{0} = Button(root, text="  ",width=3, activebackground="{2}", bg="{1}", command = lambda: button_code({0}))' #Safe button
    near_bomb = 'button{0} = Button(root, text="  ",width=3, activebackground="orange", bg="{1}", command = lambda: button_code({0}))' #Nearby bomb button
    on_bomb = 'button{0} = Button(root, text="  ",width=3, activebackground="red", bg="{1}", command = lambda: button_code({0}))' #Bomb button
    replace_red = 'button{0}.configure(command = lambda: button_code({0}), activebackground="red"{1})'
    replace_green = 'button{0}.configure(command = lambda: button_code({0}), activebackground="{2}"{1})'
    replace_orange = 'button{0}.configure(command = lambda: button_code({0}), activebackground="orange"{1})'
    save_site = "button{}.grid(row={},column={})" #Creates button
    
    #Secondary Variables setup

    #100 Button variables
    row = 1 #Tells game builder to start on row 1
    total_safe_spots = 100 #How large the grid is
    column = 0 #Sets the starting column to 0 so it can build the GUI correctly
    valid_row = 0 #Sets the starting row to 0

    #Default color settings
    bg_color = "green" #Default click-on button color
    bomb_color = "white" #Default visible bomb color
    no_bomb_color = "gray" #Default background color
    no_bomb_color_checker = "gray" #Default Color for non-bomb sites
    save_color = "gray" #Default color for next round
    trans = 0
    trans_bomb = []
    trans_color = "gray"

    #Level up system
    color_tier = 0 #Tells the level up system to not start yet
    click_points = 1 #Sets the points per click to 1
    reset_highscore = 0 #Resets the highscore for the round
    level_up = 0 #Tells the code not to level up the player
    reset_attempt = 0 #Setup for the reset button
    mode_xp = 0

    #Difficulty setup
    mode = 2 #What difficulty it should default to
    timing_difficulty = 5 #Speed bombs should appear at
    easy_attempt = 0 #Setup for the difficulty button
    possible_modes = [0, 3] #Tells the code when to show bombs and when to hide them (0=Easy, 3=Normal)

    #Game Level
    game_level = 0 #Sets the game to level 1
    level = 1 #What level the player should start on

    #Bomb resets
    near_bombs = [] #Clears the locations of near-bomb sites
    bomb_amount = 1 #Tells the code to start with 1 bomb at a time
    credit = [-64, -65, -66, -55, -45, -35, -26] #Setup for the ending scene
    latest_bomb = 0 #Tells the code not to add any bombs yet
    tested_sites = [] #List for storing which sites user has checked
    bombs = [] #Clears the locations of bombs from previous rounds
    non_filled_sites = []
    for i in range(100):
        non_filled_sites.append(i)

    #Game engine
    advance_score = 50 #Tells what the minimium amount is to advance to the next level
    end = 0 #Tells the code not to end the game immedietly
    go = 0 #Variable used later in the code
    timing = 1000 #The beginning speed bombs should appear at in ms
    win = 0 #Tells the code the user hasn't won
    checker = 0 #Checks stuff
    score = 1 #Starts the score at 1
    
    #Database setup
    highscore_info = pickle.load( open( "highscore_BombDrop.p", "rb")) #Gets my Highscore
    easy_highscore = highscore_info[0] #Retrieves Easy mode highscore from database
    normal_highscore = highscore_info[1] #Retrieves Normal mode highscore from database
    hard_highscore = highscore_info[2] #Retrieves Hard mode from database

    #Double event
    danger = [22, 23, 24, 32, 33, 34, 42, 43, 44]
    safe = [25, 26, 27, 35, 36, 37, 45, 46, 47]
    event = 0

    #Pause setup
    pause_mode = 0 #Stops game
    pause_button = Button(root, text="Pause", command= lambda: pause(0), bg="white", fg="green")
    pause_button.grid(row=13, column=8, columnspan=2, sticky="we")

    #Power click setup
    cooldown = 0
    power_click_sites = []
    power_button = Button(root, text="Click++", command= lambda: power_click(0), bg="white", fg="green")
    power_button.grid(row=13, column=0, columnspan=2, sticky="we")
    
    #Retrieves Stupid mode from database
    try: #Prevents Restart/reset Error
        stupid_highscore = highscore_info[3] #Retrieves mode
        
    except IndexError: #Prevents the IndexError related to Restart/reset Error
        print("To restart games after resets please reboot this game") #Instructs the user from the terminal

    #Xp retrieval
    highscore = normal_highscore #Default setup for highscore
    xp = pickle.load( open("xp_BombDrop.p", "rb")) #Gets xp level from database
    timing -= xp[0] * 3 #Sets timing to xp level
    
    #Top label setup
    top_label = Label(root, text="Welcome! Score to beat is {}".format(highscore), fg="black", pady=7) #Setup for top label
    top_label.grid(row = 0, columnspan = 10, sticky = "we") #Updates GUI with top label

    #Stop button setup
    stop_button = Button(root, text="Replay", command=restart, bg=no_bomb_color, fg="black") #Setup for stop button
    stop_button.grid(row=13, column=3, columnspan=4, sticky="we") #Updates GUI with stop button

    #Other GUI related setup
    root.title("BombDrop") #Sets the title
    level_update()
    
    #Creates GUI
    for number in range(100): #Makes 100 buttons
        #Sees if it needs to add a new line
        temp_var = int(number / 10) #Sees if it has reached max for that row
        if temp_var == valid_row: #Tells code to go down a row
            valid_row += 1 #Decreases row
            row += 1 #Not sure what this does (Don't want to break anything)
            column = 0 #Resets column
        else:
            column += 1
        #Creates the button
        if number in bombs: #Sees if the button is a bombsite
            exec(on_bomb.format(number, bomb_color))#Retrieves bomb button string and converts to code
            exec(save_site.format(number, row, column))#Retrieves "save_site" script and converts to code
        elif number in near_bombs:#Sees if button is near a bomb site
            exec(near_bomb.format(number, no_bomb_color))#Same as above but with "near_bomb"
            exec(save_site.format(number, row, column))#Same as above
        else:#Else it will store as a safe spot
            exec(no_bomb.format(number, no_bomb_color, bg_color))#Same as above but with "no_bomb" script
            exec(save_site.format(number, row, column))#Same as above
    
    #Pre-GUI setup
    root.after(timing, timer) #Setup so the GUI is dynamic not static
    user_data = pickle.load(open("user_cache_BombDrop.p", "rb")) #Gets the user cache (Color, difficulty etc)

    #Sets up user settings
    background(user_data[0]) #Sets background to what the user has chosen
    mode = user_data[1] #Sets the difficulty to what the user has chosen
    switch_mode() #Updates GUI with new information

    #Execution of GUI
    print("GUI Setup Complete.")
    root.mainloop()

    #Notifies the user when the game engine stops
    print("Game ended.")