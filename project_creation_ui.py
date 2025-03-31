from tkinter import Tk, Button, Label, Entry, messagebox, Listbox, END, Scrollbar, StringVar, Radiobutton, IntVar, TclError
from tkcalendar import Calendar
from datetime import date, datetime
import pandas
import os

# Creating initial window

window = Tk()
window.title("Gestor de Proyectos")
window.config(padx=50, pady=50)
window.minsize(width=100, height=100)

if not os.path.exists('existing_clients.csv'):
    # Creating mock clients
    MOCK_CLIENTS={"Nombre" : ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"],
                  "Razon" : ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"],
                  }
    MOCK_CLIENT_DATAFRAME = pandas.DataFrame(MOCK_CLIENTS)
    MOCK_CLIENT_DATAFRAME.to_csv('existing_clients.csv', index=False)

if not os.path.exists('existing_renderists.csv'):
    # Creating mock renderists
    MOCK_RENDERISTS={"Nombre" : ["Renderist 1", "Renderist 2", "Renderist 3"]}
    MOCK_RENDERISTS_DATAFRAME = pandas.DataFrame(MOCK_RENDERISTS)
    MOCK_RENDERISTS_DATAFRAME.to_csv('existing_renderists.csv', index=False)

if not os.path.exists('existing_projects.csv'):
    # Creating mock proyects
    MOCK_PROJECTS={"Nombre" : ["Projecto 1", "Projecto 2"],
                   "Cliente" : ["C1", "C2"],
                   "Concepto": ["Render cocina", "Render completo"],
                   "Total": [10000, 8000],
                   "Porcentaje anticipo": [30, 40],
                   "Monto Anticipo": [3000, 3200],
                   "Renderista": ["Renderist 1", "Renderist 2"],
                   "Porcentaje Comision": [30, 30],
                   "Comision Anticipo": [900, 320],
                   "Anticipo abonado": ["Sí", "No"],
                   "Fecha abono" : ["03/05/25", None]}
    MOCK_PROJECTS_DATAFRAME = pandas.DataFrame(MOCK_PROJECTS)
    MOCK_PROJECTS_DATAFRAME.to_csv('existing_projects.csv', index=False)


# Functions

def destroy_view():
    for widget in window.winfo_children():
        widget.destroy()

def push_new_client_to_csv(new_client_dict):
    new_client_dataframe = pandas.DataFrame(new_client_dict)
    existing_clients_dataframe = pandas.read_csv('existing_clients.csv')
    updated_projects = pandas.concat([existing_clients_dataframe, new_client_dataframe], ignore_index=True)
    updated_projects.to_csv('existing_clients.csv', index=False)

    messagebox.showinfo(title="Éxito", message="Datos del cliente guardados con éxito")

def push_new_data_to_csv(new_data_dict):

    new_project_dataframe = pandas.DataFrame(new_data_dict)
    existing_projects_dataframe = pandas.read_csv('existing_projects.csv')
    updated_projects = pandas.concat([existing_projects_dataframe, new_project_dataframe], ignore_index=True)
    updated_projects.to_csv('existing_projects.csv', index=False)

    messagebox.showinfo(title="Éxito", message="Datos del proyecto guardados con éxito")
    initial_view()

def calendar_view(new_data_dict):
    destroy_view()
    window.title("Selección de fecha")

    def grab_date():
        selected_date = calendar.get_date()
        print(type(selected_date))
        date_object = datetime.strptime(selected_date, "%m/%d/%y").date()
        is_okay = messagebox.askokcancel(
            title="Revisar fecha",
            message=f"La fecha seleccionada es {date_object.strftime("%d-%b-%Y")}, esto es correcto?"
        )
        if is_okay:
            new_data_dict["Fecha abono"] = [selected_date]
            push_new_data_to_csv(new_data_dict)
        else:
            return

    calendar_selection_label = Label(text="Selecciona la fecha de abono del anticipo:")
    calendar_selection_label.grid(column=0, row=0, pady=5, sticky='w')

    today = date.today()

    calendar = Calendar(selectmode="day", year=today.year, month=today.month, day=today.day)
    calendar.grid(column=0, row=1, pady=5, sticky='w')

    select_button = Button(text="Okay", command=grab_date)
    select_button.grid(column=0, row=2, pady=5, sticky='e')

