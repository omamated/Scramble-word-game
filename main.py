import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

import random
import nltk
import customtkinter
from PyDictionary import PyDictionary
dictionary=PyDictionary()
from nltk.corpus import words, wordnet
from wordfreq import zipf_frequency

#print(random_word)
Wins=0
Loss=0
Hints=0
Streak=0
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.seconds=60
        self.timer_id=None

        self.gui("starting")

    def clear_window(self, s=None):
        if hasattr(self, "timer_id") and self.timer_id:
            pass
        for widget in self.winfo_children():
            if hasattr(self, "labeltimer") and widget == self.labeltimer:
                continue
            widget.destroy()
        if s == "everything":
            for widget in self.winfo_children():
                widget.destroy()

    def loading_cursor(self):
        self.configure(cursor="watch")
    def normal_cursor(self):
        self.configure(cursor="")
    def downloaddicteasy(self):
        self.clear_window()
        self.loading_label = customtkinter.CTkLabel(self, text="Loading... Please wait!")
        self.loading_label.pack(expand=True)
        self.update()
        self.loading_cursor()
        self.update_idletasks()
        nltk.download('words')
        nltk.download("wordnet")
        self.word_list= words.words()
        self.word_list=[
            word.lower() for word in self.word_list
            if word.isalpha()
            and 3<= len(word) <=7
            and zipf_frequency(word.lower(), "en") >=4
        ]
        self.word_list = list(set(self.word_list))
        self.normal_cursor()
        self.update_idletasks()
        self.gui("game")
    def downloaddictnormal(self):
        self.clear_window()
        self.loading_label = customtkinter.CTkLabel(self, text="Loading... Please wait!")
        self.loading_label.pack(expand=True)
        self.update()
        self.loading_cursor()
        self.update_idletasks()
        nltk.download("words")
        nltk.download("wordnet")
        self.word_list = words.words()
        self.word_list = [
            word.lower() for word in self.word_list
            if word.isalpha()
            and 3<= len(word) <=10
            and zipf_frequency(word.lower(), "en") >=3
        ]
        self.word_list = list(set(self.word_list))
        self.normal_cursor()
        self.update_idletasks()
        self.gui("game")
    def downloaddicthard(self):
        self.clear_window()
        self.loading_label = customtkinter.CTkLabel(self, text="Loading... Please wait!")
        self.loading_label.pack(expand=True)
        self.update()
        self.loading_cursor()
        nltk.download("words")
        nltk.download("wordnet")
        self.word_list = words.words()
        self.word_list = [
            word.lower() for word in self.word_list
            if word.isalpha()
            and 5<= len(word)<=15
            and zipf_frequency(word.lower(),"en")>=2
        ]
        self.word_list = list(set(self.word_list))
        self.normal_cursor()
        self.gui("game")
    def downloaddicttimed(self):
        self.clear_window()
        self.loading_label = customtkinter.CTkLabel(self, text="Loading... Please wait!")
        self.loading_label.pack(expand=True)
        self.update()
        self.loading_cursor()
        self.update_idletasks()
        nltk.download("words")
        nltk.download("wordnet")
        self.word_list = words.words()
        self.word_list = [
            word.lower() for word in self.word_list
            if word.isalpha()
            and 3<= len(word)<=10
            and zipf_frequency(word.lower(), "en")>=3
        ]
        self.word_list=list(set(self.word_list))
        self.normal_cursor()
        self.update_idletasks()
        self.gui("timed")
    def countdown(self):
        if hasattr(self, "labeltimer") and self.labeltimer.winfo_exists() and self.seconds >= 0:
            self.labeltimer.configure(text=f"Time Remaining: 00:{self.seconds:02d}")
            if self.seconds == 0:
                self.gui("timedstats")
                return
            self.seconds -=1
            self.timer_id = self.after(1000, self.countdown)
    def updatescore(self):
        self.labelscore.configure(text=f"Your Score\n Correct:{Wins}\n Skipped:{Loss}\nHints Used: {Hints}\n Correct Streak: {Streak}")
    def submit(self, event=None):
        self.useranswer=self.answerentry.get().lower()
        if self.useranswer != self.random_word:
            global Streak
            Streak=0
            self.updatescore()
            self.labelword.configure(text=f"TRY AGAIN!!!\n {self.scrambledword}")
            self.answerentry.delete(0, "end")
            self.answerentry.focus_set()
        if self.useranswer == self.random_word:
            global Wins
            Streak= Streak+1
            Wins = Wins+1
            self.updatescore()
            self.clear_window()
            self.gameloop()
            self.labelword.configure(text=f"Nice work, NEXT ONE!!!\n {self.scrambledword}")
            
    def getworddefinition(self, word):
        try:
            synsets = wordnet.synsets(word)
            if synsets:
                return synsets[0].definition()
        except Exception:
            pass
        return None
    def definition(self):
        self.loading_cursor()
        global Hints
        Hints=Hints+1
        self.updatescore()
        define=self.getworddefinition(self.random_word)
        if define:
            definition_text=str(define)
        else:
            definition_text="No definition available!"
        if hasattr(self, "labeldefine") and self.labeldefine.winfo_exists():
            self.labeldefine.configure(text=definition_text)
        else:
            self.labeldefine=customtkinter.CTkLabel(
                self,
                text=definition_text,
                wraplength=300
            )
            self.labeldefine.pack(padx=20,pady=20)
        self.update_idletasks()
        self.normal_cursor()

    def reveal(self):
        global Loss
        global Streak
        Streak=0
        Loss=Loss+1
        self.updatescore()
        old_answer=self.random_word
        self.clear_window()
        self.gameloop()
        self.labelreveal = customtkinter.CTkLabel(self, text=f"The Word Was {old_answer}")
        self.labelreveal.pack(padx=20,pady=20)

    def gameloop(self):
                
        self.random_word = random.choice(self.word_list).lower()
        word_letters = list(self.random_word)
        random.shuffle(word_letters)
        self.scrambledword = "".join(word_letters)

        self.labelword = customtkinter.CTkLabel(self, text=f"The letters to unscramble are ...\n {self.scrambledword}", fg_color="transparent")
        self.labelword.pack(padx=20, pady=20)
        self.answerentry =  customtkinter.CTkEntry(self, placeholder_text="Answer Here!!!")
        self.answerentry.pack(padx=20,pady=20)

        self.buttonsubmit = customtkinter.CTkButton(self, text="Submit Answer", command=self.submit)
        self.buttonsubmit.pack(padx=20,pady=20)
        self.buttondefinitionhint = customtkinter.CTkButton(self, text="Definition Hint", command=self.definition)
        self.buttondefinitionhint.pack(padx=20,pady=20)
        self.buttonreveal = customtkinter.CTkButton(self, text="Reveal Answer", command=self.reveal)
        self.buttonreveal.pack(padx=20,pady=20)
        self.labelscore = customtkinter.CTkLabel(self, text=f"Your Score\n Correct:{Wins}\n Skipped:{Loss}\nHints Used: {Hints}\n Correct Streak: {Streak}")
        self.buttonrestart=customtkinter.CTkButton(self, text="Go Back", command=lambda: self.gui("starting"))
        self.buttonrestart.pack(padx=20,pady=20)
        self.labelscore.pack(padx=20,pady=20)
        self.answerentry.focus_set()
        self.answerentry.bind("<Return>", self.submit)
        
    def gui(self, s):
        
        if s=="starting":
            self.clear_window("everything")
            self.title("Scramble Word Game")
            self.geometry("600x800")
            self.buttoniniteasy = customtkinter.CTkButton(self, text="Easy Mode", command=self.downloaddicteasy)
            self.buttoniniteasy.pack(padx=20, pady=20)

            self.buttoninit = customtkinter.CTkButton(self, text="Normal Mode", command=self.downloaddictnormal)
            self.buttoninit.pack(padx=20, pady=20)
            self.buttoninithard = customtkinter.CTkButton(self, text="Hard Mode", command=self.downloaddicthard)
            self.buttoninithard.pack(padx=20,pady=20)
            self.buttoninittimed = customtkinter.CTkButton(self, text="Timed Mode", command=self.downloaddicttimed)
            self.buttoninittimed.pack(padx=20,pady=20)
            self.labelinfo = customtkinter.CTkLabel(self, text="The modes correlate with how common the words are and their lengths\n(hard mode will have longer+rarer words)\nThe goal of the game is to unscramble a bundle of characters into a valid word\n Sometimes there can be multiple answers so you may have to use the\n definition hint to narrow it down.")
            self.labelinfo.pack(padx=20,pady=20)

        if s=="game":
            self.clear_window()
            self.title("Scramble Word Game")
            self.geometry("600x800")


            self.gameloop()
        if s=="timed":
            self.clear_window()
            self.title("Scramble Word Game")
            self.geometry("600x800")
            self.labeltimer=customtkinter.CTkLabel(self, text= "Time Remaining: 00:60")
            self.labeltimer.pack(padx=20,pady=20)
            self.seconds=60
            self.countdown()
            self.gameloop()
        if s=="timedstats":
            self.clear_window()
            self.labelscore = customtkinter.CTkLabel(self, text=f"Your Score\n Correct:{Wins}\n Skipped:{Loss}\nHints Used: {Hints}\n Correct Streak: {Streak}")
            self.labelscore.pack(padx=20,pady=20)
            self.buttonrestart=customtkinter.CTkButton(self, text="Go Back", command=lambda: self.gui("starting"))
            self.buttonrestart.pack(padx=20,pady=20)

if __name__ == "__main__":
    app=App()
    app.mainloop()

    