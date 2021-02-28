from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.config import Config
import pyrebase

Config.set('graphics','width','400')
Config.set('graphics','height','830')

firebaseConfig={'apiKey': "AIzaSyACKK3IncOVxDWTfBttBTv4KD1nZIHCLS8",
    'authDomain': "pytest-a61de.firebaseapp.com",
    'databaseURL': "https://pytest-a61de-default-rtdb.firebaseio.com",
    'projectId': "pytest-a61de",
    'storageBucket': "pytest-a61de.appspot.com",
    'messagingSenderId': "223434862368",
    'appId': "1:223434862368:web:f021f1c83a5ce0e987f145",
    'measurementId': "G-7D08G5N1GN"}

firebase=pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
storage=firebase.storage()
db = firebase.database()

username=""
userLibrary=[]
currentDebate=""
currentPlaying=""
currentPlayList=[]


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                try:
                    auth.create_user_with_email_and_password(self.email.text,self.password.text)
                    print("success")
                except:
                    invalidForm()
                    print("sugoen")
                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()
        self.makeUserProfile()

    def makeUserProfile(self):
        account=self.email.text.replace('.','-')
        account=account.replace('@','-')
        db.child(account).push({'filename':""})

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = "email"
        self.password.text = "password"
        self.namee.text = "name"

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                try: 
                    auth.sign_in_with_email_and_password(self.email.text,self.password.text)
                    #get userinfo
                    ##setUserData()
                    sm.current = "action"
                except:
                    invalidLogin()
                    print("you fked up")
            else:
                invalidForm()
        else:
            invalidForm()
        self.setUserData()
        self.reset()

    def setUserData(self):
        username=self.email.text.replace('.','-')
        username=username.replace('@','-')
        ##load from database
        userLibrary=""
        userData = db.child(username).get()
        for i in userData.each():
            currFile = i.val()['filename']
            if currFile != "":
                userLibrary.append(currFile)
        print(currFile)
        

    def createBtn(self):
        sm.current = "create"

    def reset(self):
        self.email.text = "email"
        self.password.text = "password"

class UploadWindow(Screen):
    filename = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def upload(self):
        if self.filename.text!="":
            ##TODO: call convert to JSON, check for MIDI
            ##puts file into correct folder in storage
            ##puts filename into database under user's name
            ##updates new userlibrary
            storage.child(username+"/" + self.filename.text).put(self.filename.text)
            data={'filename': self.filename.text}
            db.child(username).push(data)
            userLibrary=""
            userData = db.child(username).get()
            for i in userData.each():
                currFile = i.val()['filename']
                if currFile != "":
                    userLibrary.append(currFile)
            print(currFile)
    
    def back(self):
        sm.current = "action"

class playRemove(Screen):
    ##add something to remmeber name of selected song 
    ##add something for current user logged in
    def play(self):
        #send song to MC
        #send stop command, download from DB and then send file
        currentPlayList.clear()
        currentPlayList.append(currentDebate)
        currentPlaying = currentPlayList[0]
        sm.current="currPlay"
        print("lalalala")

    def remove(self):
        #delete item from DataBase
        print("removing")

    def addQ(self):
        #add currDebate to curr playlist
        currentPlayList.append(currentDebate)

    
    def back(self):
        sm.current = "allMusic"
