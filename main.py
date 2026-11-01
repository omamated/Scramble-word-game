import random
import nltk
import customtkinter
from PyDictionary import PyDictionary
dictionary=PyDictionary()
from nltk.corpus import words
from wordfreq import zipf_frequency

#print(random_word)
Wins=0
Loss=0
Hints=0
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.gui("starting")

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def downloaddicteasy(self):
        labeliniteasy = customtkinter.CTkLabel(self, text="Loading...", fg_color="transparent")
        labeliniteasy.pack(padx=20,pady=20)
        nltk.download('words')
        self.word_list= words.words()
        self.word_list=[
            word.lower() for word in self.word_list
            if word.isalpha()
            and 3<= len(word) <=7
            and zipf_frequency(word.lower(), "en") >=4
        ]
        self.word_list = list(set(self.word_list))
        labeliniteasy.configure(text="Loading Complete!")
        labeliniteasy.pack(padx=20,pady=20)
        self.gui("game")
    def downloaddictnormal(self):
        labelinit = customtkinter.CTkLabel(self, text="Loading...", fg_color="transparent")
        labelinit.pack(padx=20,pady=20)
        nltk.download("words")
        self.word_list = words.words()
        self.word_list = [
            word.lower() for word in self.word_list
            if word.isalpha()
            and 3<= len(word) <=10
            and zipf_frequency(word.lower(), "en") >=3
        ]
        self.word_list = list(set(self.word_list))
        labelinit.configure(text="Loading Complete!")
        labelinit.pack(padx=20,pady=20)
        self.gui("game")
    def downloaddicthard(self):
        labelinithard = customtkinter.CTkLabel(self, text="Loading...",fg_color="transparent")
        labelinithard.pack(padx=20,pady=20)
        nltk.download("words")
        self.word_list = words.words()
        self.word_list = [
            word.lower() for word in self.word_list
            if word.isalpha()
            and 5<= len(word)<=15
            and zipf_frequency(word.lower(),"en")>=2
        ]
        self.word_list = list(set(self.word_list))
        labelinithard.configure(text="Loading Complete!")
        labelinithard.pack(padx=20,pady=20)
        self.gui("game")
    def submit(self):
        self.useranswer=self.answerentry.get().lower()
        if self.useranswer != self.random_word:
            self.labelword.configure(text=f"TRY AGAIN!!! {self.scrambledword}")
        if self.useranswer == self.random_word:
            global Wins
            Wins = Wins+1
            self.labelgood = customtkinter.CTkLabel(self, text="Nice!!!!", fg_color="transparent")
            self.clear_window()
            self.gameloop()
            self.labelword.configure(text=f"Nice work, NEXT ONE!!! {self.scrambledword}")
    def definition(self):
        global Hints
        Hints=Hints+1
        define=dictionary.meaning(self.random_word)
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
    def reveal(self):
        global Loss
        Loss=Loss+1
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
        self.labelword = customtkinter.CTkLabel(self, text=f"The letters to unscramble are ... {self.scrambledword}", fg_color="transparent")
        self.labelword.pack(padx=20, pady=20)
        self.answerentry =  customtkinter.CTkEntry(self, placeholder_text="Answer Here!!!")
        self.answerentry.pack(padx=20,pady=20)

        self.buttonsubmit = customtkinter.CTkButton(self, text="Submit Answer", command=self.submit)
        self.buttonsubmit.pack(padx=20,pady=20)
        self.buttondefinitionhint = customtkinter.CTkButton(self, text="Definition Hint", command=self.definition)
        self.buttondefinitionhint.pack(padx=20,pady=20)
        self.buttonreveal = customtkinter.CTkButton(self, text="Reveal Answer", command=self.reveal)
        self.buttonreveal.pack(padx=20,pady=20)
        self.labelscore = customtkinter.CTkLabel(self, text=f"Your Score\n Correct:{Wins}\n Skipped:{Loss}")
        self.labelscore.pack(padx=20,pady=20)
    def gui(self, s):
        
        if s=="starting":
            self.title("Scramble Word Game")
            self.geometry("400x600")
            self.buttoniniteasy = customtkinter.CTkButton(self, text="Easy Mode", command=self.downloaddicteasy)
            self.buttoniniteasy.pack(padx=20, pady=20)

            self.buttoninit = customtkinter.CTkButton(self, text="Normal Mode", command=self.downloaddictnormal)
            self.buttoninit.pack(padx=20, pady=20)
            self.buttoninithard = customtkinter.CTkButton(self, text="Hard Mode", command=self.downloaddicthard)
            self.buttoninithard.pack(padx=20,pady=20)

        if s=="game":
            self.clear_window()
            self.title("Scramble Word Game")
            self.geometry("400x600")


            self.gameloop()


if __name__ == "__main__":
    app=App()
    app.mainloop()