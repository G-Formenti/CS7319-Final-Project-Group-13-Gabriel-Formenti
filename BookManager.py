import psycopg2
from tkinter import *
from psycopg2 import sql
from tkinter import messagebox

class BookManagerApp:
    def __init__(self, root):
        self.root = root
        root.geometry("650x500")

        self.conn = psycopg2.connect(
            host="localhost",
            database="Books",
            user="postgres",
            password="postgres1",
            port="5432"
        )
        # Create the frames
        self.Insert_Frame = LabelFrame(root, text="Insert Book")
        self.Current_Frame = LabelFrame(root,
                                        text="Current Reading List")
        self.Update_Frame = LabelFrame(root, text="Update")
        self.Insights_Frame = LabelFrame(root, text="Insights")
        self.Delete_Frame = LabelFrame(root, text="Delete")

        # Create navigation buttons
        self.Insert_Switch = Button(root, text="Insert Book",
                                    command=self.Change_to_Insert)
        self.Insert_Switch.pack(side=TOP)

        self.Current_Switch = Button(root, text="Book List",
                                     command=self.on_Book_List_Press)
        self.Current_Switch.pack(side=TOP)

        self.Update_Switch = Button(root, text="Update",
                                    command=self.Change_to_Update)
        self.Update_Switch.pack(side=TOP)

        self.Insights_Switch = Button(root, text="Insights",
                                      command=self.on_Insights_Press)
        self.Insights_Switch.pack(side=TOP)

        self.Delete_Switch = Button(root, text="Delete",
                                      command=self.Change_to_Delete)
        self.Delete_Switch.pack(side=TOP)

        self.Books_Output_label = Label(self.Current_Frame, text="")
        self.Books_Output_label.pack(pady=50)

        self.Insights_Output_label = Label(self.Insights_Frame, text="")
        self.Insights_Output_label.pack(pady=50)

        self.CreateGui()

    def Change_to_Current(self):
        self.Current_Frame.pack(fill='both', expand=1)
        self.Insert_Frame.pack_forget()
        self.Update_Frame.pack_forget()
        self.Insights_Frame.pack_forget()
        self.Delete_Frame.pack_forget()

    def Change_to_Insert(self):
        self.Insert_Frame.pack(fill='both', expand=1)
        self.Current_Frame.pack_forget()
        self.Update_Frame.pack_forget()
        self.Insights_Frame.pack_forget()
        self.Delete_Frame.pack_forget()

    def Change_to_Update(self):
        self.Update_Frame.pack(fill='both', expand=1)
        self.Current_Frame.pack_forget()
        self.Insights_Frame.pack_forget()
        self.Insert_Frame.pack_forget()
        self.Delete_Frame.pack_forget()

    def Change_to_Insights(self):
        self.Insights_Frame.pack(fill='both', expand=1)
        self.Current_Frame.pack_forget()
        self.Insert_Frame.pack_forget()
        self.Update_Frame.pack_forget()
        self.Delete_Frame.pack_forget()

    def Change_to_Delete(self):
        self.Delete_Frame.pack(fill='both', expand=1)
        self.Current_Frame.pack_forget()
        self.Insert_Frame.pack_forget()
        self.Update_Frame.pack_forget()
        self.Insights_Frame.pack_forget()

    def on_Book_List_Press(self):
        self.Change_to_Current()
        self.update_Book_List()

    def on_Insights_Press(self):
        self.Change_to_Insights()
        self.update_Insights()

    def ErrorMsg(self, message):
        messagebox.showerror("Error", message)

    def SuccessMsg(self, message):
        messagebox.showinfo("Success", message)

    def run(self):
        self.root.mainloop()


