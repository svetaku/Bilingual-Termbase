from tkinter import *
import pickle

with open('termbase_top_3.pkl', 'rb') as f:
        unigrams3 = pickle.load(f)

root_1 = Tk()
root_1.title('Term Adder')

text_1 = Label(root_1, text = "Look up term: ")
text_1.grid(row=0, column=0)

term_for_lookup = Entry(root_1, width=40)
term_for_lookup.grid(row=1, column=0)

def submit():
    return
    
#    new_term = {}
 #   try:
  #      num = int(right_num.get())
   #     num -= 1
    #    new_term[ent.get()] = unigrams3[ent.get()][num]
     #   new_entry = Label(root_1, text='The new entry is ' + new_term)
      #  new_entry.grid(row=5, column=0)
    #except:
     #   error3 = Label(root_1, text = 'Incorrect number')
      #  error3.grid(row=5, column=0)

def lookup(term_for_lookup):
    try:
        options = Label(root_1, text = unigrams3[term_for_lookup])
        options.grid(row=2, column=0)
        try:
            whichOne = Label(root_1, text='Which one is the correct one? Enter 1, 2 or 3.')
            whichOne.grid(row=3, column=0)
            right_num = Entry(root_1, width=40)
            right_num.grid(row=4, column=0)
            button_submit_2 = Button(root_1, text='Submit', padx=15, command=submit)
            button_submit_2.grid(row=4, column=1)
        except:
            error2 = Label(root_1, text='Wrong input')
            error2.grid(row=5, column=0)
    except:
        error1 = Label(root_1, text='No such term')
        error1.grid(row=2, column=0)
    

button_submit_1 = Button(root_1, text='Submit', padx=15, command=lambda: lookup(term_for_lookup.get())
button_submit_1.grid(row=1, column=1)




root_1.mainloop()

