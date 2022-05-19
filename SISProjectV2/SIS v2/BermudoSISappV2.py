#UREL VAN WILLIAM BERMUDO BSCS, 2ND YEAR, CCC151, SIS V2 HOMEWORK

import mysql
import mysql.connector
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem, QHeaderView, QErrorMessage, QPushButton, QHBoxLayout, QMessageBox
from PyQt5 import uic, QtCore



#cursor for manipulating database
db = mysql.connector.connect(host = 'localhost', user = 'root', password = '*P@ssw0rd', database = 'student information system')
mydb = db.cursor()

#MYSQL QUERIES

# mydb.execute(f"Select * FROM student WHERE courseId IS NULL ") 
# row = mydb.fetchone() 
# print(row) 




def checkCodeDup(courseCode, rowNo = None):     #course code duplication check
    if rowNo == None:             #if row is none, it is adding, not editing
        mydb.execute(f"Select rowNo, COUNT(rowNo) as cnt FROM  courses WHERE courseId = '{courseCode}'")
        row = mydb.fetchone() 
        row = row[1] 
        if (row):                
            return True 

    if rowNo != None:
        mydb.execute(f"Select rowNo, COUNT(rowNo) as cnt FROM courses WHERE courseId = '{courseCode}' and rowNo != {rowNo}") 
        row = mydb.fetchone() 
        row = row[1]
        if (row):                
            return True 

def checkIdDup(idnumber, rowNo = None):
    if rowNo == None:             #if row is none, it is adding, not editing
        mydb.execute(f"Select idNo, COUNT(IdNo) as cnt FROM student WHERE idNo = '{idnumber}'")
        row = mydb.fetchone() 
        row = row[1] 
        if (row):                
            return True 

    if rowNo != None:
        mydb.execute(f"Select idNo, COUNT(IdNo) as cnt FROM student WHERE idNo = '{idnumber}' and rowNo != {rowNo}") 
        row = mydb.fetchone() 
        row = row[1]
        if (row):                

            return True 

def getCRow(row):
    mydb.execute(f"SELECT * FROM courses WHERE rowNo = {row}")
    row = mydb.fetchone()
    return row

def getRow(row):
    mydb.execute(f"SELECT * FROM STUDENT WHERE rowNo = {row}")
    row = mydb.fetchone()
    return row

def updateCRow(row,courseCode,courseName):     
    if(checkCodeDup(courseCode, row)):
        return False
    mydb.execute(f"UPDATE courses SET courseId = '{courseCode}',courseName = '{courseName}'  WHERE rowNo = {row}")
    db.commit()

def updateRow(row,idNo,fullName,yearLevel,gender,course):    
    if(checkIdDup(idNo, row)):
        return False
    mydb.execute(f"UPDATE STUDENT SET fullName = '{fullName}', idNo = '{idNo}', yearLevel = '{yearLevel}', gender = '{gender}', courseCode = '{course}'  WHERE rowNo = {row}")
    db.commit()


def addRow(idNo,fullName,yearLevel,gender,course):
    if(checkIdDup(idNo)):
        return False
    mydb.execute(f"INSERT INTO STUDENT VALUES(NULL,'{idNo}','{fullName}',{yearLevel},'{gender}','{course}');")
    db.commit()

def addCRow(courseCode, courseName):
    if(checkCodeDup(courseCode)):
        return False
    mydb.execute(f"INSERT INTO courses VALUES('{courseCode}','{courseName}',NULL);")
    db.commit()


def deleteRow(row):
    mydb.execute(f"DELETE FROM STUDENT WHERE rowNo = {row}")
    db.commit() 


def deleteCRow(row):
    mydb.execute(f"DELETE FROM courses WHERE rowNo = {row}")
    db.commit() 


def getCourseName(courseCode):
    mydb.execute(f"SELECT courseName FROM courses WHERE courseId = '{courseCode}'")
    row = mydb.fetchone()
    return row[0]


