import tkinter
import customtkinter
import pygame
import time
from customtkinter import filedialog
from CTkListbox import *
from tkinter import messagebox
from tkinter.ttk import *
from PIL import Image, ImageTk


# Required variables
paused=True
first_play=True
song_length=100

# Songs list
list_of_songs=[]
pygame.mixer.init()

# Functions
def add_song():
    song_list = filedialog.askopenfilenames(title="Select Songs", filetypes=(("mp3 Files", "*.mp3"),))
    # print(song_list)
      
    for song in song_list:
        if song not in list_of_songs:
            row_value = add_song_btn.grid_info()['row']
            for song_index in range(len(song_list)):
                row_value+=1
                # print(song_list[song_index].split('/')[-1])        
                playlist_box.insert("END", song_list[song_index].split('/')[-1])

                list_of_songs.append(song_list[song_index])# Adding song with path to list
            # row_value=add_song_btn.grid_info()['row']
            # print(row_value+1)
            add_song_btn.grid(row=row_value+1)# Changing position of add song button
            del_song_btn.grid(row=row_value+1)
            # Default option activation
            playlist_box.activate(0)
        else:
            print("Song Already Present")
    

def del_song():
    global first_play, paused

    # Get current selected Song
    current_song=playlist_box.curselection() # Index number
    # Deactivate current option
    playlist_box.deactivate(index=current_song)
    # Delete Song
    playlist_box.delete(index=current_song) # Delete Song from GUI
    del list_of_songs[current_song] # Dlete song from list
    pygame.mixer.music.unload() # Unload Music

    song_title.configure(text="Song Title")
    play_button.configure(image=play_img)
    song_progress.set(0)
    time_elapsed_label.configure(text="00:00")
    time_total_label.configure(text="00:00")

    first_play=True
    paused=True

def progress(value):
    global paused, first_play

    current_time=song_progress.get()
    current_time_conv=time.strftime('%M:%S', time.gmtime(current_time))

    # Change label
    time_elapsed_label.configure(text=current_time_conv)

    if not paused:
        pygame.mixer.music.play(start=value)
    else:# If the song is Paused and the position of slider is changed
        pygame.mixer.music.play(start=value)
        pygame.mixer.music.pause()
        paused=True

def song_changed(selected_option):
    global first_play, paused
    print("Song Changed")
    song_title.configure(text=selected_option.strip(".mp3"))
    # Unload previous playing song and configure button
    pygame.mixer.music.unload()
    play_button.configure(image=play_img)
    song_progress.set(0)
    time_elapsed_label.configure(text="00:00")
    paused=True
    first_play=True

    # Search the path of selected song
    for path in list_of_songs:
        if selected_option in path:
            # print(path)
            current_song=path
            break
    global song_length
    song_length=pygame.mixer.Sound(current_song) # Convert str to object
    song_conv_len=song_length.get_length() # Total length in seconds
    song_conv_len=time.strftime('%M:%S', time.gmtime(song_conv_len))
    # Change label
    time_total_label.configure(text=song_conv_len)
    # Change length of progressbar
    song_progress.configure(to=int(song_length.get_length()))

def play_time():
    global paused, first_play, song_length
    # Get current position in Song
    current_time=pygame.mixer.music.get_pos()/1000
    # print("Song Progress : ", current_time)
    # print("Bar Progress : ", song_progress.get())
    current_time_conv=time.strftime('%M:%S', time.gmtime(current_time))

    # If the song is ended
    if int(song_progress.get())==int(song_length.get_length()):
        print("Song Ended")
        current_time_conv=time.strftime('%M:%S', time.gmtime(song_progress.get()))
        # Change label
        time_elapsed_label.configure(text=current_time_conv)

        # Stop the music and set paused=True and change button
        pygame.mixer.music.stop()
        play_button.configure(image=play_img)
        paused=True


    # If the song is 1 second ahead of progressbar
    elif int(current_time)==int(song_progress.get())+1:
        print("Song is 1 second ahead")
        # Change label
        time_elapsed_label.configure(text=current_time_conv)
        # Change position of Progress Bar
        song_progress.set(current_time)

    # If the position of song is changed manually
    else:
        current_time=song_progress.get()
        current_time_conv=time.strftime('%M:%S', time.gmtime(current_time))

        # Change label
        time_elapsed_label.configure(text=current_time_conv)

        new_pos=int(song_progress.get())+1
        song_progress.set(new_pos)
    # If the song is not paused loop the function
    if not paused and not first_play:
        # Loop the function every 1 second
        song_progress.after(1000, play_time)

