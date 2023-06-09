from psychopy import visual, event, core, sound
import random
import os
import time
from psychopy import data

# Window
win = visual.Window(size=[800, 600], fullscr=False, units="pix")

# Instructions text
instructions = visual.TextStim(win, text="Thank you for participating in this experiment!\n\nYou will hear three voice samples.\nAfter hearing all three sounds, please indicate as fast as you can which of the first two samples is closest to the third one.\n\nPress any key to start.")

# Displays the instructions and wait for key press to start
instructions.draw()
win.flip()
event.waitKeys()

# Sound directory(this is mine)
sound_dir = "C:/Users/marga/OneDrive/Bureau/Travaux_ecole/Travaux_Memoire/Corpus/stimuli"

# Sorts sound files by speaker name
sound_files_by_speaker = {}
for filename in os.listdir(sound_dir):
    if filename.endswith(".wav"):
        speaker = filename.split("_")[0]
        if speaker not in sound_files_by_speaker:
            sound_files_by_speaker[speaker] = []
        sound_files_by_speaker[speaker].append(os.path.join(sound_dir, filename))

# This will create trials for each speaker and play sound a and b in shuffle (my own sounds, use your own)
trials_list = []
for speaker, sound_files in sound_files_by_speaker.items():
    random.shuffle(sound_files)
    for i in range(0, len(sound_files), 3):
        block_sound_files = sound_files[i: i+3]
        x = [f for f in block_sound_files if f.endswith("_originel.wav")][0]
        ab = [f for f in block_sound_files if not f.endswith("_originel.wav")]
        random.shuffle(ab)
        a, b = ab
        block = {
            "A": a,
            "B": b,
            "X": x
        }
        trials_list.append(block)

# Sets the number of repetitions for each block
n_reps = 1

# The trial handler for blocks
trials = data.TrialHandler(trialList=trials_list, nReps=n_reps, method="sequential")

#File path for the results (again, my own)
results_file_path = "C:/Users/marga/OneDrive/Bureau/Travaux_ecole/Travaux_Memoire/results"

# Presents  the blocks on screen
results = []
for i, trial in enumerate(trials):
    block_num = i + 1
    block = trial
    
    # creates my sound stimuli
    sound_A = sound.Sound(block["A"])
    sound_B = sound.Sound(block["B"])
    sound_X = sound.Sound(block["X"])

    # Shuffle order of A and B
    AB_order = [sound_A, sound_B]
    random.shuffle(AB_order)

   # Play sounds A and B in shuffled order
    prompt_texts = []
    for i, sound_stim in enumerate(AB_order):
        if i == 0:
            prompt_text = visual.TextStim(win, text ="Sound A")
        elif i == 1:
            prompt_text = visual.TextStim(win, text ="Sound B")
        prompt_texts.append(prompt_text)
        sound_stim.setVolume(1)
        start_time = core.getTime()
        win.callOnFlip(sound_stim.play)
        while core.getTime() < start_time + sound_stim.getDuration():
            prompt_text.draw()
            win.flip()
        core.wait(0.5)

    # Creates and play sound X
    sound_X = sound.Sound(block["X"])
    prompt_text = visual.TextStim(win, text="Sound X")
    sound_X.setVolume(1)
    start_time = core.getTime()
    win.callOnFlip(sound_X.play)
    while core.getTime() < start_time + sound_X.getDuration():
        prompt_text.draw()
        win.flip()
    core.wait(0.5)
    

    # Displays the answer prompt
    prompt_text = visual.TextStim(win, text="Which sound was closest to X?\n\nPress s for the first sound\nPress d for the second sound")
    prompt_text.draw()
    prompt_onset = win.flip()
    
    # Collects the response choice, I used key s and d. You can also record the response time. Here the response time is 
    #recorded right after the end of the question prompt.
    keys = event.waitKeys(keyList=["s", "d"])
    rt = core.getTime() - prompt_onset
    
    # determines which sound was chosen
    if keys[0] == "s":
        chosen_sound = "A"
    else:
        chosen_sound = "B"

    # writes the result to file (this is a csv file)
    with open('results.csv', 'a') as f:
        f.write(f"{block_num},{rt},{chosen_sound}\n")

    print(f"Block {block_num}: RT={rt}, Chosen sound={chosen_sound}")
    
# Creates and present end message and waits a little 
end_message = visual.TextStim(win, text="The experiment is over.\nThank you for your participation.\n\nDon't forget your free candy.")
end_message.draw()
win.flip()
core.wait(3)

# quits
core.quit()
