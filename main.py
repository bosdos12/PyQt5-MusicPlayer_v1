import sys
import json
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import QTimer as pyqtTimer
import time
import os
import pygame
from mutagen.mp3 import MP3

# Mixer;
pygame.mixer.init()

# Some notes:
#app.primaryScreen().size().width())

# Returns the desired screen percentage based off the current screen width/height;
def PercentageValue(p, s, a):
    width = a.primaryScreen().size().width()
    height = a.primaryScreen().size().height()
    if (p > 0) and p <= 100:
        if s == "h":
            return int((p/100)*height)
        elif s == "w":
            return int((p/100)*width)

        else:
            print(f"Invalid argument, please enter either 'v' or 'h' as the first parameter,\n{str(s)} is invalid;") 
    else:
        print(f"Please enter a percentage value between 0 and 100,\n{str(p)} is invalid;")



# If the user isnt logged in, this page will open and the user will have to login;
class LoginPage(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.wantedUsername = "numba1"
        self.wantedPassword = "123"

        self.setStyleSheet("""
        QPushButton:hover:!pressed
            {
                background-color: white;
            }
        """)

        loginInputsFrame = qtw.QFrame(self)
        loginInputsFrame.setFixedSize(PercentageValue(36, "w", app), PercentageValue(70, "h", app))
        loginInputsFrame.setStyleSheet("background-color: lightgray; border: 3px solid black; border-radius: 50")
        loginInputsFrame.move(PercentageValue(32, "w", app), PercentageValue(15, "h", app))

        loginInfoLabel = qtw.QLabel("Please login", self)
        loginInfoLabel.setFont(qtg.QFont("Arial", PercentageValue(3, "w", app)))
        loginInfoLabel.move(PercentageValue(39, "w", app), PercentageValue(24, "h", app))

        self.usernameErrorLabel = qtw.QLabel("--------------------------------------------------------------------------------------------------", self)
        self.usernameErrorLabel.setFont(qtg.QFont("Arial", PercentageValue(1, "w", app)))
        self.usernameErrorLabel.setStyleSheet("color: red;")
        self.usernameErrorLabel.move(PercentageValue(40, "w", app), PercentageValue(33.9, "h", app))
        self.usernameErrorLabel.setVisible(False)

        self.usernameEntry = qtw.QLineEdit(self)
        self.usernameEntry.setFixedSize(PercentageValue(20, "w", app), PercentageValue(5, "h", app))
        self.usernameEntry.setFont(qtg.QFont("Arial", PercentageValue(1, "w", app)))
        self.usernameEntry.move(PercentageValue(40, "w", app), PercentageValue(36, "h", app))
        self.usernameEntry.setPlaceholderText("Username: ")

        self.passwordErrorLabel = qtw.QLabel("--------------------------------------------------------------------------------------------------", self)
        self.passwordErrorLabel.setFont(qtg.QFont("Arial", PercentageValue(1, "w", app)))
        self.passwordErrorLabel.setStyleSheet("color: red;")
        self.passwordErrorLabel.move(PercentageValue(40, "w", app), PercentageValue(43.9, "h", app))
        self.passwordErrorLabel.setVisible(False)

        self.passwordEntry = qtw.QLineEdit(self)
        self.passwordEntry.setFixedSize(PercentageValue(20, "w", app), PercentageValue(5, "h", app))
        self.passwordEntry.setFont(qtg.QFont("Arial", PercentageValue(1, "w", app)))
        self.passwordEntry.move(PercentageValue(40, "w", app), PercentageValue(46, "h", app))
        self.passwordEntry.setPlaceholderText("Password: ")
        self.passwordEntry.setEchoMode(qtw.QLineEdit.Password)
        
        loginButton = qtw.QPushButton("Login", self, clicked=lambda: self.loginF())
        loginButton.setFixedSize(PercentageValue(14, "w", app), PercentageValue(6, "h", app))
        loginButton.setFont(qtg.QFont("Arial", PercentageValue(2, "w", app)))
        loginButton.setStyleSheet("border: 2px solid black;border-radius: 25px;")
        loginButton.move(PercentageValue(43, "w", app), PercentageValue(56, "h", app))




    def loginF(self):
        enteredUsn = self.usernameEntry.text()
        enteredPass = self.passwordEntry.text()

        # Clearing the entries;
        self.usernameEntry.setText("")
        self.passwordEntry.setText("")

        if len(enteredUsn) > 0:
            self.usernameErrorLabel.setVisible(False)
            if len(enteredPass) > 0:
                self.passwordErrorLabel.setVisible(False)
                if enteredUsn == self.wantedUsername:
                    self.usernameErrorLabel.setVisible(False)
                    if enteredPass == self.wantedPassword:
                        self.passwordErrorLabel.setVisible(False)
                        with open("./Data/userData.json", "r") as rd:
                            wd = json.load(rd)
                        wd["loggedIn"] = True
                        wd["userData"]["username"] = enteredUsn
                        wd["userData"]["password"] = enteredPass
                        wd["userData"]["bio"] = ""
                        with open("./Data/userData.json", "w") as wpd:
                            json.dump(wd, wpd)

                        hp = HomePage()
                        appStack.addWidget(hp)
                        appStack.setCurrentIndex(appStack.currentIndex()+1)
                    else:
                        self.passwordErrorLabel.setVisible(True)
                        self.passwordErrorLabel.setText("Invalid password.")
                else:
                    self.usernameErrorLabel.setVisible(True)
                    self.usernameErrorLabel.setText("Invalid username.")
            else:
                self.passwordErrorLabel.setVisible(True)
                self.passwordErrorLabel.setText("Please enter a password.")
        else:
            self.usernameErrorLabel.setVisible(True)
            self.usernameErrorLabel.setText("Please enter a username.")





# This is the homepage the user will use;
class HomePage(qtw.QWidget):
    def __init__(self):
        super(HomePage, self).__init__()
        # app state data;
        self.allSongs = [] 
        # All songs is the variable which will get all the songs names assigned to, 
        # which then will be used for iterative song frame + info creation;
        self.songsButtons = []
        self.currentSongIndex = 0
        self.currentSongTimeState = 0
        self.currentSongLength = 0

        # First creating some basic layout gridboxes;
        self.songsLocation = qtw.QScrollArea(self)
        self.songsLocation.setWidgetResizable(True)
        self.scrollAreaWidgetContents = qtw.QWidget()
        self.songsLocation.setStyleSheet("background-color: rgb(17, 20, 66);")
        self.songsLocation.setFixedSize(PercentageValue(82, "w", app), PercentageValue(86, "h", app))
        self.songsLocation.move(-1, -1)
        self.SongsGrid = qtw.QGridLayout(self.scrollAreaWidgetContents)
        self.songsLocation.setWidget(self.scrollAreaWidgetContents)

        # Username location;
        usernameLocation = qtw.QFrame(self)
        usernameLocation.setStyleSheet("background-color: rgb(200, 191, 231);")
        usernameLocation.setFixedSize(PercentageValue(19, "w", app), PercentageValue(12, "h", app))
        usernameLocation.move(PercentageValue(81.9, "w", app), 0)

        # Username label;
        self.usernameText = qtw.QLabel("                                  ", self)
        self.usernameText.setFont(qtg.QFont("Arial", PercentageValue(1, "w", app)+10))
        self.usernameText.setStyleSheet("color: white;")
        self.usernameText.move(PercentageValue(82, "w", app)+5, PercentageValue(5, "h", app))

        # Bio location;
        bioLocation = qtw.QFrame(self)
        bioLocation.setStyleSheet("background-color: rgb(63, 72, 204);")
        bioLocation.setFixedSize(PercentageValue(19, "w", app), PercentageValue(73.9, "h", app))
        bioLocation.move(PercentageValue(81.9, "w", app), PercentageValue(12, "h", app))

        # Bio text area;    
        self.bioTextArea = qtw.QTextEdit(self)
        self.bioTextArea.setFont(qtg.QFont("Arial", PercentageValue(1, "w", app)))
        self.bioTextArea.setStyleSheet("background-color: white;")
        self.bioTextArea.setFixedSize(PercentageValue(18, "w", app), PercentageValue(65.9, "h", app))
        self.bioTextArea.move(PercentageValue(82, "w", app), PercentageValue(12, "h", app))
        self.bioTextArea.setPlaceholderText("Your Bio Here")

        # Save bio button
        saveBioButton = qtw.QPushButton("Save", self, clicked=lambda:self.editBioF())
        saveBioButton.setFixedSize(PercentageValue(8, "w", app), PercentageValue(4, "h", app))
        saveBioButton.setFont(qtg.QFont("Arial", PercentageValue(1, "w", app)))
        saveBioButton.move(PercentageValue(87, "w", app), PercentageValue(79, "h", app))


        # Music Player Location;
        self.musicPlayerLocation = qtw.QGroupBox(self)
        self.musicPlayerLocation.setStyleSheet("background-color: black; border: 2px solid black;")
        self.musicPlayerLocation.setFixedSize(PercentageValue(100, "w", app), PercentageValue(16, "h", app))
        self.musicPlayerLocation.move(0, PercentageValue(85, "h", app)-2)

        # Music timer;
        self.musicTimer = qtw.QLabel("                                                                ", self)
        self.musicTimer.setFont(qtg.QFont("Arial", PercentageValue(0.9, "w", app)))
        self.musicTimer.setStyleSheet("color: rgb(34, 177, 76);")
        self.musicTimer.move(PercentageValue(46.9, "w", app), PercentageValue(85.9, "h", app))

        # Music bar;
        emptyMusicBar = qtw.QFrame(self)
        emptyMusicBar.setFixedSize(PercentageValue(40, "w", app), PercentageValue(2, "h", app))
        emptyMusicBar.setStyleSheet(f"border-radius: 10; background-color: white;")
        emptyMusicBar.move(PercentageValue(30, "w", app), PercentageValue(88.5, 'h', app))

        # Filler music Bar;
        self.musicColorBar = qtw.QFrame(self)
        self.musicColorBar.setFixedSize(PercentageValue(1, "w", app), PercentageValue(2, "h", app))
        self.musicColorBar.setStyleSheet(f"border-radius: 10; background-color: rgb(34, 177, 76);")
        self.musicColorBar.move(PercentageValue(30, "w", app), PercentageValue(88.5, 'h', app))

        # Music slider;
        self.musicSlider = qtw.QSlider(1, self)
        self.musicSlider.setRange(0, 0)
        self.musicSlider.valueChanged.connect(self.changeMusicPos)
        self.musicSlider.setFixedSize(PercentageValue(40, "w", app), PercentageValue(2, "h", app))
        self.musicSlider.setStyleSheet(f"border-radius: 10;")
        self.musicSlider.move(PercentageValue(30, "w", app), PercentageValue(88.5, 'h', app))

        # Previous song button;
        self.previousSongButton = qtw.QLabel("◄", self)
        self.previousSongButton.setFont(qtg.QFont("Arial", PercentageValue(2.9, "w", app)))
        self.previousSongButton.setStyleSheet("color: white;")
        self.previousSongButton.mouseReleaseEvent = self.goToPreviousSongClick
        self.previousSongButton.move(PercentageValue(26, "w", app)+4, PercentageValue(86, 'h', app))

        # Next song button;
        self.nextSongButton = qtw.QLabel("►", self)
        self.nextSongButton.setFont(qtg.QFont("Arial", PercentageValue(2.9, "w", app)))
        self.nextSongButton.setStyleSheet("color: white;")
        self.nextSongButton.mouseReleaseEvent = self.goToNextSongClick
        self.nextSongButton.move(PercentageValue(70, "w", app), PercentageValue(86, 'h', app))

        # Current playing song label;
        self.currentPlayingSongName = qtw.QLabel("                                                                                             ", self)
        self.currentPlayingSongName.setFont(qtg.QFont("Arial", PercentageValue(1, "w", app)))
        self.currentPlayingSongName.setFixedSize(PercentageValue(100, "w", app), PercentageValue(5, "h", app))
        self.currentPlayingSongName.setStyleSheet("color: rgb(34, 177, 76);")
        self.currentPlayingSongName.move(PercentageValue(30, "w", app), PercentageValue(95, "h", app))

        # Pause Button;
        self.pauseButton = qtw.QPushButton("⏸", self, clicked=lambda:self.pauseOrPlayF())
        self.pauseButton.setFixedSize(PercentageValue(4.9, "h", app), PercentageValue(4.9, "h", app))
        self.pauseButton.setFont(qtg.QFont("Arial", PercentageValue(2, "w", app)))
        self.pauseButton.move(PercentageValue(47, "w", app), PercentageValue(91, "h", app))

        # Logout Button;
        logoutButton = qtw.QPushButton("Logout", self, clicked=lambda:self.logoutF())
        logoutButton.setFixedSize(PercentageValue(8, "w", app), PercentageValue(4, "h", app))
        logoutButton.setFont(qtg.QFont("Arial", PercentageValue(1, "w", app)))
        logoutButton.move(PercentageValue(0.9, "w", app)-2, PercentageValue(95, "h", app))


        # Loading the user data from the json file;
        self.loadPersonalDataf()

        # creating the song timer;
        self.timer = pyqtTimer(self)
        self.timer.setObjectName("musicTimer")
        self.timer.timeout.connect(self.incSongTime)

        # Appending all the songs to the self.allSongs array;
        self.loadAllSongs()
        # Creating all the songs frames/info's now;
        # How its gonna be done #
            # Each frame will always have a static width
            # We will create x grid by the amount of static width's we can create in the self.songsLocation GroupBox
        self.renderAllSongs()
        


    # Loops through all the mp3 files in the music folder and appends them to the self.allSongs array;
    def loadAllSongs(self):
        self.allSongs = []
        for file in os.listdir("./Music"):
            if file.endswith(".mp3"):
                self.allSongs.append(file)
            
    # Loops through the songs on the self.allSongs array, based of a given static width, creates a proper grid;
    def renderAllSongs(self):
        songStaticWidth = 400
        xVal = int(self.songsLocation.width()/songStaticWidth)
        x = 0
        y = 0

        for i in range(len(self.allSongs)):
            if x >= xVal:
                x = 0
                y += 1
            songButton = qtw.QPushButton(f"{self.allSongs[i]}", clicked=lambda ignore, a=i: self.buttonSongPlay(a))
            songButton.setFixedSize(songStaticWidth, 100)
            songButton.setFont(qtg.QFont("Arial", PercentageValue(0.9, "w", app)))
            songButton.setStyleSheet("""
                        background-color: rgb(163, 73, 164);
                        border: 2px solid white;
                        color: white;
                        border-radius: 25;
                    """)
            self.songsButtons.append(songButton)
            self.SongsGrid.addWidget(songButton, y, x)
            x+=1
    
    def buttonSongPlay(self, callerIndex):
        self.songsButtons[self.currentSongIndex].setStyleSheet("""
                        background-color: rgb(163, 73, 164);
                        border: 2px solid white;
                        color: white;
                        border-radius: 25;
                    """)
        self.playSongF(callerIndex)


    def playSongF(self, songIndex):
        self.timer.start(1000)
        # Some clearings;
        self.musicSlider.setSliderPosition(0)
        self.musicColorBar.setFixedSize(0, PercentageValue(2, "h", app))
        self.currentSongTimeState = 0

        self.currentSongIndex = songIndex # Setting the current song index;
        curPlayingSongData = MP3(f"./Music/{self.allSongs[songIndex]}")
        self.currentSongLength = int(curPlayingSongData.info.length) # Setting the current song length;
        self.musicTimer.setText(f"0 - {self.currentSongLength}") # Setting the song timer text;
        self.currentPlayingSongName.setText(f"Playing: {self.allSongs[songIndex]}") # Setting the current playing song text;
        self.songsButtons[songIndex].setStyleSheet("background-color: rgb(213, 123, 214); color: white; border-radius: 25;") # Refreshing the old song button;
        self.musicSlider.setRange(0, self.currentSongLength) # Setting the slider range max to the current song length

        # Starting the song
        pygame.mixer.music.load(f"./Music/{self.allSongs[songIndex]}")
        pygame.mixer.music.play()


    def incSongTime(self):
        if self.currentSongTimeState >= self.currentSongLength:
            self.goToNextSongClick(None)
        else:
            self.currentSongTimeState+=1
            self.musicTimer.setText(f"{self.currentSongTimeState} - {self.currentSongLength}")
            self.updateColorBar()

    # Clickedd from the previous song label;
    # Starts playing the previous index song of the current song;
    def goToPreviousSongClick(self, btnClick):
        if self.currentSongIndex > 0:
            self.songsButtons[self.currentSongIndex].setStyleSheet("background-color: rgb(163, 73, 164); color: white; color: white; border-radius: 25;border: 2px solid white;")
            self.playSongF(self.currentSongIndex-1)


    # Clickedd from the next song label;
    # Starts playing the next index song of the current song;
    def goToNextSongClick(self, btnClick):
        if self.currentSongIndex < len(self.allSongs)-1:
            self.songsButtons[self.currentSongIndex].setStyleSheet("background-color: rgb(163, 73, 164); color: white; color: white; border-radius: 25;border: 2px solid white;")
            self.playSongF(self.currentSongIndex+1)
        
    # Sets the music position when the music slider is moved;
    def changeMusicPos(self, posVal):
        if posVal == 0:
            posVal = 1
        self.currentSongTimeState = posVal
        self.musicTimer.setText(f"{posVal} - {self.currentSongLength}")
        pygame.mixer.music.set_pos(self.currentSongTimeState)
        self.updateColorBar()

    def updateColorBar(self):
        w = PercentageValue(40, "w", app)
        p = (self.currentSongTimeState/self.currentSongLength)*100
        self.musicColorBar.setFixedSize((p/100)*w, PercentageValue(2, "h", app))
        
    def pauseOrPlayF(self):
        if self.pauseButton.text() == "⏸":
            self.timer.stop()
            pygame.mixer.music.pause()
            self.pauseButton.setText("►")
        else:
            self.timer.start()
            pygame.mixer.music.unpause()
            self.pauseButton.setText("⏸")
    
    def loadPersonalDataf(self):
        with open("./Data/userData.json", "r") as udLoader:
            userData = json.load(udLoader)
        self.bioTextArea.setText(userData["userData"]["bio"])
        self.usernameText.setText(userData["userData"]["username"])

    def editBioF(self):
        with open("./Data/userData.json", "r") as udLoader:
            userData = json.load(udLoader)
            userData["userData"]["bio"] = self.bioTextArea.toPlainText()
        with open("./Data/userData.json", "w") as uwriter:
            json.dump(userData, uwriter, indent=4)
    
    def logoutF(self):
        with open("./Data/userData.json", "r") as udLoader:
            userData = json.load(udLoader)
            userData["userData"]["username"] = ""
            userData["userData"]["password"] = ""
            userData["userData"]["bio"] = ""
            userData["loggedIn"] = False
        with open("./Data/userData.json", "w") as uwriter:
            json.dump(userData, uwriter, indent=4)
        lgs = LoginPage()
        appStack.addWidget(lgs)
        appStack.setCurrentIndex(appStack.currentIndex()+1)




# Reads the app data and see's if the user is already logged in;
# If the user is logged in returns True, otherwise, returns False;
def checkIfLoggedF():
    # Getting the user data;
    with open("./Data/userData.json", "r") as ud:
        userData = json.load(ud)
    if userData["loggedIn"]:
        return True
    else:
        return False






if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    appStack = qtw.QStackedWidget()
    # Setting some basic appstack data
    appStack.setWindowTitle("Adak Music Player")



    # If True, sends to the homepage, else, sends to the LoginPage
    if checkIfLoggedF():
        hp = HomePage()
        appStack.addWidget(hp)
    else:
        lp = LoginPage()
        appStack.addWidget(lp)
    # Rendering the stack
    appStack.showFullScreen()


    app.exec_()