def play_music():
    global paused, first_play
    
    song_name = playlist_box.get()# Get selected option

    # If no Song is selected
    if song_name==None:
        print("No Song Selected")
        messagebox.showinfo("showinfo", "Please Select a Song")
    else:
        # Search the path of selected song
        for path in list_of_songs:
            if song_name in path:
                # print(path)
                current_song=path
                break
        # print(current_song)
        song_name=current_song.split('/')[-1].strip('.mp3')
        song_title.configure(text=song_name)

        if first_play:
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.5)
            first_play=False
            paused=False

            global song_length
            song_length=pygame.mixer.Sound(current_song) # Convert str to object
            song_conv_len=song_length.get_length() # Total length in seconds
            song_conv_len=time.strftime('%M:%S', time.gmtime(song_conv_len))
            # Change label
            time_total_label.configure(text=song_conv_len)
            # Change length of progressbar
            song_progress.configure(to=int(song_length.get_length()))
            # Configure Play button
            play_button.configure(image=pause_img)
        else:
            if paused:# If the song is Paused
                pygame.mixer.music.unpause()
                play_button.configure(image=pause_img)
                paused=False
            else:
                pygame.mixer.music.pause()
                play_button.configure(image=play_img)
                paused=True

        play_time()
def next_song():
    global first_play, paused, song_length

    # Get current selected song
    selected_song=playlist_box.curselection() # Index number of song
    
    # Check indexing in list
    if (selected_song+1)<(len(list_of_songs)):
        # Clear selection
        playlist_box.deactivate(selected_song)

        # Activate next song
        playlist_box.activate(selected_song+1)

        first_play=True
        paused=True

        song_progress.set(0)
        time_elapsed_label.configure(text="00:00")

        # Update the song length time and progressbar length
        song_name=playlist_box.get()
        # print(song_name)
        # Search the path of selected song
        for path in list_of_songs:
            if song_name in path:
                # print(path)
                current_song=path
                break
        # print(current_song)
        song_length=pygame.mixer.Sound(current_song) # Convert str to object
        song_conv_len=song_length.get_length() # Total length in seconds
        song_conv_len=time.strftime('%M:%S', time.gmtime(song_conv_len))
        # Change label
        time_total_label.configure(text=song_conv_len)
        # Change length of progressbar
        song_progress.configure(to=int(song_length.get_length()))

def prev_song():
    global first_play, paused
    
    # Get current selected song
    selected_song=playlist_box.curselection() # Index number of song
    
    # Check indexing in list
    if (selected_song-1) in range(len(list_of_songs)):
        # Clear selection
        playlist_box.deactivate(selected_song)

        # Activate next song
        playlist_box.activate(selected_song-1)

        first_play=True
        paused=True

        song_progress.set(0)
        time_elapsed_label.configure(text="00:00")

        song_name=playlist_box.get()
        # print(song_name)
        # Search the path of selected song
        for path in list_of_songs:
            if song_name in path:
                # print(path)
                current_song=path
                break
        # print(current_song)
        song_length=pygame.mixer.Sound(current_song) # Convert str to object
        song_conv_len=song_length.get_length() # Total length in seconds
        song_conv_len=time.strftime('%M:%S', time.gmtime(song_conv_len))
        # Change label
        time_total_label.configure(text=song_conv_len)
        # Change length of progressbar
        song_progress.configure(to=int(song_length.get_length()))