def new_project_view(client_type, client_name, client_razon_social=None):
    if client_type == "new":
        if not client_name or not client_razon_social:
            messagebox.showwarning(title="Oops", message="No dejes ningún campo vacío!")
            return
        else:
            new_client_dict = {"Nombre": [client_name],
                             "Razon": [client_razon_social],
                             }
            push_new_client_to_csv(new_client_dict)



    destroy_view()

    window.title("Nuevo Proyecto")

    window.grid_columnconfigure(1, weight=0)

    # Project name widget

    project_name_label = Label(text="Nombre del proyecto:")
    project_name_label.grid(column=0, row=0, pady=5, sticky='w')

    project_name_entry = Entry(width=30)
    project_name_entry.grid(column=1, row=0, pady=5)
    project_name_entry.focus()

    # Project concept widget

    project_concept_label = Label(text="Concepto(s):")
    project_concept_label.grid(column=0, row=1, pady=5, sticky='w')

    project_concept_entry = Entry(width=35)
    project_concept_entry.grid(column=0, row=1, sticky='e', columnspan=2, pady=5)

    # Payment type widget

    payment_type_label = Label(text="Forma de pago:")
    payment_type_label.grid(column=0, row=2, pady=5, sticky='w')

    payment_type_selection = StringVar()
    payment_type_selection.set(None)

    cash_radio_button = Radiobutton(text="Efectivo", variable=payment_type_selection, value="cash")
    cash_radio_button.grid(column=1, row=2, pady=5, sticky='w')

    card_radio_button = Radiobutton(text="Tarjeta", variable=payment_type_selection, value="card")
    card_radio_button.grid(column=1, row=2, pady=5, padx=(0,40), sticky='e')

    # Total payment widget

    total_payment_label = Label(text="Total con IVA:")
    total_payment_label.grid(column=0, row=3, pady=5, sticky='w')

    total_payment_entry = Entry(width=35)
    total_payment_entry.grid(column=0, row=3, sticky='e', columnspan=2, pady=5)
    total_payment_entry.insert(0, "$ ")

    # Pre-payment widget

    pre_payment_percentage_label = Label(text="Anticipo:")
    pre_payment_percentage_label.grid(column=0, row=4, pady=5, sticky='w')

    pre_payment_percentage_entry = Entry(width=35)
    pre_payment_percentage_entry.grid(column=0, row=4, sticky='e', columnspan=2, pady=5)
    pre_payment_percentage_entry.insert(0, "% ")

    # Payment calculation button

    def calculate_pre_payment_amount(calculate_button_clicked="no"):

        raw_total_payment = total_payment_entry.get()
        total_payment = ""
        for char in raw_total_payment:
            if char.isdigit():
                total_payment += char

        raw_payment_percentage = pre_payment_percentage_entry.get()
        percentage = ""
        for char in raw_payment_percentage:
            if char.isdigit():
                percentage += char

        if percentage == "" or total_payment == "":
            messagebox.showwarning(title="Faltan cantidades",
                                message=f"No haz ingresado todos los valores, no se puede calcular el monto.")
            return None, None, None

        int_percentage = int(percentage)
        int_payment = int(total_payment)

        pre_payment_amount = (int_percentage * .01) * int_payment

        if calculate_button_clicked == "yes":
            messagebox.showinfo(title="Anticipo", message=f"Con los valores ingresados el anticipo es de ${pre_payment_amount:,}")

        return pre_payment_amount, int_payment, int_percentage

    calculate_pre_payment_amount_button = Button(text="Calcular anticipo", width=10, command=lambda: calculate_pre_payment_amount (calculate_button_clicked="yes"))
    calculate_pre_payment_amount_button.grid(column=2, row=4, pady=5, padx=(20,0), sticky='w')

    # Renderist widget

    renderist_label = Label(text="Renderista:")
    renderist_label.grid(column=0, row=5, pady=5, sticky='w')

    renderist_dataframe = pandas.read_csv("existing_renderists.csv")
    renderist_name_list = renderist_dataframe["Nombre"].to_list()

    renderist_scrollbar = Scrollbar()
    renderist_scrollbar.grid(column=2, row=5, pady=5, sticky="nsw")

    renderist_list_box = Listbox(height=2, yscrollcommand=renderist_scrollbar.set, selectmode='single')
    renderist_list_box.grid(column=1, row=5, pady=5, sticky='nsew')

    renderist_scrollbar.config(command=renderist_list_box.yview)

    for renderist_name in renderist_name_list:
        renderist_list_box.insert(END, renderist_name)

    # Commission widget

    commission_label = Label(text="Comisión:")
    commission_label.grid(column=0, row=6, pady=5, sticky='w')

    commission_value_selection = IntVar()
    commission_value_selection.set(None)

    ten_radio_button = Radiobutton(text="10%", variable=commission_value_selection, value=10)
    ten_radio_button.grid(column=0, row=6, pady=5, padx=(100,0), sticky='w', columnspan=2)

    twenty_radio_button = Radiobutton(text="20%", variable=commission_value_selection, value=20)
    twenty_radio_button.grid(column=1, row=6, pady=5, padx=(0,160), sticky='e')

    thirty_radio_button = Radiobutton(text="30%", variable=commission_value_selection, value=30)
    thirty_radio_button.grid(column=1, row=6, pady=5, padx=(0,100), sticky='e')

    forty_radio_button = Radiobutton(text="40%", variable=commission_value_selection, value=40)
    forty_radio_button.grid(column=1, row=6, pady=5, padx=(0,40), sticky='e')

    fifty_radio_button = Radiobutton(text="50%", variable=commission_value_selection, value=50)
    fifty_radio_button.grid(column=1, row=6, pady=5, padx=(0,170), sticky='e', columnspan=2)

    # Calculate Commission button

    def calculate_commission_amount(calculate_button_clicked="no"):
        try:
            commission_percentage = commission_value_selection.get()
        except TclError:
            messagebox.showwarning(title="Falta selección",
                                   message=f"No haz seleccionado un porcentage de comisión.")
        else:

            try:
                pre_payment_amount, total, percentage = calculate_pre_payment_amount()
            except TypeError as e:
                print(e)
            else:
                commission_amount = (commission_percentage * .01) * pre_payment_amount

                if calculate_button_clicked == "yes":
                    messagebox.showinfo(title="Comisión", message=f"Con los valores ingresados la comisión es de ${commission_amount:,}")

                return commission_amount

    calculate_commission_amount_button = Button(text="Calcular comisión", width=15, command=lambda: calculate_commission_amount(calculate_button_clicked="yes"))
    calculate_commission_amount_button.grid(column=2, row=6, pady=5, padx=(40,0), sticky='w')

    # Pre_payment paid widget

    pre_payment_paid_label = Label(text="Anticipo abonado:")
    pre_payment_paid_label.grid(column=0, row=7, pady=5, sticky='w')

    pre_payment_paid_value_selection = StringVar()
    pre_payment_paid_value_selection.set(None)

    pre_payment_yes_radio_button = Radiobutton(text="Sí", variable=pre_payment_paid_value_selection, value="Sí")
    pre_payment_yes_radio_button.grid(column=1, row=7, pady=5, padx=(0,0), sticky='w')

    pre_payment_no_radio_button = Radiobutton(text="No", variable=pre_payment_paid_value_selection, value="No")
    pre_payment_no_radio_button.grid(column=1, row=7, pady=5, padx=(50,0), sticky='w')

    def check_responses():
        project_name = project_name_entry.get()
        project_concept = project_concept_entry.get()
        pre_payment_amount, total_payment, pre_payment_percentage = calculate_pre_payment_amount()
        selected_indices = renderist_list_box.curselection()
        commission_percentage = commission_value_selection.get()
        is_pre_payment_paid = pre_payment_paid_value_selection.get()

        if project_name == "" or project_concept == "" or payment_type_selection is None or pre_payment_amount is None or len(selected_indices) == 0 or commission_percentage is None or is_pre_payment_paid is None:
            messagebox.showwarning(title="Falta selección", message=f"Asegurate de llenar todos los campos.")
        else:
            renderist = renderist_name_list[selected_indices[0]]
            commission_amount = calculate_commission_amount()
            is_okay = messagebox.askokcancel(
                title="Revisar datos",
                message=f"Estos son los datos del proyecto, asegurate que son correctos:\n\n"
                                                               f"Nombre del proyecto: {project_name}\n"
                                                               f"Concepto(s) del proyecto: {project_concept}\n"
                                                               f"Total con IVA: ${total_payment:,}\n"
                                                               f"Porcentaje de Anticipo: {pre_payment_percentage}%\n"
                                                               f"Monto de Anticipo: ${pre_payment_amount:,}\n"
                                                               f"Renderista: {renderist}\n"
                                                               f"Porcentaje de comisión: {commission_percentage}%\n"
                                                               f"Comisión anticipo: ${commission_amount:,}\n"
                                                               f"Anticipo abonado: {is_pre_payment_paid}"
            )
            if is_okay:
                new_data_dict = {"Nombre": [project_name],
                                 "Concepto": [project_concept],
                                 "Cliente": [client_name],
                                 "Total": [total_payment],
                                 "Porcentaje anticipo": [pre_payment_percentage],
                                 "Monto Anticipo": [pre_payment_amount],
                                 "Renderista": [renderist],
                                 "Porcentaje Comision": [commission_percentage],
                                 "Comision Anticipo": [commission_amount],
                                 "Anticipo abonado": [is_pre_payment_paid],
                                 }
                if is_pre_payment_paid == "Sí":
                    calendar_view(new_data_dict)
                elif is_pre_payment_paid == "No":
                    new_data_dict["Fecha abono"] = [None]
                    push_new_data_to_csv(new_data_dict)
            else:
                return


    ok_button = Button(text="Okay", width=4,
                       command=check_responses)
    ok_button.grid(column=0, row=10, columnspan=2, pady=5)