class SQL_Commands(BookManagerApp):
    #Good
    def clear(self):
        self.BT_name.delete(0, END)
        self.AU_name.delete(0, END)
        self.PR_name.delete(0, END)
        self.TP_name.delete(0, END)
        self.DI_name.delete(0, END)
        self.Update_BT_name.delete(0, END)
        self.Update_AU_name.delete(0, END)
        self.Update_PR_name.delete(0, END)
        self.Delete_BT_name.delete(0, END)
        self.Delete_AU_name.delete(0, END)

    #Good
    def update(self):
        cur = self.conn.cursor()

        Book_Title = self.Update_BT_name.get()
        Authors = self.Update_AU_name.get()
        Read = self.Update_PR_name.get()

        SQL = '''UPDATE Books SET Pages_Read = %s WHERE 
            Book_Title = %s AND Author = %s'''

        try:
            cur.execute(SQL, (Read, Book_Title, Authors))
            RowCount = cur.rowcount
            if RowCount == 0:
                self.ErrorMsg("Error Book Not Found")
            else:
                self.SuccessMsg("Update Successful")
            self.conn.commit()
            cur.close()

        except Exception as e:
            self.conn.close()
            cur.close()
            self.ErrorMsg(e)
            self.conn = psycopg2.connect(
                host="localhost",
                database="Books",
                user="postgres",
                password="postgres1",
                port="5432"
            )
        self.clear()

    #Good
    def insert(self):
        cur = self.conn.cursor()

        Book_Title = self.BT_name.get()
        Authors = self.AU_name.get()
        Read = self.PR_name.get()
        Total = self.TP_name.get()
        Date = self.DI_name.get()

        try:
            cur.execute('''INSERT INTO Books (Book_Title, Author, Pages_Read, 
                 Pages_Book, Date_Inserted) VALUES (%s, %s, %s, %s, %s) ''',
                    (Book_Title, Authors, Read, Total, Date))
            RowCount = cur.rowcount
            if RowCount == 0:
                self.ErrorMsg("Row Was Not Inserted")
            else:
                self.SuccessMsg("Update Successful")
            self.conn.commit()
            cur.close()

        except Exception as e:
            self.conn.close()
            cur.close()
            self.ErrorMsg(e)
            self.conn = psycopg2.connect(
                host="localhost",
                database="Books",
                user="postgres",
                password="postgres1",
                port="5432"
            )
        self.clear()

    def delete_Book(self):
        cur = self.conn.cursor()

        Title = self.Delete_BT_name.get()
        Authors = self.Delete_AU_name.get()
        delete_query = sql.SQL('DELETE FROM Books WHERE Book_Title = {} AND Author = {}').format(
            sql.Literal(Title),
            sql.Literal(Authors))

        try:
            cur.execute(delete_query)
            RowCount = cur.rowcount
            if RowCount == 0:
                self.ErrorMsg("Error Book Not Found")
            else:
                self.SuccessMsg("Update Successful")
            self.conn.commit()
            cur.close()

        except Exception as e:
            self.conn.close()
            cur.close()
            self.ErrorMsg(e)
            self.conn = psycopg2.connect(
                host="localhost",
                database="Books",
                user="postgres",
                password="postgres1",
                port="5432"
            )
        self.clear()

    def update_Book_List(self):
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT * FROM Books")
            Books_Rows = cur.fetchall()
            Books_Output = ''
            header_label = Label(self.Current_Frame,
                             text="Book Title | Author | Pages Read | Pages in Book | Date Inserted | Progress Percentage ")
            for Books in Books_Rows:
                Books_Output += f'\n {Books[0]} | {Books[1]} | {Books[2]} | {Books[3]} | {Books[4]} | {Books[5]}'

            self.Books_Output_label.config(text=header_label['text'] +
                                            Books_Output,
                                       font=('Helvetica bold', 12))
            cur.close()

        except Exception as e:
            self.conn.close()
            cur.close()
            self.ErrorMsg(e)
            self.conn = psycopg2.connect(
                host="localhost",
                database="Books",
                user="postgres",
                password="postgres1",
                port="5432"
            )

    def update_Insights(self):
        cur = self.conn.cursor()
        cur.execute("SELECT SUM(Pages_Read) FROM Books")
        Total_Pages = cur.fetchall()
        Pages = ''
        header_label = Label(self.Insights_Frame,
                             text=" Books Pages Read | Books Completed")

        for Info in Total_Pages:
            Pages += f'\n{Info[0]}'

        try:
            cur.execute("SELECT COUNT(*) FROM Books WHERE Progress = 100")
            Progress_Info = cur.fetchall()
            Progress = ''
            for Info in Progress_Info:
                Progress += f'{Info[0]}'
            self.Insights_Output_label.config(
                text=header_label['text'] + Pages +
                    " | " + Progress,
                font=('Helvetica bold', 18))
            cur.close()

        except Exception as e:
            self.conn.close()
            cur.close()
            self.ErrorMsg(e)
            self.conn = psycopg2.connect(
                host="localhost",
                database="Books",
                user="postgres",
                password="postgres1",
                port="5432"
            )

