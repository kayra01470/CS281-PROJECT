#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 21:41:01 2024

@author: cengizmenten
"""

import random
import sqlite3
import PySimpleGUI as sg
from datetime import datetime

# connect to the DB
con = sqlite3.connect('IMDB Project.db')
cur = con.cursor()
sg.theme('DarkGrey1')
# global variables
login_user_email = -1
login_user_name = -1
login_user_type = -1

# window functions
def window_login():
    
    layout = [[sg.Text('Welcome to the IMDB. Please login.',font=('Helvetica', 14, 'bold'))],
              [sg.Text('Email:',size=(40,1)), sg.Input(size=(40,1), key='email')],
              [sg.Text('Password:',size=(40,1)), sg.Input(size=(40,1), key='password', password_char='*')],
              [sg.Button('Login',border_width=5, pad=(10, 10))],[sg.Button('Register', border_width=5, pad=(10, 10))]]

    return sg.Window('Login Window', layout)

def window_Admin():
    
    layout = [[sg.Text('Welcome ' + login_user_name.capitalize())],
              [sg.Button('Add new show')],
              [sg.Button("List Available Shows")],
              [sg.Button('Control the Comments')],
              [sg.Button('Control the Discussions')],
              [sg.Button('Logout')]]
    return sg.Window('Admin Window', layout)

def window_User():
    
    layout = [[sg.Text('Welcome ' + login_user_name.capitalize())],
              [sg.Button('Show my rating')],
              [sg.Button('Labeling')],
              [sg.Button("Display my list")],
              [sg.Button("Display rates")],
              [sg.Button('Comment')],
              [sg.Button('Show other Comments')],
              [sg.Button('Discussions')],
              [sg.Button('Logout')]]

    return sg.Window('Admin Window', layout)

def window_register():
    
    layout = [[sg.Text('email:',size=(40,1)), sg.Input(key='email',size=(40,1))],
              [sg.Text('Name:',size=(40,1)), sg.Input(key='Name',size=(40,1))],
              [sg.Text('Surname:',size=(40,1)), sg.Input(key='Surname',size=(40,1))],
              [sg.Text('Password:',size=(40,1)), sg.Input(key='Password',size=(40,1))],
              [sg.Text('username:',size=(40,1)), sg.Input(key='username',size=(40,1))],
              [sg.Button('Register Now'),sg.Button('Return To Main')]]
    
    return sg.Window('Registeration Window' , layout)
    
def window_registering(values):
    
    Name = values['Name']
    username = values['username']
    email = values['email']
    Surname = values['Surname']
    Password = values['Password']
    
    
    uemail = values['email']
    cur.execute('Select uemail from User where uemail=?',(uemail,) )
    existing_uemail = cur.fetchone()
    username_ =values['username']
    cur.execute('Select username from User where username =?',(username_,))
    existing_username = cur.fetchone()
    
    if username == '':
        sg.popup('Username cannot be empty!')
    elif Password == '':
        sg.popup('Password cannot be empty!')
    elif email == '':
        sg.popup('Email cannot be empty!')
    elif existing_uemail:
        sg.popup('This email is already used')
    elif existing_username:
        sg.popup("This username has been taken")
        
    
        
   
    else:
        
        cur.execute('INSERT INTO User VALUES (?,?)',(username,uemail))
        cur.execute('Insert INTO Account VALUES(?,?,?,?)', (email,Name,Surname,Password))
        
        
        sg.popup('Successfully Registered '  + ' ' + 'Welcome' + ' ' + Name)
            # clear inputs
        window.Element('Name').Update(value='')
        
       
        window.Element('Surname').Update(value='')
        window.Element('Password').Update(value='')
        window.Element('username').Update(value='')
        window.Element('email').Update(value='')
def window_discussions():
    discussion = []
    shows = []
    
    for row in cur.execute('''Select name,ID from Show'''):
        shows.append(row)
    
    for row in cur.execute('''Select did,description FROM Discussion'''):
        discussion.append(row)
    
    layout = [[sg.Listbox(discussion, size=(100,10), key='discussion'), sg.Combo(shows,default_value='interstellar 1',key='show'),sg.Button('Filter')],
              [sg.Text('Discussion'), sg.Input(key='Discussion'),sg.Button('Add Discussion') ],
              [sg.Button('Look at Opinions'),sg.Button('Return To Main')]]

    return sg.Window('Discussions', layout)

def window_show_discussion_from_Admin():
    shows =[]
    for row in cur.execute('SELECT ID,name from Show'):
        shows.append(row)
    layout = [[sg.Text('Show:'), sg.Combo(shows,default_value='1 interstellar', key='show'), sg.Button('Control these discussions')],
              [sg.Button('Return To Main')]]
    return sg.Window('Show Discussions',layout)


    

def control_these_discussions(values):
    
    global show_name 
    global show
    show = values['show']
    if show == ' ':
        sg.popup('Please choose a film first')
    else:
        global show_name
        show_name = show[1]  
        discussion = []

        for row in cur.execute('''SELECT d.description,d.did
                                   FROM Discussion d, Initiate i, Show s
                                   WHERE d.did = i.did AND s.ID = i.ID AND s.name = ?''', (show_name,)):
            discussion.append(row)

        layout = [[sg.Listbox(discussion, size=(100, 10), key='discussion')],
                  [sg.Button('Show the Opinions for this discussion')],
                  [sg.Button('Delete this Discussion')],
                  [sg.Button('Return To Main')]]

    return sg.Window('Discussion Control Window', layout)
    
def window_show_opinion_for_admin(values):
    discussion = values["discussion"]
    if discussion == []:
        sg.popup("Please choose a discussion first")
        global show_name 
        discussion = []

        for row in cur.execute('''SELECT d.description,d.did
                                   FROM Discussion d, Initiate i, Show s
                                   WHERE d.did = i.did AND s.ID = i.ID AND s.name = ?''', (show_name,)):
            discussion.append(row)

        layout = [[sg.Listbox(discussion, size=(100, 10), key='discussion')],
                  [sg.Button('Show the Opinions for this discussion')],
                  [sg.Button('Delete this Discussion')],
                  [sg.Button('Return To Main')]]
  
    else:
        global did
        did = discussion[0][1]
        opinion = []
        
        for row in cur.execute('''SELECT o.oid, o.content
                                    From Opinion o,Discussion d
                                    WHERE o.did = d.did AND d.did=?''',(did,)):
            opinion.append(row)
        
        layout = [[sg.Listbox(opinion, size=(70, 10), key='opinion')],
                  [sg.Button('Delete this opinion')],
                  [sg.Button('Return To Main')]]
        
    return sg.Window('Opinion Control Window', layout)
def deleting_opinions(values):
    opinion = values['opinion']
    if opinion == []:
        sg.popup("Choose a opinion first")
        
    else:
        oid = opinion[0][0]
        cur.execute('''DELETE FROM Opinion WHERE oid = ? ''',(oid,))
        sg.popup('Successfully Deleted')
        opinions_after_delete = []
        for row in cur.execute('''Select o.oid,o.content FROM Opinion o , Discussion d WHERE d.did = o.did AND d.did = ?''',(did,)):
            opinions_after_delete.append(row)
        window.Element('opinion').Update(values= opinions_after_delete)

def deleting_discussions(values):
    
    discussion = values['discussion']
    if discussion == [] :
        sg.popup("choose a discussion first")
    else:
        did = discussion[0][1]
        
        cur.execute('''DELETE FROM Discussion WHERE did = ?''', (did,))
        cur.execute('''DELETE FROM Initiate  WHERE  did = ?''', (did,))
        cur.execute('''DELETE FROM Opinion WHERE did = ? ''',(did,))
        sg.popup('Successfully Deleted')
        
        
        discussions_after_delete = []
        global show
        global show_name
        show_name = show[1]  
        discussion = []

        for row in cur.execute('''SELECT d.description,d.did
                                   FROM Discussion d, Initiate i, Show s
                                   WHERE d.did = i.did AND s.ID = i.ID AND s.name = ?''', (show_name,)):
            discussions_after_delete.append(row)

           
        window.Element('discussion').Update(values= discussions_after_delete)


    
def show_the_discussions(values):
    discussion = []
    shows = values['show']
    
    

    show_name = shows[0]
   
    for row in cur.execute('''SELECT d.description
                                   FROM Initiate i, Discussion d, Show s
                                   WHERE i.ID = s.ID AND d.did = i.did AND s.name = ?''', (show_name,)):
        discussion.append(row)
    
    layout = [[sg.Listbox(discussion, size=(100,10), key='discussion')],
              [sg.Button('Return to Discussion')]]   
    
    return sg.Window('Discussions', layout) 

def add_discussion(values):
    show = values['show']
    show_name= show[0]
    
    show_id = show[1]
    description = values['Discussion']
    if description == '':
        sg.popup('Please Enter Your Discussion Text')
        
    else:
        cur.execute('SELECT MAX(did) FROM Discussion')
        row = cur.fetchone()
        if row is None:
           
            new_did = 1
        else:
            new_did = row[0] + 1
        
       
        cur.execute('INSERT INTO Discussion VALUES (?,?)',(new_did,description))
        cur.execute('Insert INTO Initiate VALUES (?,?,?)', (login_user_email,show_id,new_did))
        
        sg.popup('Discussion Successfully Added ')
        adding_after =[]
        for row in cur.execute('''Select description FROM Discussion'''):
            adding_after.append(row)
            
        window.Element('Discussion').Update(value='')
        window.Element('discussion').Update(values=adding_after)
        
def window_look_at_opinions(values):
    opinion = []
    valuedid = values['discussion']
    if valuedid ==[]:
        sg.Popup('Please Choose a Discussion First!')
        discussion = []
        shows = []
    
        for row in cur.execute('''Select name,ID from Show'''):
            shows.append(row)
    
        for row in cur.execute('''Select did,description FROM Discussion'''):
            discussion.append(row)
        
        layout = [[sg.Listbox(discussion, size=(100,10), key='discussion'), sg.Combo(shows,default_value='interstellar 1',key='show'),sg.Button('Filter')],
              [sg.Text('Discussion'), sg.Input(key='Discussion'),sg.Button('Add Discussion') ],
              [sg.Button('Look at Opinions'),sg.Button('Return To Main')]]
        
    else:
        global did
        did = valuedid[0][0]
       
    
        for row in cur.execute('''SELECT u.username, ':' , o.content 
               FROM Opinion o, User u 
               WHERE u.uemail = o.uemail AND o.did = ?''', (did,)):
            opinion.append(row)
        
        layout = [[sg.Listbox(opinion ,size =(40,10),key='opinion')],
              [sg.Text('Add Your Opinion'), sg.Input(key='Add Your Opinion'),sg.Button('Add Opinion')],    
              [sg.Button('Return to Discussion')]]
    
    return sg.Window('Opinion', layout)
 
def adding_new_opinion(values):
    global did
    new_opinion = values["Add Your Opinion"]
    if new_opinion == []:
        sg.popup("Please Enter an Opinion")
    else: 
        cur.execute('SELECT MAX(oid) FROM Opinion')
        row = cur.fetchone()
        if row is None:
            new_oid = 1
        else:
            new_oid = row[0] + 1
        
        cur.execute('INSERT INTO Opinion VALUES (?,?,?,?)',(new_oid,did,login_user_email,new_opinion))
        sg.popup('Opinion Successfully Added ')
        
        opinion_after_adding = []
        for row in cur.execute('''SELECT u.username, ':' , o.content 
               FROM Opinion o, User u 
               WHERE u.uemail = o.uemail AND o.did = ?''', (did,)):
            opinion_after_adding.append(row)
        window.Element("Add Your Opinion").Update(value = "")
        window.Element('opinion').Update(values=opinion_after_adding)
    
    
def window_add_new_show():
    
    layout = [[sg.Text('name:',size=(10,1)), sg.Input(key='name',size=(10,1))],
              [sg.Text('genre:',size=(10,1)), sg.Input(key='genre',size=(10,1))],
              [sg.Text('year:',size=(10,1)), sg.Input(key='year',size=(10,1))],
              [sg.Text('type:',size=(10,1)), sg.Input(key='type',size=(10,1))],
              [sg.Text('stars:',size=(10,1)), sg.Input(key='stars',size=(10,1))],
              [sg.Text('psummary:',size=(10,1)), sg.Input(key='psummary',size=(10,1))],
              [sg.Button('Insert'), sg.Button('Return To Main')]]

    return sg.Window('Insert Window', layout)

def button_login(values):
    
    global login_user_email
    global login_user_name
    global login_user_type
    global window
    
    uemail = values['email']
    upass = values['password']
    if uemail == '':
        sg.popup('Email cannot be empty')
    elif upass == '':
        sg.popup('Password cannot be empty')
    else:
        # first check if this is a valid user
        cur.execute('SELECT email, Name FROM Account WHERE email = ? AND Password = ?', (uemail,upass))
        row = cur.fetchone()
        
        if row is None:
            sg.popup('Email or password is wrong!')
        else:
            # since it is some existing user,the email of this account is in the global variable
            login_user_email = row[0]
            
            login_user_name = row[1]
            
            # find which type of account this login_user_email belongs to
            # check if this is a user
            cur.execute('SELECT uemail FROM User WHERE uemail = ?', (uemail,))
            row_user = cur.fetchone()
            
            if row_user is None:
                # this is not a user, check for admin
                cur.execute('SELECT aemail FROM Admin WHERE aemail = ?', (uemail,))
                row_admin = cur.fetchone()
                if row_admin is None:
                    # this is not a admin also, then there should be some problem with the DB
                    # since we expect a user to be either a user or a admin
                    sg.popup('User type error! Please contact the admin.')
                else:
                    # this is a admin
                    login_user_type = 'Admin'
                    sg.popup('Welcome, ' + login_user_name.capitalize() + ' (Admin)')
                    window.close()
                    window = window_Admin()
            else:
                # this is a user
                    login_user_type = 'User'
                    sg.popup('Welcome, ' + login_user_name.capitalize() + ' (User)')
                    window.close()
                    window = window_User()

def button_insert(values):

    name = values['name']
    genre = values['genre']
    year = values['year']
    type = values['type']
    stars = values['stars']
    psummary = values['psummary']
   
    
    if name == '':
        sg.popup('name cannot be empty!')
        # for this show we should find the next available id
    else:
        cur.execute('SELECT MAX(ID) FROM Show')
        row = cur.fetchone()
        if row is None:
           # this is when there is no user in the system
            new_id = 1
        else:
            new_id = row[0] + 1
        # first insert to the Show table
        cur.execute('INSERT INTO Show VALUES (?,?,?,?,?,?,?)',(new_id,psummary,stars,name,genre,year,type))
        
        sg.popup('Successfully inserted '  + ' ' + name + ' with id: ' + str(new_id) )
            # clear inputs
        window.Element('name').Update(value='')
        window.Element('genre').Update(value='')
        window.Element('year').Update(value='')
        window.Element('type').Update(value='')
        window.Element('stars').Update(value='')
        window.Element('psummary').Update(value='')


def window_available_show():
    
    shows = []  
    for row in cur.execute('''SELECT name,genre,year,type,stars
                               FROM Show
                               '''):
         shows.append(row)
    
    layout = [[sg.Listbox(shows, size=(100,10), key='show')],
              [sg.Button('Return To Main')]]

    return sg.Window('Available Show Window', layout)

def window_rate():
    
    shows = []
    
    for row in cur.execute('''SELECT List.Category,Show.name,Show.ID
                               FROM Show,List
                               Where Show.ID=List.ID AND uemail = ?''',(login_user_email,)):
        shows.append(row)
    
    layout = [[sg.Listbox(shows, size=(40,10), key='show')],
              [sg.Text('Rate: '), sg.Input(key='rate'), sg.Button('Rate Show')],
              [sg.Button('Return To Main')]]

    return sg.Window('Rate Window', layout)



def button_rate(values):
    
    show = values['show']
    rate = values['rate']
    category_of_shows = []
    already_rated_users = []
    valid_for_rate = []
    for row in cur.execute('''Select Category, ID
                           FROM List
                           where uemail = ?''',(login_user_email,)):
                category_of_shows.append(row)

    for row in category_of_shows:
        if row[0] == "Completed" or row[0] == "Dropped":
            valid_for_rate.append(row[1])
            
    for row in cur.execute("SELECT uemail,ID FROM Give "):
        already_rated_users.append(row)
    
    if len(show) == 0:
        sg.popup('Please choose a show first.')
    elif rate == '':
        sg.popup('Please enter rate.')
    elif  show[0][2] not in valid_for_rate:
        sg.popup("The show must be labeled as Completed or Dropped")

    elif not rate.isnumeric():
        sg.popup('Rate should be numeric!')
    elif (login_user_email,show[0][2]) in already_rated_users:
        sg.popup("You already rated this show.")
            
    else:
        cur.execute('SELECT MAX(rid) FROM Rate')
        row = cur.fetchone()
        if row is None:
           # this is when there is no user in the system
            rate_id = 1
            
        else:
            rate_id = row[0] + 1
            
        rate_value = int(rate)
        
        if rate_value < 0 or rate_value > 10:
             sg.popup('rate should be in [0,10] range!')
        else:
            
            show_id = show[0][2]
            
            
            
            cur.execute('Insert INTO Rate VALUES (?,?)' , (rate_id,rate_value))
            cur.execute('Insert INTO Give VALUES(?,?,?)', (show_id,rate_id,login_user_email))
            sg.popup('Successfully rated ')
            
            # clear the rate input
            window.Element('rate').Update(value='')
            
def window_comment():
    
    shows = []
    
    for row in cur.execute('''SELECT List.Category,Show.name,Show.ID
                               FROM Show,List
                               Where Show.ID=List.ID AND uemail = ?''',(login_user_email,)):
        shows.append(row)
    
    layout = [[sg.Listbox(shows, size=(40,10), key='show')],
              [sg.Text('Comment'), sg.Input(key='Comment'), sg.Button('Enter your Comment')],
              [sg.Button('Return To Main')]]

    return sg.Window('Comment Window', layout)

def button_comment(values):
    
    show = values['show']
    comment = values['Comment']
    category_of_shows = []

    valid_for_commenting = []
    for row in cur.execute('''Select Category, ID
                           FROM List
                           where uemail = ?''',(login_user_email,)):
                category_of_shows.append(row)

    for row in category_of_shows:
        if row[0] == "Completed" or row[0] == "Dropped":
            valid_for_commenting.append(row[1])
            
   
    
    if len(show) == 0:
        sg.popup('Please choose a show first.')
    elif comment == '':
        sg.popup('Please enter you comments.')
    elif  show[0][2] not in valid_for_commenting:
        sg.popup("The show must be labeled as Completed or Dropped")

   
            
    else:
        cur.execute('SELECT MAX(CID) FROM Comment')
        row = cur.fetchone()
        if row is None:
           # this is when there is no user in the system
            cid = 1
            
        else:
            cid = row[0] + 1
            
        
        
        
            
        show_id = show[0][2]
            
            
            
        cur.execute('Insert INTO Comment VALUES (?,?)' , (cid,comment))
        cur.execute('Insert INTO Leave VALUES(?,?,?)', (login_user_email,show_id,cid,))
        sg.popup('Successfully Commented ')
            
            # clear the rate input
        window.Element('Comment').Update(value='')
    
def window_label():
    
    shows = []
    
    for row in cur.execute('''SELECT ID,name
                              FROM Show
                              '''):
        shows.append(row)
    
    categories = ['Completed', 'Watching', 'Dropped', 'Plan to Watch']

    layout = [[sg.Listbox(shows, size=(40, 10), key='show')],
        [sg.Text('Category:'), sg.Combo(categories, default_value='Completed', key='category'), sg.Button('Add to List')],
        [sg.Button('Return To Main')]]

    return sg.Window('Label Window', layout)

def window_listing():
    
    shows = []
    
    for row in cur.execute('''SELECT ID,name
                              FROM Show
                              '''):
        shows.append(row)
    
    categories = ['Completed', 'Watching', 'Dropped', 'Plan to Watch']

    layout = [[sg.Listbox(shows, size=(40, 10), key='show')],
        [sg.Text('Category:'), sg.Combo(categories, default_value='Completed', key='category'), sg.Button('Add to List')],
        [sg.Button('Return To Main')]]

    return sg.Window('Label Window', layout)

def button_label(values):
    show = values['show']
    category = values['category']
    # Assuming cur is the cursor object for database
    if len(show) == 0:
        sg.popup('Please choose a show first.')
    else:
        # Assuming show_id and login_user_email are defined somewhere
        if len(show) > 0:
            show_id = show[0][0]  # Assuming show[0][0] contains the ID of the selected show
            cur.execute('''SELECT category,ID FROM List where uemail=? and ID =? ''',(login_user_email,show_id))
            existing_label = cur.fetchone()
            if existing_label:
                sg.popup("You have already labeled")
            elif not existing_label:
            # Insert the show into the List table
                cur.execute('INSERT INTO List VALUES (?, ?, ?)',
                            (category, login_user_email, show_id))
                sg.popup('Successfully labeled')
            
            else: 
                cur.execute('''UPDATE List SET Values (?,?,?)''',(category,login_user_email,show_id))
            window.Element('category').Update(value='')
            
def window_user_list():
    categories = []
    
    for row in cur.execute('''SELECT category
                              FROM List
                              '''):
        categories.append(row)
    
    categories = ['Completed', 'Watching', 'Dropped', 'Plan to Watch']
    layout = [
        [sg.Text('Category:'), sg.Combo(categories, default_value='Completed', key='category'), sg.Button('Demostrate')],
        [sg.Button('Return To Main')]
    ]

    return sg.Window('List Window', layout)

def window_check_rate():
    shows = []  
    for row in cur.execute('''SELECT ID, name FROM Show'''):
        shows.append(row)
    layout = [
        [sg.Text('Show:'), sg.Combo(shows,default_value='1 interstellar', key='show'), sg.Button('Check Rate')],
        [sg.Button('Return To Main')]
    ]
    return sg.Window('List Window', layout)

def button_check_rate(values):
    show = values['show']  # Extract the selected show ID
    show_id = show[0]
    query = cur.execute('''SELECT s.name, AVG(r.rate) AS average_rating
               FROM Show s
               JOIN Give g ON s.ID = g.ID
               JOIN Rate r ON g.rid = r.rid
               WHERE  s.ID = ?
               GROUP BY s.name''',(show_id,))

    shows_list = []
    for row in query:
        shows_list.append(row)

    if len(shows_list) > 0:
        show_name, average_rating = shows_list[0]
        sg.popup(f"Show: {show_name}, Average Rating: {average_rating}")
    else:
        sg.popup("No ratings found for this show.")
        


def window_show_comment():
    shows =[]
    for row in cur.execute('SELECT ID,name from Show'):
        shows.append(row)
    layout = [[sg.Text('Show:'), sg.Combo(shows,default_value='1 interstellar', key='show'), sg.Button('See Comments')],
              [sg.Button('Return To Main')]]
    return sg.Window('Show Comments',layout)

def button_see_comment(values):
    
    show = values['show']
    show_id = show[0]
    show_name = show[1]
    code = cur.execute('''Select  c.comment FROM show s, leave l, comment c where l.ID = s.ID and l.cid = c.CID and s.ID=? ''',(show_id,))
    shows_list = [row[0] for row in code]
    
    if shows_list:
        comment_text = '\n'.join(shows_list)
        sg.popup(f'Show : {show_name}\nComments:\n{comment_text}')
    else:
        sg.popup("No comment for this show")
        
def window_show_comment_from_Admin():
    shows =[]
    for row in cur.execute('SELECT ID,name from Show'):
        shows.append(row)
    layout = [[sg.Text('Show:'), sg.Combo(shows,default_value='1 interstellar', key='show'), sg.Button('Control these Comments')],
              [sg.Button('Return To Main')]]
    return sg.Window('Show Comments',layout)

def control_these_comments(values):
    
    global show_name  
    show = values['show']
    if show == ' ':
        sg.popup('Please choose a film first')
    else:
        show_name = show[1]  
        comment = []

        for row in cur.execute('''SELECT c.comment, c.cid
                                   FROM Comment c, Leave l, Show s
                                   WHERE c.CID = l.CID AND s.ID = l.ID AND s.name = ?''', (show_name,)):
            comment.append(row)

        layout = [[sg.Listbox(comment, size=(70, 10), key='comment')],
                  [sg.Button('Delete this Comment')],
                  [sg.Button('Return To Main')]]

        return sg.Window('Control Window', layout)

def deleting_comment(values):
    global show_name
    comment = values['comment']
    if not comment:
        sg.popup("Please select a comment first")
    elif comment:
        cid = comment[0][1]
        
        cur.execute('''DELETE FROM Comment WHERE cid = ?''', (cid,))
        cur.execute('''DELETE FROM Leave  WHERE  cid = ?''', (cid,))
        sg.popup('Successfully Deleted')
        
        
        comments_after_delete = []
        for row in cur.execute('''SELECT c.comment
                                  FROM Comment c, Leave l, Show s
                                  WHERE c.CID = l.CID AND s.ID = l.ID AND s.name = ?''', (show_name,)):
            comments_after_delete.append(row)

       
        window.Element('comment').Update(values=comments_after_delete)
    
    
    
def window_user_list_display(values):
    category = values["category"]
    shows_in_user_list =[]
    for row in cur.execute('''Select Category, List.ID,Show.name, Show.year,Show.genre, Show.type,Show.stars
                           FROM List,Show
                           where List.ID = Show.ID AND uemail = ? AND List.category= ?''',(login_user_email,category)):
                shows_in_user_list.append(row)
                
    
    layout = [[sg.Listbox(shows_in_user_list,size=(70,10),key = "list")],
           [sg.Button("Return To Main")]]
            
    return sg.Window("User List Window",layout)
    

            
            
            
window = window_login()
while True:
    event, values = window.read()
    if event == 'Login':
        button_login(values)
    elif event == 'Register':
        window.close()
        window = window_register()
    elif event == 'Delete this Comment':
        deleting_comment(values)
    elif event == 'Add new show':
            window.close()
            window = window_add_new_show()
    elif event == 'Control the Comments':
        window.close()
        window = window_show_comment_from_Admin()
    elif event == 'Control these Comments':
        window.close()
        window = control_these_comments(values)
    elif event == 'Return To Main':
        if login_user_type == 'Admin':
            window.close()
            window = window_Admin()
        elif login_user_type == 'User':
            window.close()
            window = window_User()
        else:
            # this should not happen, but in case happens return to login window
            window.close()
            window = window_login() 
    elif event == 'Insert':
        button_insert(values)
    elif event == "List Available Shows":
        window.close()
        window = window_available_show()
    elif event == "Show my rating":
        window.close()
        window =window_rate()
    elif event =='Discussions':
        window.close()
        window = window_discussions()
    elif event == 'Return to Discussion':
        window.close()
        window = window_discussions()
    elif event == 'Add Opinion':
        adding_new_opinion(values)
        
        
    elif event == 'Register Now':
         window_registering(values)
    elif event == "Rate Show":
        button_rate(values)
        window.close()
        window = window_rate()
    elif event == "Comment":
        window.close()
        window = window_comment()
    elif event =="Enter your Comment":
        button_comment(values)
        window.close()
        window = window_comment()
    elif event == 'Show other Comments':
        window.close()
        window = window_show_comment()
    elif event == 'See Comments':
        button_see_comment(values)
    elif event== 'Filter':
        window.close()
        window =show_the_discussions(values)
    elif event == 'Look at Opinions':
        window.close()
        window = window_look_at_opinions(values)
    elif event == "Delete Discussion":
        window.close()
        control_these_discussions(values)
    elif event == 'Delete this Discussion':
        deleting_discussions(values)
        
        
    elif event == "Labeling":
        window.close()
        window = window_label()
    elif event == "Add to List":
        button_label(values)
    elif event == "Display my list":
        window.close()
        window = window_user_list()
    elif event == "Demostrate":
        window.close()
        window = window_user_list_display(values)
    elif event== 'Add Discussion':
        add_discussion(values)
    elif event == 'Control the Discussions':
        window.close()
        window = window_show_discussion_from_Admin()
    elif event == "Control these discussions":
        window.close()
        window = control_these_discussions(values)
    elif event == 'Show the Opinions for this discussion':
        window.close()
        window = window_show_opinion_for_admin(values)
        
    elif event == 'Delete this opinion':
        deleting_opinions(values)
    elif event== "Display rates":
        window.close()
        window = window_check_rate()    
    elif event == "Check Rate":
        button_check_rate(values)
    elif event == 'Logout':
        # set login user global parameters
        login_user_email = -1
        login_user_name = -1
        login_user_type = -10
        window.close()
        window = window_login()
    elif event == sg.WIN_CLOSED:
        break
            
window.close()
con.commit()
con.close()