def getCourseCode(text):
    text = text.split(' ')
    text = text[0]
    return text




# credits https://www.reddit.com/r/learnpython/comments/69vm4t/pyqt5_and_high_resolution_monitors/ 
# to fix gui not displaying properly on different resolutions
QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) 


class EDITcourse(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{sys.path[0]}/editcourse.ui', self)
        self.error_dialog = QErrorMessage()
        self.error_dialog.setWindowTitle('Error')
        self.doneEdit.pressed.connect(self.editData)
        self.chosenRow = None
    
    def editData(self):  
        reply = QMessageBox.question(self, 'Confirmation', 'Save edit changes?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            pass
        else:
            self.close()
            return

        courseCode = (self.codeField.text()).upper()       
        if (checkCodeDup(courseCode) == False):
            self.error_dialog.showMessage('Invalid ID Number format!')
            return

        courseName = (self.courseField.text()).title()
        if (courseName == ''):
            self.error_dialog.showMessage('Name field cannot be blank!')
            return

        if(updateCRow(self.chosenRow, courseCode, courseName) == False):
            self.error_dialog.showMessage('Course Code currently in use by another course!')
            return

        self.close()   
        mygui.refresh2()
    


class ADDcourse(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{sys.path[0]}/addcourse.ui', self)
        self.error_dialog = QErrorMessage()
        self.error_dialog.setWindowTitle('Error')
        self.doneAdd.pressed.connect(self.getData)
        self.chosenRow = None


    def getData(self):
        courseCode = self.codeField.text().upper()  
        if(courseCode == ''):
            self.error_dialog.showMessage('Course Code field cannot be blank!')
            return

        courseName = (self.courseField.text()).title()
        if (courseName == ''):
            self.error_dialog.showMessage('Course Name field cannot be blank!')
            return
        
        if(addCRow(courseCode, courseName) == False):
            self.error_dialog.showMessage('Course Code is already in use!')
            return 


        self.doneAdd.setEnabled(False)
        self.close()
        self.codeField.clear()
        self.courseField.clear()
        mygui.refresh2()


class EDITform(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{sys.path[0]}/editwindow.ui', self)
        self.error_dialog = QErrorMessage()
        self.error_dialog.setWindowTitle('Error')
        self.doneEdit.pressed.connect(self.editData)
        self.chosenRow = None


    def editData(self):  
        reply = QMessageBox.question(self, 'Confirmation', 'Save edit changes?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            pass
        else:
            self.close()
            return

        idNumber = self.idField.text()            
        if (self.checkIDformat(idNumber) == False):
            self.error_dialog.showMessage('Invalid ID Number format!')
            return

        fullName = (self.nameField.text()).title()
        if (fullName == ''):
            self.error_dialog.showMessage('Name field cannot be blank!')
            return

        course = getCourseCode(self.courseField.currentText()) 

        year = self.yearField.currentText() 
        gender = self.genderField.currentText() 
        if(updateRow(self.chosenRow, idNumber, fullName, year, gender, course) == False):
            self.error_dialog.showMessage('ID Number is currently in use by another student.')
            return

        self.close()    
        mygui.refresh()


    def checkIDformat(self, idNumber):
        if len(idNumber)!= 9:
            return False
        for i in range(len(idNumber)):
            if i != 4:
                try:
                    int(idNumber[i])
                except:
                    return False
            if i == 4:
                if idNumber[i] != '-':
                    return False
        return True


class ADDform(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{sys.path[0]}/addwindow.ui', self)
        self.error_dialog = QErrorMessage()
        self.error_dialog.setWindowTitle('Error')
        self.doneAdd.pressed.connect(self.getData)
    

    def getData(self):
        idNumber = self.idField.text()            
        if (self.checkIDformat(idNumber) == False):
            self.error_dialog.showMessage('Invalid ID Number format!')
            return

        fullName = (self.nameField.text()).title()
        if (fullName == ''):
            self.error_dialog.showMessage('Name field cannot be blank!')
            return

        course = getCourseCode(self.courseField.currentText())

        year = self.yearField.currentText()
        gender = self.genderField.currentText()
        
        if(addRow(idNumber, fullName, year, gender, course) == False):
            self.error_dialog.showMessage('ID Number is already in use by another student!')
            return


        self.doneAdd.setEnabled(False)
        self.close()
        self.idField.clear()
        self.nameField.clear()
        mygui.refresh()
    

    def checkIDformat(self, idNumber):
        if len(idNumber)!= 9:
            return False
        for i in range(len(idNumber)):
            if i != 4:
                try:
                    int(idNumber[i])
                except:
                    return False
            if( (i == 4) and (idNumber[i] != '-')):
                    return False
        return True



class SISgui(QMainWindow):  


    def __init__(self):
        super().__init__()
        uic.loadUi(f'{sys.path[0]}/mainwindow.ui', self)
        self.addButton2.pressed.connect(self.openAddCourse)
        self.addButton.pressed.connect(self.openAddWindow)       #connecting buttons to function
        self.searchButton.pressed.connect(self.findStudent)            
        self.searchButton2.pressed.connect(self.findCourse)             
        self.showButton.pressed.connect(self.refresh)
        self.showButton2.pressed.connect(self.refresh2)
        self.headerLabels =['ID Number','Full Name','Year Level','Gender','Course Code','Action']
        self.headerLabels2 = ['Course Code', 'Full Course Name', 'Action']
        
        # error message object
        self.error_dialog = QErrorMessage()
        self.error_dialog.setWindowTitle('Error')

        #adds student and edit student window initialize
        self.window2 = ADDform() 
        self.window3 = EDITform() 
        self.window4 = ADDcourse()
        self.window5 = EDITcourse()
        self.comboItems = []
        self.setComboBox()        
        self.refresh()
        self.refresh2()


    def openEditCourse(self,row):
        data = getCRow(row)
        int(row)
        self.window5.chosenRow = row
        self.window5.doneEdit.setEnabled(True) # preventing double clicking
        self.window5.codeField.setText(data[0])
        self.window5.courseField.setText(data[1])
        self.window5.show()
    
    def openEditWindow(self,row): 
        data = getRow(row)
        int(row)
        self.window3.chosenRow = row
        self.window3.doneEdit.setEnabled(True) # preventing double clicking 
        self.window3.idField.setText(data[1]) 
        self.window3.nameField.setText(data[2])
        self.window3.yearField.setCurrentText(str(data[3])) 
        self.window3.genderField.setCurrentText(str(data[4])) 
        self.window3.courseField.setCurrentIndex(self.getComboBoxIndex(data[5])) 
        self.window3.show() 


    def openAddWindow(self):
        self.window2.doneAdd.setEnabled(True) # preventing double clicking
        self.window2.show()
    
    def openAddCourse(self):
        self.window4.doneAdd.setEnabled(True) # preventing double clicking
        self.window4.show()


        # method for making the delete and edit buttons that will be used for each row
    def makeButtons(self, row):                          # yoinked from https://stackoverflow.com/questions/60396536/pyqt5-setcellwidget-on-qtablewidget-slows-down-ui
        self.editButton = QPushButton('Edit')
        self.editButton.pressed.connect(lambda:self.openEditWindow(row))
    

        self.deleteStudentButton = QPushButton('Delete')
        self.deleteStudentButton.pressed.connect(lambda:self.deleteStudent(row))

        self.actionLayout = QHBoxLayout()
        self.actionLayout.addWidget(self.deleteStudentButton,5)
        self.actionLayout.addWidget(self.editButton,5)
        self.actionWidget = QWidget()
        self.actionWidget.setLayout(self.actionLayout)
        return self.actionWidget

    def makeButtons2(self, row):                          # yoinked from https://stackoverflow.com/questions/60396536/pyqt5-setcellwidget-on-qtablewidget-slows-down-ui
        self.editButton = QPushButton('Edit')
        self.editButton.pressed.connect(lambda:self.openEditCourse(row))
    

        self.deleteStudentButton = QPushButton('Delete')
        self.deleteStudentButton.pressed.connect(lambda:self.deleteCourse(row))

        self.actionLayout = QHBoxLayout()
        self.actionLayout.addWidget(self.deleteStudentButton,5)
        self.actionLayout.addWidget(self.editButton,5)
        self.actionWidget = QWidget()
        self.actionWidget.setLayout(self.actionLayout)
        return self.actionWidget


    def deleteStudent(self, row):
        student = getRow(row)
        reply = QMessageBox.question(self, student[1], 'Are you sure you want to delete this student?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            deleteRow(row)
            self.refresh()
        else:
            pass

    def deleteCourse(self, row):
        course = getCRow(row)
        reply = QMessageBox.question(self, course[1], 'Are you sure you want to delete this course?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            deleteCRow(row)
            self.refresh2()
        else:
            pass
        


    def clear_table(self):
        while(self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)


    def refresh(self):
        self.clear_table
        self.displayData()
        


    def displayData(self):                                      #yoinked the code from https://www.youtube.com/watch?v=HDjc3w1W9oA
        hheader = self.tableWidget.horizontalHeader()           #stole this from https://www.tutorialexample.com/pyqt-table-set-adaptive-width-to-fit-resized-window-a-beginner-guide-pyqt-tutorial/
        hheader.setSectionResizeMode(QHeaderView.Stretch)
        vheader = self.tableWidget.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.Fixed)        # row resize: https://stackoverflow.com/questions/19304653/how-to-set-row-height-of-qtableview
        vheader.setDefaultSectionSize(40)
        
        numColumn = 5
        mydb.execute("SELECT COUNT(*) FROM STUDENT")
        numRows = mydb.fetchone()
        numRows = numRows[0]
        self.tableWidget.setColumnCount(numColumn+1)
        self.tableWidget.setRowCount(numRows)
        self.tableWidget.setHorizontalHeaderLabels(self.headerLabels)
        
        mydb.execute("SELECT rowNo, idNo, fullName, yearLevel, gender, courseCode from STUDENT")
        rows = mydb.fetchall()
        
        for i in range(numRows):
            for j in range(numColumn):
                try:
                    if j == 4:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(getCourseName(rows[i][j+1]))))
                        break
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(rows[i][j+1])))
                except TypeError:
                    self.tableWidget.setItem(i, j, QTableWidgetItem('None'))
                
            actionWidget = self.makeButtons(rows[i][0])
            self.tableWidget.setCellWidget(i, 5, actionWidget)


    def findStudent(self):
        idnumber = self.searchBar.text()

        if(idnumber == ''):
            return

        if(self.checkIDformat(idnumber) == False):
            self.error_dialog.showMessage('Invalid ID Number')
            self.searchBar.clear()
            return

        mydb.execute(f"SELECT rowNo, idNo, fullName, yearLevel, gender, courseCode from STUDENT WHERE idNo = '{idnumber}'")
        row = mydb.fetchone()

        if (row == None):
            self.error_dialog.showMessage('Student with this ID Number does not exist.')
            self.searchBar.clear()
            return

        self.clear_table()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setHorizontalHeaderLabels(self.headerLabels)
        
        for i in range(5):
            try:
                if i == 4:
                    self.tableWidget.setItem(0, i, QTableWidgetItem(str(getCourseName(row[i+1]))))
                    break
                self.tableWidget.setItem(0, i, QTableWidgetItem(str(row[i+1])))
            except TypeError:
                self.tableWidget.setItem(0, i, QTableWidgetItem('None'))
        actionWidget = self.makeButtons(row[0])
        self.tableWidget.setCellWidget(0, 5, actionWidget)
        return True
        
        
    def checkIDformat(self, idNumber):
        if len(idNumber)!= 9:
            return False
        for i in range(len(idNumber)):
            if i != 4:
                try:
                    int(idNumber[i])
                except:
                    return False
            if i == 4:
                if idNumber[i] != '-':
                    return False
        return True
        
    
    def clear_table2(self):
        while(self.tableWidget2.rowCount() > 0):
            self.tableWidget2.removeRow(0)


    def refresh2(self):
        self.clear_table
        self.displayCourse()
        self.setComboBox()


    def displayCourse(self):                                      #yoinked the code from https://www.youtube.com/watch?v=HDjc3w1W9oA
        hheader = self.tableWidget2.horizontalHeader()           #stole this from https://www.tutorialexample.com/pyqt-table-set-adaptive-width-to-fit-resized-window-a-beginner-guide-pyqt-tutorial/
        hheader.setSectionResizeMode(QHeaderView.Stretch)
        vheader = self.tableWidget2.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.Fixed)        # row resize: https://stackoverflow.com/questions/19304653/how-to-set-row-height-of-qtableview
        vheader.setDefaultSectionSize(40)
        
        numColumn = 2
        mydb.execute("SELECT COUNT(*) FROM courses")
        numRows = mydb.fetchone()
        numRows = numRows[0]
        self.tableWidget2.setColumnCount(numColumn+1)   
        self.tableWidget2.setRowCount(numRows)
        self.tableWidget2.setHorizontalHeaderLabels(self.headerLabels2)
        
        mydb.execute("SELECT courseId, courseName, rowNo from courses")
        rows = mydb.fetchall()

        for i in range(numRows): 
            for j in range(numColumn):
                self.tableWidget2.setItem(i, j, QTableWidgetItem(str(rows[i][j]))) 
            actionWidget = self.makeButtons2(rows[i][2]) 
            self.tableWidget2.setCellWidget(i, 2, actionWidget) 
        
    def getComboBoxIndex(self,text):
        if (text == None):
            return 0
        return self.comboItems.index(text)

    def setComboBox(self):
        mydb.execute(f"SELECT courseId FROM courses ORDER BY rowNo;")
        rows = mydb.fetchall()
        for item in rows:
            self.comboItems.append(*item)
        self.window2.courseField.addItems(self.comboItems)
        self.window3.courseField.addItems(self.comboItems)


    def test(self):
        self.window2.courseField.addItems(['TEST'])

    def findCourse(self):
        courseCode = self.searchBar2.text()

        if(courseCode == ''):
            return

        mydb.execute(f"SELECT courseId, courseName, rowNo from courses WHERE courseId = '{courseCode}'")
        row = mydb.fetchone()

        if (row == None):
            self.error_dialog.showMessage('Course with this course code does not exist.') 
            self.searchBar2.clear() 
            return

        self.clear_table2()
        self.tableWidget2.setColumnCount(3)
        self.tableWidget2.setRowCount(1)
        self.tableWidget2.setHorizontalHeaderLabels(self.headerLabels)
        
        for i in range(2):
            self.tableWidget2.setItem(0, i, QTableWidgetItem(str(row[i])))
        actionWidget = self.makeButtons2(row[2])
        self.tableWidget2.setCellWidget(0, 2, actionWidget)
        return True

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mygui = SISgui()
    mygui.show()

    try:
        sys.exit(app.exec_())
    except (SystemExit):
        print("Closing window...")
        mydb.execute("SET @num := 0; UPDATE student SET rowNo = @num := (@num+1); ALTER TABLE student AUTO_INCREMENT=1; SET @num := 0; UPDATE courses SET rowNo = @num := (@num+1); ALTER TABLE student AUTO_INCREMENT=1;") #resets the row numbers 






