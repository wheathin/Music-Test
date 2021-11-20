# Ethan Wong
# CSCI 101 - Section E
# Create Project
# References:

# Library imports
from tkinter import *
import eyed3
import pygame
import random
import fnmatch
import os
import glob

# Define variables
song_list = []
title_list = []
used_num = [-1]
score = 0

# Define Functions

# Basic play and stop music functions
pygame.mixer.init()

def play():

    # Global variables
    global song
    global s_title
    global s_file
    global s_label
    
    # Random song selector
    rng = random.randint(0, len(song_list) - 1)
    
    if(len(song_list) != len(used_num) - 1):
        while (rng in used_num):
            rng = random.randint(0, len(song_list) - 1)
        
        used_num.append(rng)

        # Reads song data
        song = eyed3.load(song_list[rng])
        s_title = song.tag.title
        s_file = song_list[rng]
        s_time = song.info.time_secs

        ran_time = random.randint((int(s_time) // 5), (4 * int(s_time) // 5))
        
        pygame.mixer.music.load(s_file)
        pygame.mixer.music.play(loops=0, start=ran_time)
        pygame.mixer.music.set_volume(0.25)

    # Case for when there are no more songs    
    else:
        pygame.mixer.music.stop()
        submit_button.destroy()
        s_select.destroy()
        disp_text.config(text='The test is over; here are the results!')
        disp_score.config(text=f'Final Score: {score} out of {len(song_list)}')
    
    return (song, s_title, s_file)

# Starts the game
def start():
    global submit_button
    global s_select
    
    disp_text.config(text='What song is currenty playing?')
    disp_score.config(text=f'Score: {score}')
    start_button.destroy()
    play()

    submit_button = Button(root, text='Submit', font=('Helvetica', 32), command= lambda: submit(score))
    submit_button.pack(pady=20)

    s_label = Label(root, text='')
    s_label.pack()

    s_select = OptionMenu(root, selected, *title_list)
    s_select.pack()

# Submits an answer from a dropdown list
def submit(s):
    global score
    
    answer = selected.get()

    if(answer == s_title): 
        s += 1
        score = s
        disp_score.config(text=f'Score: {s}')
        
    play()

    return score
    
# Scans all songs in the Songs folder
for song in glob.glob(os.path.join('Songs/', '*.mp3')):
    with open(os.path.join(os.getcwd(), song), 'r') as s:
        song_list.append(s.name)
for t in song_list:
    t_dat = eyed3.load(t)
    title_list.append(t_dat.tag.title)

# Initialize interface
root = Tk()

# Interface design
root.title('Music Cognition Test')
root.geometry('800x400')

# Main menu
disp_text = Label(root, text='Welcome to the Music Cognition Test!', font=('Helvetica', 32))
disp_text.pack()

disp_score = Label(root,text='', font=('Helvetica', 32))
disp_score.pack()

start_button = Button(root, text='Press to Start', font=('Helvetica', 32), command=start)
start_button.pack(pady=20)

selected = StringVar()

root.mainloop()
