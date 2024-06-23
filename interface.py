from tkinter import *
from tkinter import Tk
from tkinter import StringVar
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkcalendar import Calendar
from tkcalendar import DateEntry
from PIL import Image
from PIL import ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 
from datetime import date
global tree
from manipulationDB import *


################# cores ###############
co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"  # letra
co5 = "#e06636"   
co6 = "#038cfc"  
co7 = "#3fbfb9"  
co8 = "#263238"  
co9 = "#e9edf5"   
colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

################# criando window ###############
window = Tk ()
window.title ("")
window.geometry('900x650')
window.configure(background=co9)
window.resizable(width=FALSE, height=FALSE)

style = ttk.Style(window)
style.theme_use("clam")
style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 9)) # Modify the font of the body


################# Frames ####################
frameUp = Frame(window, width=1043, height=50, bg=co1,  relief="flat",)
frameUp.grid(row=0, column=0)

frameMiddle = Frame(window,width=1043, height=361,bg=co1, pady=20, relief="raised")
frameMiddle.grid(row=1, column=0,pady=1, padx=0, sticky=NSEW)

frameDown = Frame(window,width=1043, height=300,bg=co1, relief="flat")
frameDown.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

frame_gra_2 = Frame(frameMiddle, width=580, height=250,bg=co2)
frame_gra_2.place(x=415, y=5)