def show_existing_client_list():
    try:
        dataframe = pandas.read_csv("existing_clients.csv")
    except FileNotFoundError as e:
        filename = e.filename
        messagebox.showerror(title="Oops", message=f"La base de datos {filename} no existe.")
        show_new_client_view()
    else:
        window.title("Clientes existentes")

        client_name_list = dataframe["Nombre"].to_list()

        select_client_label = Label(text="Selecciona un cliente:")
        select_client_label.grid(column=0, row=0, pady=5)

        scrollbar = Scrollbar()
        scrollbar.grid(column=1, row=1, pady=5, sticky="ns")

        client_list_box = Listbox(height=4, yscrollcommand = scrollbar.set, selectmode='single')
        client_list_box.grid(column=0, row=1, pady=5, sticky='nsew')

        scrollbar.config(command=client_list_box.yview)

        for client_name in client_name_list:
            client_list_box.insert(END, client_name)

        def get_client_name():
            selected_indices = client_list_box.curselection()
            if selected_indices:
                selected_client_name = client_name_list[selected_indices[0]]
                selected_client_razon = dataframe.loc[selected_indices[0], "Razon"]
                new_project_view(client_type="old", client_name=selected_client_name, client_razon_social=selected_client_razon)
            else:
                messagebox.showwarning(title="Oops", message="No elegiste ningún cliente.")

        ok_button = Button(text="Okay", width=4,
                           command=get_client_name)
        ok_button.grid(column=0, row=2, columnspan=2, pady=5)