def sound_controller(value):
    # print(value)
    pygame.mixer.music.set_volume(value)

# Function to update the image inside the image_frame
def update_image():
    # Load the image
    image_path = "images/CDcover.png"  # Replace with the path to your image file
    img = Image.open(image_path)

    # Resize the image to fit inside the image_frame
    img = img.resize((200, 200))  # Use Image.ANTIALIAS here

    # Convert the image to Tkinter format
    tk_img = ImageTk.PhotoImage(img)

    # Update the image in the Label widget
    image_label.configure(image=tk_img)
    image_label.image = tk_img  # Keep a reference to avoid garbage collection

app = customtkinter.CTk()
app.geometry("840x600")
app.resizable(0,0)
app.title("Py Music Player")

# Required Images
play_img=tkinter.PhotoImage(file=r'images\Play.png')
pause_img=tkinter.PhotoImage(file=r'images\Pause.png')
next_img=tkinter.PhotoImage(file=r'images\Next.png')
prev_img=tkinter.PhotoImage(file=r'images\Previous.png')

image_frame=customtkinter.CTkFrame(master=app, width=300, height=300)
image_frame.grid(row=0, column=1, pady=10)

# Create a Label widget to display the image
image_label = customtkinter.CTkLabel(master=image_frame, text="")
image_label.grid(padx=20, pady=20)
update_image()

song_title=customtkinter.CTkLabel(master=app, text="Song Title", font=("Arial Rounded MT Bold", 30), justify="center", wraplength=300)
song_title.grid(row=1, column=0, pady= 5, columnspan=3)

song_progress = customtkinter.CTkSlider(master=app, from_=0, to=100, progress_color="#C6AEE7", button_color="#C6AEE7", button_hover_color="#827C96",  orientation="horizontal", width=300, command=progress)
song_progress.set(0)
song_progress.grid(row=2, column=1, pady=10)

time_elapsed_label=customtkinter.CTkLabel(master=app, text="00:00")
time_elapsed_label.grid(row=2, column=0, pady= 10)

time_total_label=customtkinter.CTkLabel(master=app, text="00:00")
time_total_label.grid(row=2, column=2, pady= 10)

player_frame=customtkinter.CTkFrame(master=app, width=480)
player_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="s")

sound = customtkinter.CTkSlider(master=player_frame, from_=0, to=1, progress_color="#C6AEE7", button_color="#C6AEE7", button_hover_color="#827C96", command=sound_controller, width=250)
sound.grid(row=0, column=0, columnspan=3, padx=115, pady=10)

play_button = customtkinter.CTkButton(master=player_frame, text="", image=play_img, corner_radius=30, fg_color="transparent", hover_color="#383838", width=20, height=20, command=play_music)
play_button.grid(row=1, column=1, pady=5)

prev_button = customtkinter.CTkButton(master=player_frame, text="", image=prev_img, corner_radius=30, fg_color="transparent", hover_color="#383838", width=20, height=20, command=prev_song)
prev_button.grid(row=1, column=0, pady=5, padx=10)

next_button = customtkinter.CTkButton(master=player_frame, text="", image=next_img, corner_radius=30, fg_color="transparent", hover_color="#383838", width=20, height=20, command=next_song)
next_button.grid(row=1, column=2, pady=5, padx=10)

playlist_box=CTkListbox(master=app, width=300, height=560, hover_color="#673AB7", select_color="#7E57C2", command=song_changed)
playlist_box.grid(row=0, column=3, padx=5, pady=10, sticky='e', rowspan=4)

add_song_btn=customtkinter.CTkButton(master=playlist_box, text="+ Add Song", hover_color="#673AB7", fg_color="#7E57C2", command=add_song)
add_song_btn.grid(row=0, column=0, pady=10, padx=2)

del_song_btn=customtkinter.CTkButton(master=playlist_box, text="- Delete Song", hover_color="#673AB7", fg_color="#7E57C2", command=del_song)
del_song_btn.grid(row=0, column=1, pady=10, padx=2)

app.mainloop()
