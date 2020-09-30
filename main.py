from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os,os.path
from PyQt5.uic import loadUiType
import urllib.request as ur
import pafy
import humanize

ui,_=loadUiType('main.ui')

class MainApp(QMainWindow,ui):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handel_Buttons()
        self.Dark_Blue_Theme()

    def InitUI(self):
        # Contain all Change in Ui Change In loading
        self.tabWidget.tabBar().setVisible(False)
        self.Move_Box_1()
        self.Move_Box_2()
        self.Move_Box_3()
        self.Move_Box_4()


    def Handel_Buttons(self):
        # Handel all the buttons in app
        self.pushButton_2.clicked.connect(self.Download)
        self.pushButton.clicked.connect(self.Handel_Browse)
        self.pushButton_4.clicked.connect(self.Get_Video_Data)
        self.pushButton_5.clicked.connect(self.Handel_Browse1)
        self.pushButton_3.clicked.connect(self.Download_Video)

        self.pushButton_7.clicked.connect(self.Playlist_Download)
        self.pushButton_6.clicked.connect(self.Playlist_Save_Browse)

        self.pushButton_8.clicked.connect(self.Open_Home)
        self.pushButton_9.clicked.connect(self.Open_Download)
        self.pushButton_10.clicked.connect(self.Open_Youtube)
        self.pushButton_11.clicked.connect(self.Open_Settings)

        self.pushButton_12.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_13.clicked.connect(self.Dark_Gray_Theme)
        self.pushButton_14.clicked.connect(self.Dark_Orange_Theme)
        self.pushButton_15.clicked.connect(self.Q_Dark_Theme)

    def Handel_Progress(self,blocknum,blocksize,totalsize):
        # Handel Progress Bar
        read_data=blocknum*blocksize

        if totalsize>0:
            download_percentage=read_data*100/totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()
            


    def Handel_Browse(self):
        # Enable Browse Button to open browse button
        save_location=QFileDialog.getSaveFileName(self,caption="Save as",directory=".",filter="All Files(*.*)")
        self.lineEdit_2.setText(save_location[0])

    def Download(self):
        # Download any file
        downlaod_url=self.lineEdit.text()
        save_location=self.lineEdit_2.text()
        
        if downlaod_url=='':
            QMessageBox.warning(self,"Warning","Please Provide Url Link")
        elif save_location=="":
            QMessageBox.warning(self,"Warning","Please Provide download location")
        else:
            try:
                ur.urlretrieve(downlaod_url,save_location,self.Handel_Progress)
                QMessageBox.information(self,"Downlaod Successfully!","Your Download is Completed Successfully!!")
                self.lineEdit.setText("")
                self.lineEdit_2.setText("")
                self.progressBar.setValue(0)
            except Exception:
                QMessageBox.warning(self,"Warning","Please Provide Url Link or Download Location")
            
    ##################################### Youtube Video Download ##################################################

    def Handel_Browse1(self):
        # Enable Browse Button to open browse button
        save_location=QFileDialog.getSaveFileName(self,caption="Save as",directory=".",filter="All Files(*.*)")
        self.lineEdit_4.setText(save_location[0])

    def Get_Video_Data(self):
        video_url=self.lineEdit_3.text()

        if video_url=="":
            QMessageBox.warning(self,"Warning","Please Provide Youtube Link")
        else:
            try:
                video=pafy.new(video_url)
                video_streams=video.allstreams
                for stream in video_streams:
                    size=humanize.naturalsize(stream.get_filesize())
                    data="{} {} {} - {}".format(stream.mediatype,stream.extension,stream.quality,size)
                    self.comboBox.addItem(data)
            except Exception:
                QMessageBox.warning(self,"Warning","Please Provide Url Link")

                
    def Download_Video(self):
        video_url=self.lineEdit_3.text()
        save_location=self.lineEdit_4.text()
        if video_url=="":
            QMessageBox.warning(self,"Warning","Please Provide Youtube Link")
        elif save_location=="":
            QMessageBox.warning(self,"Warning","Please Provide Valid Location")
        else:
            video=pafy.new(video_url)
            video_stream=video.videostreams
            video_quality=self.comboBox.currentIndex()
            download=video_stream[video_quality].download(filepath=save_location,callback=self.Video_Progress)

    def Video_Progress(self,total,received,ratio,rate,time):
        read_data=received
        if total>0:
            download_percentage=(read_data*100)/total
            self.progressBar_2.setValue(download_percentage)
            remaining_time=round(time/60,2)

            self.label_5.setText(str("{} minute Remaining".format(remaining_time)))
            QApplication.processEvents()
    ##################################### Youtube Playlist Download ##################################################
    def Playlist_Save_Browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self , "Select Download Directory")
        self.lineEdit_6.setText(playlist_save_location)

    def Playlist_Download(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        if playlist_url == '' or save_location == '' :
            QMessageBox.warning(self, "Data Error", "Provide a valid Playlist URL or save location")

        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))


        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))

        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.comboBox_2.currentIndex()


        QApplication.processEvents()

        for video in playlist_videos :
            current_video = video['pafy']
            current_video_stream = current_video.videostreams
            self.lcdNumber.display(current_video_in_download)
            download = current_video_stream[quality].download(callback=self.Playlist_Progress)
            QApplication.processEvents()

            current_video_in_download +=1

    def Playlist_Progress(self , total , received , ratio , rate , time):
        read_data = received
        if total > 0 :
            download_percentage = read_data * 100 / total
            self.progressBar_3.setValue(download_percentage)
            remaining_time = round(time/60 , 2)

            self.label_6.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()
    
    ################################################
    ###### UI CHanges Methods
    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Youtube(self):
        self.tabWidget.setCurrentIndex(2)


    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(3)

    ############################ Theme Section ############################################
    def Dark_Blue_Theme(self):
        style=open("Theme/dark_blue.css",'r')
        style=style.read()
        self.setStyleSheet(style)
    def Dark_Orange_Theme(self):
        style = open("Theme/dark_orange.css", 'r')
        style = style.read()
        self.setStyleSheet(style)
    def Dark_Gray_Theme(self):
        style = open("Theme/dark_gray.css", 'r')
        style = style.read()
        self.setStyleSheet(style)
    def Q_Dark_Theme(self):
        style = open("Theme/qdark.css", 'r')
        style = style.read()
        self.setStyleSheet(style)
    
    ##########################################
    ####### App Animation

    def Move_Box_1(self):
        box_animation1 = QPropertyAnimation(self.groupBox , b"geometry")
        box_animation1.setDuration(2500)
        box_animation1.setStartValue(QRect(0,0,0,0))
        box_animation1.setEndValue(QRect(40,80,331,171))
        box_animation1.start()
        self.box_animation1 = box_animation1


    def Move_Box_2(self):
        box_animation2 = QPropertyAnimation(self.groupBox_2 , b"geometry")
        box_animation2.setDuration(2500)
        box_animation2.setStartValue(QRect(0,0,0,0))
        box_animation2.setEndValue(QRect(430,80,331,171))
        box_animation2.start()
        self.box_animation2 = box_animation2


    def Move_Box_3(self):
        box_animation3 = QPropertyAnimation(self.groupBox_3 , b"geometry")
        box_animation3.setDuration(2500)
        box_animation3.setStartValue(QRect(0,0,0,0))
        box_animation3.setEndValue(QRect(40,270,331,171))
        box_animation3.start()
        self.box_animation3 = box_animation3


    def Move_Box_4(self):
        box_animation4 = QPropertyAnimation(self.groupBox_4 , b"geometry")
        box_animation4.setDuration(2500)
        box_animation4.setStartValue(QRect(0,0,0,0))
        box_animation4.setEndValue(QRect(430,270,331,171))
        box_animation4.start()
        self.box_animation4 = box_animation4

def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()