def show_new_client_view():
    window.title("Nuevo cliente")

    client_name_label = Label(text="Nombre del cliente:")
    client_name_label.grid(column=0, row=0, pady=5)

    client_name_entry= Entry(width=30)
    client_name_entry.grid(column=1, row=0, pady=5)

    razon_social_label = Label(text="Razón Social:")
    razon_social_label.grid(column=0, row=1, sticky='w', pady=5)

    razon_social_entry= Entry(width=35)
    razon_social_entry.grid(column=0, row=1, sticky='e', columnspan=2, pady=5)

    ok_button = Button(text="Okay", width=4, command=lambda: new_project_view(client_type="new", client_name=client_name_entry.get(), client_razon_social=razon_social_entry.get()))
    ok_button.grid(column=0, columnspan=2, pady=5)


def client_detail_view(new_client):
    destroy_view()

    if new_client == "yes":
        show_new_client_view()
    else:
        show_existing_client_list()


def client_prompt_view():
    destroy_view()

    new_client_label = Label(text="¿Es un cliente nuevo?")
    new_client_label.grid(column=0, row=0, columnspan=2)

    yes_button = Button(text="Sí", width=4, command=lambda: client_detail_view("yes"))
    yes_button.grid(column=0, row=1, pady=10)

    no_button = Button(text="No", width=4, command=lambda: client_detail_view("no"))
    no_button.grid(column=1, row=1, pady=10)

# Initial view

def initial_view():
    destroy_view()
    new_project = Button(text="Nuevo Proyecto", width=20, command=client_prompt_view)
    new_project.grid(column=0, row=0, sticky="ew")
    updated_projects = pandas.read_csv("existing_projects.csv")
    print(updated_projects)

initial_view()


window.mainloop()
