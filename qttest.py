import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QMessageBox, QPushButton, QApplication, QDesktopWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox,  QPlainTextEdit, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSlot
import numpy as np
import cv2
from compare2set import compare2set



class CardReader(QWidget):
    
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def closeEvent(self, event):
        #Handles qutting when using the top-right X
        reply = QMessageBox.question(self, 'Quitting',
            "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  
            
    def keyPressEvent(self, event):
        key = event.key()
        print(key)
    
        if key == Qt.Key_Space:
            print('Left Arrow Pressed')
        
    def center(self):
        #Function to center the window
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    
    
    ## Set Up Main UI
    
    def initUI(self):
        global compareset
        compareset = []
        
        ##Functions
        
        def addtotext(num):
            print('Adding to textbox')
            matchname = name_match_lab.text()
            #curr_text = 
            textline = str(num)+' '+matchname
            textbox.appendPlainText(textline)
            QApplication.processEvents()
        
        def read_match(c2s,cvim):
            print('Reading and Matching')
            name_match_lab.setText('Matching...')
            img_match_lab.setPixmap(blank)
            readbtn.setEnabled(False)
            setselect.setEnabled(False)
            add1btn.setEnabled(False)
            add4btn.setEnabled(False)
            add10btn.setEnabled(False)
            QApplication.processEvents()
            (matchname,matchcvimage) = c2s.compareimg(cvim)
            matchimage = cvimg2qpixmap(matchcvimage)
            name_match_lab.setText(matchname)
            img_match_lab.setPixmap(matchimage)
            readbtn.setEnabled(True)
            setselect.setEnabled(True)
            add1btn.setEnabled(True)
            add4btn.setEnabled(True)
            add10btn.setEnabled(True)
            QApplication.processEvents()
            
        def switchset(text):
            global compareset
            print('Switching to Set: ',text)
            name_match_lab.setText('Loading Set {}'.format(text))
            img_match_lab.setPixmap(blank)
            readbtn.setEnabled(False)
            setselect.setEnabled(False)
            add1btn.setEnabled(False)
            add4btn.setEnabled(False)
            add10btn.setEnabled(False)
            QApplication.processEvents()
            start = setselect.findText('None', Qt.MatchFixedString)
            if start != -1:
                setselect.removeItem(start)
            compareset = compare2set(text)
            name_match_lab.setText('Ready')
            readbtn.setEnabled(True)
            setselect.setEnabled(True)
            QApplication.processEvents()

        def cvimg2qpixmap(cvimg):
            cvimgRGB = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
            qpiximg = QPixmap(QImage(cvimgRGB, cvimgRGB.shape[1], cvimgRGB.shape[0], cvimgRGB.shape[1] * 3,QImage.Format_RGB888))
            return qpiximg
            
        def updateWC(cvimg):
            pixmapimg = cvimg2qpixmap(cvimg)
            imgwindow.setPixmap(pixmapimg)
            imgwindow.update()
            QApplication.processEvents()
            
            #Set Tooltip Font
            QToolTip.setFont(QFont('SansSerif', 10))
            
        def copytext():
            textbox.selectAll()
            textbox.copy()
            textboxcursor.clearSelection()
            textbox.setTextCursor(textboxcursor)
            
        def pastetext():
            textbox.paste()
        
        def cleartext():
            textbox.clear()
        
        ##Widgets
        
        #Main Window
        grid = QGridLayout()
        self.setLayout(grid)
        self.center()
        self.setWindowTitle('MTG Card Reader')
        self.setWindowIcon(QIcon('MTG Blue.ico'))
        
        #Set Seclection Drop Down Menu
        setselectlab = QLabel(self)
        setselectlab.setText('Set:')
        setselectlab.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(setselectlab, 1,1)
        
        setselect = QComboBox(self)
        setselect.addItem('None')
        sets = {'MM3','IMA','MM2'}
        for set in sets:
            setselect.addItem(set)
        setselect.activated[str].connect(switchset)
        grid.addWidget(setselect, 1,2)
        
        #Read Button
        readbtn = QPushButton('Read', self)
        readbtn.setToolTip('Press when your card is in the frame')
        #readbtn.resize(readbtn.sizeHint())
        readbtn.clicked.connect(lambda:read_match(compareset,cvframe))
        readbtn.setEnabled(False)
        readbtn.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        grid.addWidget(readbtn, 2,1)
        readbtn.setDefault(True)
        
        #Image Window
        imgwindow = QLabel(self)
        grid.addWidget(imgwindow, 2,2)
        
        ##Card Info Vert
        
        cardinfov = QVBoxLayout()
        grid.addLayout(cardinfov, 1,3,2,1)
         
        #Add 1 to Text Button
        add1btn = QPushButton('Add 1', self)
        add1btn.setToolTip('Press to add this card to the text box')
        #add1btn.resize(readbtn.sizeHint())
        add1btn.clicked.connect(lambda:addtotext(1))
        add1btn.setEnabled(False)
        add1btn.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        cardinfov.addWidget(add1btn)
        add1btn.setDefault(True)
        
        #Add 4 to Text Button
        add4btn = QPushButton('Add 4', self)
        add4btn.setToolTip('Press to add 4 of this card to the text box')
        #add4btn.resize(readbtn.sizeHint())
        add4btn.clicked.connect(lambda:addtotext(4))
        add4btn.setEnabled(False)
        add4btn.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        cardinfov.addWidget(add4btn)
        add4btn.setDefault(True)
        
        #Add 10 to Text Button
        add10btn = QPushButton('Add 10', self)
        add10btn.setToolTip('Press to add 10 of this card to the text box')
        #add10btn.resize(readbtn.sizeHint())
        add10btn.clicked.connect(lambda:addtotext(10))
        add10btn.setEnabled(False)
        add10btn.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        cardinfov.addWidget(add10btn)
        add10btn.setDefault(True)
         
        #Name of Matched Card
        name_match_lab = QLabel(self)
        name_match_lab.setText('Select a Set Above')
        cardinfov.addWidget(name_match_lab)
        
        #Image of Matched Card
        img_match_lab = QLabel(self)
        blankcv = cv2.imread('blank.png')
        blank = cvimg2qpixmap(blankcv)
        img_match_lab.setPixmap(blank)
        cardinfov.addWidget(img_match_lab)
        
        ##Text Vert
        
        textv = QVBoxLayout()
        grid.addLayout(textv, 1,4,2,1)
        
        #Text Area
        textbox = QPlainTextEdit(self)
        textboxcursor = textbox.textCursor()
        textv.addWidget(textbox)
        
        textopth = QHBoxLayout()
        textv.addLayout(textopth)
        
        #Copy Button
        copybtn = QPushButton('Copy', self)
        copybtn.setToolTip('Copy contents of text box to clipboard')
        copybtn.clicked.connect(copytext)
        copybtn.setEnabled(True)
        textopth.addWidget(copybtn)
        copybtn.setDefault(True)
        #Paste Button
        pastebtn = QPushButton('Paste', self)
        pastebtn.setToolTip('Paste contents of clipboard to text box')
        pastebtn.clicked.connect(pastetext)
        pastebtn.setEnabled(True)
        textopth.addWidget(pastebtn)
        pastebtn.setDefault(True)
        #Clear Button
        clearbtn = QPushButton('Clear', self)
        clearbtn.setToolTip('clears contents of text box')
        clearbtn.clicked.connect(cleartext)
        clearbtn.setEnabled(True)
        textopth.addWidget(clearbtn)
        clearbtn.setDefault(True)
        
        # #Quit Button
        # qbtn = QPushButton('Quit', self)
        # qbtn.clicked.connect(QApplication.instance().quit)
        # #qbtn.resize(qbtn.sizeHint())
        # grid.addWidget(qbtn, 1,4)
        
        #Begin Video Capture
        
        ##Main Camera Loop
        
        try:
            cap = cv2.VideoCapture(0)
            ret, cvframe = cap.read()
            updateWC(cvframe)
        except:
            raise IOError('Webcam or Image Error')
        #wc_height, wc_width, _ = cvframe.shape
        self.center()
        self.show()
        while ret:
            updateWC(cvframe)
            ret,cvframe=cap.read()
    
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    cr = CardReader()
    sys.exit(app.exec_())