import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QGridLayout, QMessageBox, QAction)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import cv2
import math
import numpy as np
import csv
from datetime import datetime
import pathlib

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("TomatoAnalyzer_hsv.ui", self)
        #self.Menubar()
        self.OpenFile.clicked.connect(self.Open_File) #mengaktifkan tombol Pilih Foto
        self.Analisis.clicked.connect(self.Analyse)  #mengaktifkan tombol Analisis
        self.Simpan.clicked.connect(self.Save) #mengaktifkan tombol Save
        self.Keluar.clicked.connect(self.close) #mengaktifkan tombol Exit
        self.activator = 1+1
        #mengatur warna teks label
        self.nilai_red.setStyleSheet("color: white")
        self.nilai_green.setStyleSheet("color: white")
        self.nilai_blue.setStyleSheet("color: white")
        self.nilai_pixel.setStyleSheet("color: white")
        self.nilai_area.setStyleSheet("color: white")
        self.nilai_weight.setStyleSheet("color: white")
        self.nilai_brix.setStyleSheet("color: white")
        self.nilai_hue.setStyleSheet("color: white")
        self.nilai_saturation.setStyleSheet("color: white")
        self.nilai_intensity.setStyleSheet("color: white")

        #Mengaktifkan slider threshold
        self.slider_HMin.sliderMoved.connect(self.Analyse)
        self.slider_HMax.sliderMoved.connect(self.Analyse)
        self.slider_SMin.sliderMoved.connect(self.Analyse)
        self.slider_SMax.sliderMoved.connect(self.Analyse)
        self.slider_VMin.sliderMoved.connect(self.Analyse)
        self.slider_VMax.sliderMoved.connect(self.Analyse)

        #mengaktifkan QSpinbox threshold
        self.H_Min.valueChanged.connect(self.Analyse)
        self.S_Min.valueChanged.connect(self.Analyse)
        self.V_Min.valueChanged.connect(self.Analyse)
        self.H_Max.valueChanged.connect(self.Analyse)
        self.S_Max.valueChanged.connect(self.Analyse)
        self.V_Max.valueChanged.connect(self.Analyse)

        #Menyelaraskan nilai slider dengan nilai Qspinbox
        self.slider_HMin.valueChanged['int'].connect(self.H_Min.setValue)
        self.slider_SMin.valueChanged['int'].connect(self.S_Min.setValue)
        self.slider_VMin.valueChanged['int'].connect(self.V_Min.setValue)
        self.slider_HMax.valueChanged['int'].connect(self.H_Max.setValue)
        self.slider_SMax.valueChanged['int'].connect(self.S_Max.setValue)
        self.slider_VMax.valueChanged['int'].connect(self.V_Max.setValue)

        #Menyelaraskan nilai Qspinbox dengan nilai slider
        self.H_Min.valueChanged['int'].connect(self.slider_HMin.setValue)
        self.S_Min.valueChanged['int'].connect(self.slider_SMin.setValue)
        self.V_Min.valueChanged['int'].connect(self.slider_VMin.setValue)
        self.H_Max.valueChanged['int'].connect(self.slider_HMax.setValue)
        self.S_Max.valueChanged['int'].connect(self.slider_SMax.setValue)
        self.V_Max.valueChanged['int'].connect(self.slider_VMax.setValue)  

        self.FotoAwal.setAlignment(Qt.AlignCenter)
        self.FotoAkhir.setAlignment(Qt.AlignCenter)
        self.FotoThreshold.setAlignment(Qt.AlignCenter)
        self.label_NamaFile.setAlignment(Qt.AlignCenter)

    #membuat/mendefinisikan fungsi yang bernama CloseEvent (dipicu oleh fungsi Close())
    def closeEvent(self, event):
        # Tampilkan dialog konfirmasi keluar ketika tombol Exit ditekan
        self.reply = QMessageBox.question(self, 'Konfirmasi', 'Anda yakin ingin keluar?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if self.reply == QMessageBox.Yes: #jika tombol yes ditekan maka aplikasi akan keluar
            #aplikasi akan keluar jika gambar sudah disimpan
            if self.activator == 10:
                event.accept()
                QApplication.quit()
            elif self.activator != 10:
                if self.activator ==2:
                    event.accept()
                    QApplication.quit()
                elif self.activator == 4:
                    self.Save()
                    event.accept()
                    QApplication.quit()
        else: #jika tombol no ditekan maka aplikasi akan tetap berjalan
            event.ignore() 
          
    #Membuat/mendefinisikan fungsi yang bernama 'Open_File' untuk membuka file citra
    def Open_File(self):
        options = QFileDialog.Options()
        self.FileImage,_ = QFileDialog.getOpenFileName(directory= "./Citra_Asli", caption= "Choose a Picture", 
                                                    filter= "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files ()", options=options)
        self.OriginalImage= cv2.imread(self.FileImage) #membaca file citra yang ingin diolah dan ditampilkan
        cv2.imwrite('./Temp_Save/Citra_Asli.jpg', self.OriginalImage) #menyimpan dan merename file yang ingin diolah dan ditampilkan dengan 
        #pixmap_source = QPixmap(self.OriginalImage) #mengatur Qpixmap dengan file Citra Asli
        self.FotoAwal.setPixmap(QPixmap(self.FileImage)) #Menampilkan Citra Asli pada Qlabel
        self.ImageInsertedCheck = self.FotoAwal.pixmap()
        #Menampilkan nama file citra 
        PathFileImage = pathlib.Path(self.FileImage)
        self.PictureName = PathFileImage.stem
        self.GroupName = self.FileImage.split('/')[-2]
        self.label_NamaFile.setText(f'{self.GroupName} {self.PictureName}')
        self.activator1 = 3+3

    #Membuat/mendefinisikan fungsi yang bernama 'Save'
    def Save(self):
        image_hasil = cv2.imread('./Temp_Save/Citra_Akhir.jpg') #membaca file Citra Hasil
        image_threshold = cv2.imread('./Temp_Save/Citra_Threshold.jpg') #membaca file Citra Threshold
        options = QFileDialog.Options()
        self.filename, _ = QFileDialog.getSaveFileName(directory= "./Citra_Hasil", caption= "Save a Picture", 
                                                    filter= "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files ()", options=options)
        self.saveToCSV(self.PictureName,self.GroupName,self.r,self.g,self.b,self.H,self.S,self.V,self.count)
        if self.filename: #kondisi untuk  menyimpan 2 file secara langsung dengan nama yang berbeda
            cv2.imwrite(self.filename, image_hasil)
            self.filename2 = self.filename[:-4] + "_threshold" + self.filename[-4:] #memotong format file dan menambahkan kata baru
            cv2.imwrite(self.filename2, image_threshold)
        self.activator = 5+5

    def saveToCSV(self, NamaCitra,KelompokCitra,r,g,b,h,s,v,piksel): 
        #memasukkan nilai hasil perhitungan menjadi csv
        timeStamp = datetime.now().strftime("%a-%d-%b-%Y %H-%M-%S")
        header = [
            "Timestamp", "Nama Citra", "Kelompok",
            "Nilai R", "Nilai G", "Nilai B", "Nilai H", "Nilai S", "Nilai V", "Piksel" 
        ]
        file_exists = os.path.exists("./dataPengolahan.csv")
        
        if not file_exists:
            writeHeader = open('dataPengolahan.csv', 'a',newline='')
            writeHeader = csv.writer(writeHeader,quoting=csv.QUOTE_ALL,dialect='excel')
            writeHeader.writerow(header)

        file = open('dataPengolahan.csv', 'a',newline='')
        file = csv.writer(file,quoting=csv.QUOTE_ALL,dialect='excel')
        file.writerow([timeStamp, NamaCitra, KelompokCitra, r,g,b,h,s,v,piksel])

    #Membuat/mendefinisikan fungsi yang bernama 'Analyse'
    def Analyse(self):
        if self.activator1 != 6 :
            WarningMessage = QMessageBox()
            WarningMessage.setIcon(QMessageBox.Warning)
            WarningMessage.setText("Input image first!")
            WarningMessage.setWindowTitle('Error')
            WarningMessage.setStandardButtons(QMessageBox.Retry)
            WarningMessage.exec_()
        else:    
            hMin = sMin = vMin = hMax = sMax = vMax = 0 #set nilai batas bawah dan atas jadi 0
            #phMin = psMin = pvMin = phMax = psMax = pvMax = 0 
            #img = cv2.imread('./Temp_Save/Citra_Asal.jpg', 1) #membaca file Citra ASli
            #output = img
            
            # Mendapatkan nilai dari slider
            hMin = float(self.slider_HMin.sliderPosition())
            sMin = float(self.slider_SMin.sliderPosition())
            vMin = float(self.slider_VMin.sliderPosition())
            hMax = float(self.slider_HMax.sliderPosition())
            sMax = float(self.slider_SMax.sliderPosition())
            vMax = float(self.slider_VMax.sliderPosition())

            #penentuan batas Tresholding 
            lower = np.array([hMin, sMin, vMin]) #batas bawah threshold
            upper = np.array([hMax, sMax, vMax]) #batas atas threshold

            kernel = np.ones((5,5), np.uint8)

            medBl = cv2.medianBlur(self.OriginalImage, 5) #smoothing untuk mereduksi noise
            hsv = cv2.cvtColor(medBl, cv2.COLOR_BGR2HSV) #mengonversi Citra Asli menjadi HSV
            threshold1 = cv2.inRange(hsv, lower, upper) #mengoversi Citra Asli menjadi hitam putih (threshold1)
            threshold2 = cv2.morphologyEx(threshold1, cv2.MORPH_OPEN, kernel)
            manualthreshold = cv2.morphologyEx(threshold2, cv2.MORPH_CLOSE, kernel)
            #menggabungkan Citra Asli dan Citra Threshold
            res = cv2.bitwise_and(self.OriginalImage, self.OriginalImage, mask=manualthreshold)

            self.count = cv2.countNonZero(manualthreshold) #menghitung warna piksel yang tidak hitam atau 0
            #menghitung dan menampilkan nilai luas dan berat
            area = round(0.001*self.count)
            weight = round(0.0038*self.count - 12.064)            
            self.nilai_pixel.setText(f'= {str(self.count)}')
            self.nilai_area.setText(f'= {str(area)} cm2')
            self.nilai_weight.setText(f'= {str(weight)} gr')
                    
            #menghitung masing-masing komoponen BGR
            citra = res
            avg_color_per_row = np.average (citra, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            sum_color_per_row = np.sum(citra, axis=0)
            sum_color = np.sum(sum_color_per_row, axis=0)

            #menyimpan dan menampilkan Citra Threshold dan Citra Hasil
            chasil = res
            cv2.imwrite('./Temp_Save/Citra_Threshold.jpg', manualthreshold)
            pixmap_threshold = QPixmap ('./Temp_Save/Citra_Threshold.jpg')
            self.FotoThreshold.setPixmap(pixmap_threshold)
            cv2.imwrite('./Temp_Save/Citra_Akhir.jpg', chasil)
            pixmap_openclose = QPixmap ('./Temp_Save/Citra_Akhir.jpg')
            self.FotoAkhir.setPixmap(pixmap_openclose)

            #mengambil nilai B, G, dan R
            B= ((sum_color/self.count)[0])
            G= ((sum_color/self.count)[1])
            R= ((sum_color/self.count)[2])

            # Mengkonversi nilai RGB menjadi HSI
            r = R / (R+G+B)
            g = G / (R+G+B)
            b = B / (R+G+B)

            #pembulatan
            self.r = np.round(r, 2)
            self.g = np.round(g, 2)
            self.b = np.round(b, 2)

            #hitung nilai HSI
            Max = max(r, g, b)
            Min = min(r, g, b)
            Selisih = Max - Min
            
            if Selisih == 0:
                H = 0
            elif Max == r:
                H = (60* ((g-b)/Selisih)) 
            elif Max == g:
                H = (60* ((b-r)/Selisih)+120) 

            elif Max == b:
                H= (60* ((g-b)/Selisih)+240) 
            if Max == 0:
                S = 0
            else:
                S = (Selisih / Max) *100
            V = Max *100

            self.H = np.round(H, 2)
            self.S = np.round(S, 2)
            self.V = np.round(V, 2)
            
            brix = round(6.378*self.g - 0.3686)

            B = (f'{B:.0f}')
            G = (f'{G:.0f}')
            R = (f'{R:.0f}')
            H = (f'{H:}')
            S = (f'{S:}')
            V = (f'{V:}')
            
            #menampilkan nilai hasil perhitungan
            self.nilai_red.setText(f'= {str(R)}')
            self.nilai_green.setText(f'= {str(G)}')
            self.nilai_blue.setText(f'= {str(B)}')
            self.nilai_hue.setText(f'= {str(self.H)}')
            self.nilai_saturation.setText(f'= {str(self.S)}')
            self.nilai_intensity.setText(f'= {str(self.V)}')
            self.nilai_brix.setText(f'={str(brix)} ')
            self.activator = 2+2



app=QApplication(sys.argv)
mainwindow=MainWindow()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.showMaximized() # fit to screen window
widget.setWindowTitle("Tomato Analyser") # mengubah nama dari window
widget.show()
sys.exit(app.exec_())