# abrindo imagem
app_img  = Image.open('/Users/mabds/Desktop/Portfolio/expense-control/images/money.png')
app_img = app_img.resize((45, 45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameUp, image=app_img, text="Orçamento pessoal", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'),bg=co1, fg=co4)
app_logo.place(x=0, y=0)

# ------------- Insert categories in database table Category
def insert_category_form():
    name = e_category.get()

    list_insert = [name]

    # Check that all fields have been filled in
    for idx in list_insert:
        if idx == "":
            messagebox.showerror("Error", "Enter all the necessary fields. ")
            return insert_category_form
        
    # Call function to insert data into the database
    insert_category(list_insert)
    messagebox.showinfo("Sucess","Data entered. ")

    e_category.delete(0, "end")
    categories_func = view_category()
    category = []

    for idx in categories_func:
        category.append(idx[1])

    expense_category_combo['values'] = (category)

# ------------- Insert revenues in database table Revenue
def insert_revenue_form():
    name = "REVENUE"
    date = e_date_revenue.get()
    value = e_value_revenue.get()

    list_insert = [date,value,name]
    # Check that all fields have been filled in
    for idx in list_insert:
        if idx == "":
            messagebox.showerror("Error", "Enter all the necessary fields. ")
            return insert_revenue_form
    
    insert_revenue(list_insert)
    messagebox.showinfo("Sucess","Data entered. ")

    e_date_revenue.delete(0, "end")
    e_value_revenue.delete(0, "end")

    show_revenue()

    graph_bar()

    percentage()

    graph_pie()

    resume()

# ------------- Insert expenses in database table Expenses
def insert_expenses_form():
    name = expense_category_combo.get()
    date = e_date_expenses.get()
    value = e_value_expenses.get()

    list_insert = [date,value,name]
    # Check that all fields have been filled in
    for idx in list_insert:
        if idx == "":
            messagebox.showerror("Error", "Enter all the necessary fields. ")
            return insert_expenses_form
    
    insert_expense(list_insert)
    messagebox.showinfo("Sucess","Data entered. ")

    expense_category_combo.delete(0, "end")
    e_date_expenses.delete(0, "end")
    e_value_expenses.delete(0, "end")

    show_revenue()

    graph_bar()

    percentage()

    graph_pie()

    resume()

# ------------- Delete
def delete_form():
    try:
        treev_data = tree.focus()
        treev_dictionary = tree.item(treev_data)
        treev_list = treev_dictionary['values']
        value = treev_list[0]
        name = treev_list[1]
        
        if name == "Revenue":
            delete_revenue([value])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')

            show_revenue()

            graph_bar()

            percentage()

            graph_pie()

            resume()
        else:
            delete_expense([value])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')

            show_revenue()

            graph_bar()

            percentage()

            graph_pie()

            resume()
            

    except IndexError:
        messagebox.showerror('Erro', 'Seleciona um dos dados na tabela')
# ------------- percentage

def percentage():
    l_name = Label(frameMiddle, text="Percentage of revenue spent", height=1,anchor=NW, font=('Verdana 12 bold'), bg=co1, fg=co4)
    l_name.place(x=7, y=5)


    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='#daed6b')
    style.configure("TProgressbar", thickness=25)

    bar = Progressbar(frameMiddle, length=180,style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = percentage_value()[0]

    valor = percentage_value()[0]
    l_percentage = Label(frameMiddle, text='{:,.2f} %'.format(valor),anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_percentage.place(x=200, y=35)

# Função para mostrar o gráfico de barras

def graph_bar():
    list_categories = ["Revenue", "Expenses", "Balance"]
    list_values = bar_values()

    figura = plt.Figure(figsize=(5, 4), dpi=60)
    ax = figura.add_subplot(111)
    ax.bar(list_categories, list_values, color=colors, width=0.9)

    # create a list to collect the plt.patches data
    c = 0

    # set individual bar lables using above list
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(list_values[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom',color='dimgrey')

        c += 1


    ax.set_xticklabels(list_categories,fontsize=16)
    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMiddle)
    canva.get_tk_widget().place(x=10, y=70)


# ------- resume

def resume():
    value = bar_values()

    #l_row = Label(frameMiddle, text="", width=215, height=1,anchor=NW, font=('arial 1 '), bg='#545454',)
    #l_row.place(x=309, y=52)
    l_summary = Label(frameMiddle, text="Total Monthly Income".upper(), height=1,anchor=NW, font=('Verdana 12 bold'), bg=co1, fg='#83a9e6')
    l_summary.place(x=290, y=35)
    l_summary = Label(frameMiddle, text='R$ {:,.2f}'.format(value[0]), height=1,anchor=NW, font=('Verdana 12'), bg=co1, fg='#545454')
    l_summary.place(x=290, y=70)

    #l_row = Label(frameMiddle, text="", width=215, height=1,anchor=NW, font=('arial 1 '), bg='#545454',)
    #l_row.place(x=309, y=132)
    l_summary = Label(frameMiddle, text="Total Monthly Expenses".upper(), height=1,anchor=NW, font=('Verdana 12 bold'), bg=co1, fg='#83a9e6')
    l_summary.place(x=290, y=115)
    l_summary = Label(frameMiddle, text='R$ {:,.2f}'.format(value[1]), height=1,anchor=NW, font=('Verdana 12'), bg=co1, fg='#545454')
    l_summary.place(x=290, y=150)

    #l_row = Label(frameMiddle, text="", width=215, height=1,anchor=NW, font=('arial 1 '), bg='#545454')
    #l_row.place(x=309, y=207)
    l_summary = Label(frameMiddle, text="Total Cash Balance".upper(), height=1,anchor=NW, font=('Verdana 12 bold'), bg=co1, fg='#83a9e6')
    l_summary.place(x=290, y=190)
    l_summary = Label(frameMiddle, text='R$ {:,.2f}'.format(value[2]), height=1,anchor=NW, font=('Verdana 12'), bg=co1, fg='#545454')
    l_summary.place(x=290, y=220)

# ------- graph pie

def graph_pie():
    # make figure and assign axis objects
    figure = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figure.add_subplot(111)
    list_values = pie_values()[1]
    list_categories =pie_values()[0]

    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = []
    for i in list_categories:
        explode.append(0.05)
    ax.pie(list_values, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(list_categories, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoryl_n_category = FigureCanvasTkAgg(figure, frame_gra_2)
    canva_categoryl_n_category.get_tk_widget().grid(row=0,column=0)

# ------------- create frames for tables -------------------------
frame_revenue = Frame(frameDown, width=300, height=250,bg=co1)
frame_revenue.grid(row=0,column=0)

frame_operations = Frame(frameDown, width=220, height=250,bg=co1)
frame_operations.grid(row=0,column=1, padx=5)

frame_configuration = Frame(frameDown, width=220, height=250,bg=co1)
frame_configuration.grid(row=0,column=2, padx=5)


# Monthly income table -------------------------
l_income = Label(frameMiddle, text="Revenue and Expenses table", height=1,anchor=NW, font=('Verdana 12 bold'), bg=co1, fg=co4)
l_income.place(x=5, y=320)

# ----- show revenue
def show_revenue():
    global tree
    # creating a treeview with dual scrollbars
    table_head = ['#Id','Date','Quantity','Category']

    list_items = table()
    tree = ttk.Treeview(frame_revenue, selectmode="extended",columns=table_head, show="headings")
    # vertical scrollbar
    vsb = ttk.Scrollbar(frame_revenue, orient="vertical", command=tree.yview)

    # horizontal scrollbar
    hsb = ttk.Scrollbar(frame_revenue, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in table_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])

        n+=1

    for item in list_items:
        tree.insert('', 'end', values=item)

# Configuracoes Despesas -----------------------------------
l_description = Label(frame_operations, text="New expenses", height=1,anchor=NW,relief="flat", font=('Verdana 10 bold'), bg=co1, fg=co4)
l_description.place(x=10, y=10)

l_description = Label(frame_operations, text="Category", height=1,anchor=NW,relief="flat", font=('Ivy 10'), bg=co1, fg=co4)
l_description.place(x=10, y=40)

# Pegando os categories
categories_func = view_category()
categories = []

for i in categories_func:
    categories.append(i[1])

expense_category_combo = ttk.Combobox(frame_operations, width=10,font=('Ivy 10'))
expense_category_combo['values'] = (categories)
expense_category_combo.place(x=110, y=41)

l_date_expenses = Label(frame_operations, text="Date", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_date_expenses.place(x=10, y=70)

e_date_expenses = DateEntry(frame_operations, width=12, background='darkblue', foreground='white', borderwidth=2, year=2020)
e_date_expenses.place(x=110, y=71)

l_value_expenses = Label(frame_operations, text="Quantia Total", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_value_expenses.place(x=10, y=100)
e_value_expenses = Entry(frame_operations, width=14, justify='left',relief="solid")
e_value_expenses.place(x=110, y=101)

# Botao Inserir
img_add_expenses  = Image.open('/Users/mabds/Desktop/Portfolio/expense-control/images/add.png')
img_add_expenses = img_add_expenses.resize((17,17))
img_add_expenses = ImageTk.PhotoImage(img_add_expenses)

button_insert_expenses = Button(frame_operations,command=insert_expenses_form,image=img_add_expenses, compound=LEFT, anchor=NW, text=" add".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
button_insert_expenses.place(x=110, y=131)


# operacao Excluir -----------------------
l_delete_action = Label(frame_operations, text="Delete action", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_delete_action.place(x=10, y=190)


# Botao Deletar
img_delete  = Image.open('/Users/mabds/Desktop/Portfolio/expense-control/images/delete.png')
img_delete = img_delete.resize((20, 20))
img_delete = ImageTk.PhotoImage(img_delete)
button_delete = Button(frame_operations,command=delete_form, image=img_delete, compound=LEFT, anchor=NW, text=" Delete".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
button_delete.place(x=110, y=190)

# Configuracoes Receitas -----------------------------------

l_description = Label(frame_configuration, text="New revenue", height=1,anchor=NW,relief="flat", font=('Verdana 10 bold'), bg=co1, fg=co4)
l_description.place(x=10, y=10)

l_date_revenue = Label(frame_configuration, text="Date", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_date_revenue.place(x=10, y=40)
e_date_revenue = DateEntry(frame_configuration, width=12, background='darkblue', foreground='white', borderwidth=2, year=2020)
e_date_revenue.place(x=110, y=41)

l_value_revenue = Label(frame_configuration, text="Amount", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_value_revenue.place(x=10, y=70)
e_value_revenue = Entry(frame_configuration, width=14, justify='left',relief="solid")
e_value_revenue.place(x=110, y=71)

# Botao Inserir
img_add_revenue  = Image.open('/Users/mabds/Desktop/Portfolio/expense-control/images/add.png')
img_add_revenue = img_add_revenue.resize((17,17))
img_add_revenue = ImageTk.PhotoImage(img_add_revenue)
botao_insert_revenue = Button(frame_configuration,command=insert_revenue_form, image=img_add_revenue, compound=LEFT, anchor=NW, text=" add".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
botao_insert_revenue.place(x=110, y=111)


# operacao Nova Categoria -----------------------

l_delete_action = Label(frame_configuration, text="Category", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_delete_action.place(x=10, y=160)
e_category = Entry(frame_configuration, width=14, justify='left',relief="solid")
e_category.place(x=110, y=160)

# Botao Inserir
img_add_category  = Image.open('/Users/mabds/Desktop/Portfolio/expense-control/images/add.png')
img_add_category = img_add_category.resize((17,17))
img_add_category = ImageTk.PhotoImage(img_add_category)
botao_insert_category = Button(frame_configuration,command=insert_category_form,image=img_add_category, compound=LEFT, anchor=NW, text=" add".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
botao_insert_category.place(x=110, y=190)