##MUST REVIST ALL MUSIC TODO
class allMusic(Screen):
    def __init__(self, **kwargs):
        super(allMusic,self).__init__(**kwargs)
        # for i in range(20):
        #     button = Button(text=" "+str(i),size_hint_y=None, height=40)
        #     self.ids.grid.add_widget(button)
        # runTouchApp(self.ids.scroll)
        self.outer = FloatLayout()
        ##widgets in float layout
        self.outer.add_widget(Image(source='l2.jpg', size_hint_x=0.5, pos_hint={'x':0.25,'top':1.24999}))
        self.inner=GridLayout(size_hint_x=0.66, size_hint_y=0.25,pos_hint={'x':0.1666,'top':0.541666}, cols=1)
        self.prevB=Button(text="Prev",size_hint_x=0.25, size_hint_y=0.041666,pos_hint={'x':0.1666,'top':0.25})
        self.prevB.bind(on_release=self.prevLib)
        self.nextB=Button(text="Next",size_hint_x=0.25, size_hint_y=0.041666,pos_hint={'x':0.58333,'top':0.25})
        self.nextB.bind(on_release=self.nextLib)
        self.backB=Button(text="Back",size_hint_x=0.25, size_hint_y=0.041666,pos_hint={'x':0.1666,'top':0.1666} )
        self.backB.bind(on_release=self.back)
        self.logB=Button(text="Logout",size_hint_x=0.25, size_hint_y=0.041666, pos_hint={'x':0.58333,'top':0.1666})
        self.logB.bind(on_release=self.logOut)
       
        # for i in range(100):
        #     btn = Button(text=str(i), size_hint_y=None,size_hint_x=None,height=35)
        #     self.inner.add_widget(btn)
        # self.root = ScrollView(scroll_type=['bars'],bar_width='9dp', size_hint_x=0.66, size_hint_y=0.25,pos_hint={'x':0.1666,'top':0.541666})
        # self.root.scroll_distance = 5
        # self.root.add_widget(self.inner)
        #widgets in gridlayout
        self.song1=Button(text="song")
        self.song1.bind(on_release=self.songSelected)
        self.inner.add_widget(self.song1)
        self.song2=Button(text="song")
        self.song2.bind(on_release=self.songSelected)
        self.inner.add_widget(self.song2)
        self.song3=Button(text="song")
        self.song3.bind(on_release=self.songSelected)
        self.inner.add_widget(self.song3)
        self.song4=Button(text="song")
        self.song4.bind(on_release=self.songSelected)
        self.inner.add_widget(self.song4)
        self.song5=Button(text="song")
        self.song5.bind(on_release=self.songSelected)
        self.inner.add_widget(self.song5)
        self.song6=Button(text="song")
        self.song6.bind(on_release=self.songSelected)
        self.inner.add_widget(self.song6)

        self.outer.add_widget(self.inner)
        self.outer.add_widget(self.prevB)
        self.outer.add_widget(self.nextB)
        self.outer.add_widget(self.backB)
        self.outer.add_widget(self.logB)
        self.add_widget(self.outer)

    def on_enter(self):
        ##take first 6 songs and change text of data
        self.buttons = [self.song1, self.song2, self.song3, self.song4, self.song5, self.song6]
        for i in range(6):
            try:
                self.buttons[i].disabled=False
                self.buttons[i].text=userLibrary[i]
            except:
                self.buttons[i].disabled=True

    ##add way to dynamically add songs in    
    def songSelected(self, caller):
        #set debate
        currentDebate=caller.text
        sm.current="playRm"

    def nextLib(self, caller):
        #insert code to change names
        self.song1.text = "asdasd"
        print("next list")

    def prevLib(self, caller):
        print("last List")

    def logOut(self, caller):
        sm.current = "login"
    
    def back(self, caller):
        sm.current = "action"

class ActionWindow(Screen):
    def upload(self):
        sm.current="upload"

    def music(self):
        sm.current="allMusic"

    def sleepBtn(self):
        sm.current="sleep"

    def logoutBtn(self):
        sm.current = "login"

class MainWindow(Screen):
    def playSong(self):
        print("playing")

    def stopSong(self):
        print("stopped")

    def nextSong(self):
        print("skipping")

    def prevSong(self):
        print("going back")

    def back(self):
        sm.current = "allMusic"
    
    def logout(self):
        sm.current = "login"

class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
#db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="currPlay"),ActionWindow(name="action"), UploadWindow(name="upload"),allMusic(name="allMusic"),playRemove(name="playRm")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"

class MyMainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyMainApp().run()