class GUI(SQL_Commands):
    def CreateGui(self):
        self.BT_label = Label(self.Insert_Frame, text="Book Title:")
        self.BT_label.grid(row=0, column=0, pady=10, padx=10)

        self.BT_name = Entry(self.Insert_Frame, font=("Helvetica, 18"))
        self.BT_name.grid(row=0, column=1, pady=10, padx=10)

        self.AU_label = Label(self.Insert_Frame, text="Author:")
        self.AU_label.grid(row=1, column=0, pady=10, padx=10)

        self.AU_name = Entry(self.Insert_Frame, font=("Helvetica, 18"))
        self.AU_name.grid(row=1, column=1, pady=10, padx=10)

        self.PR_label = Label(self.Insert_Frame, text="Pages Read:")
        self.PR_label.grid(row=2, column=0, pady=10, padx=10)

        self.PR_name = Entry(self.Insert_Frame, font=("Helvetica, 18"))
        self.PR_name.grid(row=2, column=1, pady=10, padx=10)

        self.TP_label = Label(self.Insert_Frame, text="Total Pages:")
        self.TP_label.grid(row=3, column=0, pady=10, padx=10)

        self.TP_name = Entry(self.Insert_Frame, font=("Helvetica, 18"))
        self.TP_name.grid(row=3, column=1, pady=10, padx=10)

        self.DI_label = Label(self.Insert_Frame,
                              text="Date Inserted (YYYY-MM-DD):")
        self.DI_label.grid(row=4, column=0, pady=10, padx=10)

        self.DI_name = Entry(self.Insert_Frame, font=("Helvetica, 18"))
        self.DI_name.grid(row=4, column=1, pady=10, padx=10)

        self.Submit_button = Button(self.Insert_Frame, text="Submit",
                                    command=self.insert)
        self.Submit_button.grid(row=5, column=1, pady=10, padx=10)
        # -----------------------------------------------------
        # -----------------------------------------------------
        # --------------UPDATE
        self.Update_BT_label = Label(self.Update_Frame,
                                     text="Book Title:")
        self.Update_BT_label.grid(row=0, column=0, pady=10, padx=10)

        self.Update_BT_name = Entry(self.Update_Frame,
                                    font=("Helvetica, 18"))
        self.Update_BT_name.grid(row=0, column=1, pady=10, padx=10)

        self.Update_AU_label = Label(self.Update_Frame, text="Author:")
        self.Update_AU_label.grid(row=1, column=0, pady=10, padx=10)

        self.Update_AU_name = Entry(self.Update_Frame,
                                    font=("Helvetica, 18"))
        self.Update_AU_name.grid(row=1, column=1, pady=10, padx=10)

        self.Update_PR_label = Label(self.Update_Frame,
                                     text="Pages Read:")
        self.Update_PR_label.grid(row=2, column=0, pady=10, padx=10)

        self.Update_PR_name = Entry(self.Update_Frame,
                                    font=("Helvetica, 18"))
        self.Update_PR_name.grid(row=2, column=1, pady=10, padx=10)

        self.Update_Submit_button = Button(self.Update_Frame,
                                           text="Update",
                                           command=self.update)
        self.Update_Submit_button.grid(row=5, column=1, pady=10,
                                       padx=10)

        # -----------------------------------------------------
        # -----------------------------------------------------
        # --------------Delete
        self.Delete_BT_label = Label(self.Delete_Frame,
                                     text="Book Title:")
        self.Delete_BT_label.grid(row=0, column=0, pady=10, padx=10)

        self.Delete_BT_name = Entry(self.Delete_Frame,
                                    font=("Helvetica, 18"))
        self.Delete_BT_name.grid(row=0, column=1, pady=10, padx=10)

        self.Delete_AU_label = Label(self.Delete_Frame, text="Author:")
        self.Delete_AU_label.grid(row=1, column=0, pady=10, padx=10)

        self.Delete_AU_name = Entry(self.Delete_Frame,
                                    font=("Helvetica, 18"))
        self.Delete_AU_name.grid(row=1, column=1, pady=10, padx=10)

        self.Delete_Submit_button = Button(self.Delete_Frame,
                                           text="Delete",
                                           command=self.delete_Book)
        self.Delete_Submit_button.grid(row=5, column=1, pady=10,
                                       padx=10)


if __name__ == '__main__':
    root = Tk()
    Manager = GUI(root)
    Manager.run()
