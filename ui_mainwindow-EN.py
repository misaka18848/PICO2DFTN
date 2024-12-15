# -*- coding: utf-8 -*-

import os, time, shutil, re, subprocess 
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QThread,Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QSizePolicy, QWidget)

from qfluentwidgets import (BodyLabel, LargeTitleLabel, PixmapLabel, PushButton,
    SubtitleLabel, TitleLabel)

import xml.etree.ElementTree as ET

class Worker(QThread):
    update_label = Signal(str)
    finished = Signal()



    def run(self):
                self.update_label.emit("Current status: Start script")
                self.update_label.emit("Current status: Checking the apks folder for apk files")
                def check_apk(dir_path):
                    for file in os.listdir(dir_path):
                        if file.endswith(".apk"):
                            return True
                    return False
                a = check_apk("./apks")
                if (a == False):
                    self.update_label.emit("Current status: No apk file found")
                    time.sleep(1)
                    self.update_label.emit("Current status: No apk file found, checking the work folder for AndroidManifest.xml")
                    c = os.path.exists("./work/AndroidManifest.xml")
                    if (c == False):
                        self.update_label.emit("Current status: AndroidManifest.xml not found")
                        time.sleep(1)
                        self.finished.emit()
                    else:
                        self.update_label.emit("Current status: AndroidManifest.xml found, start processing")

                        # Reading XML files
                        ET.register_namespace('android', "http://schemas.android.com/apk/res/android")  
                        tree = ET.parse("./work/AndroidManifest.xml")
                        root = tree.getroot()
                        # Traverse all <activity> nodes
                        for activity in root.findall("application/activity"):
                            # Add the <meta-data> attribute
                            meta_data = ET.SubElement(activity, "meta-data")
                            meta_data.attrib["android:name"] = "pico.vr.position"
                            meta_data.attrib["android:value"] = "near"

                        # Traverse all <activity-alias> nodes
                        for alias in root.findall("application/activity-alias"):
                            # Add the <meta-data> attribute
                            meta_data = ET.SubElement(alias, "meta-data")
                            meta_data.attrib["android:name"] = "pico.vr.position"
                            meta_data.attrib["android:value"] = "near"

                        # Write to XML file
                        tree.write("./work/AndroidManifest.xml", encoding="utf-8")


                                                
                        self.update_label.emit("Current status: The file is modified successfully")
                        time.sleep(1)
                        self.finished.emit()

                else:
                        def process_apk(apk_path,self):
                            self.update_label.emit("Current status: The apk file has been found and processing begins")
                            def remove_illegal_chars(filename):

                                # Matching illegal character
                                illegal_chars = re.compile(r'[\x00-\x1f\x7f-\xff\s]')

                                # Replace invalid characters with null characters
                                filename = illegal_chars.sub('', filename)

                                return filename


                            filename = os.path.basename(apk_path)
                            new_filename = remove_illegal_chars(filename)
                            os.rename(apk_path, f"./apks/{new_filename}")
                            print(new_filename)
                            apk_name = new_filename
                            time.sleep(1)
                            self.update_label.emit("Current status: Start cleaning work,nosign directory")
                            if not os.path.exists("work"):
                                os.makedirs("work")
                            if not os.path.exists("nosign"):
                                os.makedirs("nosign")
                            if not os.path.exists("patched"):
                                os.makedirs("patched")
                            shutil.rmtree("./work")
                            shutil.rmtree("./nosign")
                            #shutil.rmtree("./patched")
                            self.update_label.emit("Current status: Clearing completed")
                            time.sleep(1)
                            self.update_label.emit(f"Current status: Decompile started {apk_name}")
                            cmd = f"apktool.bat d ./apks/{apk_name} -q -o ./work"
                            subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            self.update_label.emit("Current status: Decompile complete")
                            time.sleep(1)
                            self.update_label.emit("Current status: The file is being modified")

                            # Reading XML files
                            ET.register_namespace('android', "http://schemas.android.com/apk/res/android")  
                            tree = ET.parse("./work/AndroidManifest.xml")
                            root = tree.getroot()
                            # Traverse all <activity> nodes
                            for activity in root.findall("application/activity"):
                                # Add the <meta-data> attribute
                                meta_data = ET.SubElement(activity, "meta-data")
                                meta_data.attrib["android:name"] = "pico.vr.position"
                                meta_data.attrib["android:value"] = "near"

                            # Traverse all <activity-alias> nodes
                            for alias in root.findall("application/activity-alias"):
                                # Add the <meta-data> attribute
                                meta_data = ET.SubElement(alias, "meta-data")
                                meta_data.attrib["android:name"] = "pico.vr.position"
                                meta_data.attrib["android:value"] = "near"

                            # Write to XML file
                            tree.write("./work/AndroidManifest.xml", encoding="utf-8")
                                
                            self.update_label.emit("Current status: The file is modified successfully")
                            time.sleep(1)
                            self.update_label.emit("Current status: Start compiling")
                            cmd = f"apktool.bat b ./work -q -o ./nosign/{apk_name} -api 28"
                            subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            self.update_label.emit("Current status: Compilation completed")
                            time.sleep(1)
                            self.update_label.emit("Current status: Start signing")
                            if not os.path.exists("patched"):
                                os.makedirs("patched")
                            cmd = f"""java -jar uber-apk-signer-1.3.0.jar -a ./nosign/{apk_name} --ks testkey.jks --ksAlias "testkey" --ksKeyPass 114514 --ksPass 114514 --out ./patched """
                            subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            self.update_label.emit("Current status: Signing is complete")
                            time.sleep(1)
                            self.update_label.emit("Current status: Now start cleaning project files")
                            if not os.path.exists("work"):
                                os.makedirs("work")
                            if not os.path.exists("nosign"):
                                os.makedirs("nosign")
                            shutil.rmtree("./work")
                            shutil.rmtree("./nosign")
                            f = os.path.exists(f"./patched/{apk_name[:-4]}-aligned-signed.apk")
                            self.update_label.emit("Current status: The project file is cleared")
                            if (f == False):
                                self.update_label.emit(f"Current status:{apk_name}processing failed")
                                time.sleep(1)

                                #self.finished.emit()
                            else:
                                if(os.path.isfile(f"./patched/{apk_name[:-4]}-aligned-signed.apk.idsig")):
                                    os.remove(f"./patched/{apk_name[:-4]}-aligned-signed.apk.idsig")
                                if os.path.exists(f"./patched/PICOdedicated{apk_name[:-4]}.apk"):
                                    count = 1
                                    while os.path.exists(f"./patched/PICOdedicated{apk_name[:-4]}({count}).apk"):
                                        count += 1
                                    os.rename(f"./patched/{apk_name[:-4]}-aligned-signed.apk", f"./patched/PICOdedicated{apk_name[:-4]}({count}).apk")
                                else:
                                    os.rename(f"./patched/{apk_name[:-4]}-aligned-signed.apk", f"./patched/PICOdedicated{apk_name[:-4]}.apk")
                                self.update_label.emit(f"Current status:{apk_name}Successful processing")
                                time.sleep(1)


                        for apk in os.listdir("./apks"):
                            if apk.endswith(".apk"):
                                process_apk(os.path.join("./apks", apk),self)
                        self.update_label.emit(f"Current status: All apk files are patched, you can install the apk in the patched folder and use it later\nApk that fail to process can be manually changed by referring to txt, you may need to give the application permission to run")
                        self.finished.emit()




class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.NonModal)
        Form.setEnabled(True)
        Form.resize(1280, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(1280, 800))
        Form.setMaximumSize(QSize(1280, 800))
        Form.setSizeIncrement(QSize(0, 0))
        icon = QIcon()
        icon.addFile(u":/img/pnlo.ico", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet(u"#Form{border-image:url(:/img/BGD.png);}")
        self.LargeTitleLabel = LargeTitleLabel(Form)
        self.LargeTitleLabel.setObjectName(u"LargeTitleLabel")
        self.LargeTitleLabel.setGeometry(QRect(460, 300, 600, 50))
        self.LargeTitleLabel.setProperty("lightColor", QColor(255, 255, 255))
        self.SubtitleLabel = SubtitleLabel(Form)
        self.SubtitleLabel.setObjectName(u"SubtitleLabel")
        self.SubtitleLabel.setGeometry(QRect(460, 350, 250, 30))
        self.SubtitleLabel.setProperty("lightColor", QColor(255, 255, 255))
        self.PixmapLabel = PixmapLabel(Form)
        self.PixmapLabel.setObjectName(u"PixmapLabel")
        self.PixmapLabel.setGeometry(QRect(380, 305, 80, 80))
        self.PixmapLabel.setPixmap(QPixmap(u":/img/logo.png"))
        self.TitleLabel = TitleLabel(Form)
        self.TitleLabel.setObjectName(u"TitleLabel")
        self.TitleLabel.setGeometry(QRect(400, 390, 200, 40))
        self.TitleLabel.setProperty("lightColor", QColor(255, 255, 255))
        self.BodyLabel = BodyLabel(Form)
        self.BodyLabel.setObjectName(u"BodyLabel")
        self.BodyLabel.setGeometry(QRect(400, 440, 800, 60))
        self.BodyLabel.setProperty("lightColor", QColor(255, 255, 255))
        self.PushButton = PushButton(Form)
        self.PushButton.setObjectName(u"PushButton")
        self.PushButton.setGeometry(QRect(400, 520, 100, 32))
        self.PushButton.setFocusPolicy(Qt.ClickFocus)
        self.PushButton.clicked.connect(self.start)
        self.BodyLabel_2 = BodyLabel(Form)
        self.BodyLabel_2.setObjectName(u"BodyLabel_2")
        self.BodyLabel_2.setGeometry(QRect(510, 515, 800, 40))
        self.BodyLabel_2.setProperty("lightColor", QColor(255, 255, 255))
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)
        self.worker = Worker()
        self.worker.finished.connect(self.on_worker_finished)

    def on_worker_finished(self):
        self.PushButton.setText('start')
        self.PushButton.setEnabled(True)

        



    def start(self):
        self.PushButton.setText("processing")
        self.PushButton.setEnabled(False)
        self.worker = Worker()
        self.worker.update_label.connect(self.updateLabel)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()
    def updateLabel(self, text):
        self.BodyLabel_2.setText(text)
    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"P2DFTN Tool 2.0", None))
        self.LargeTitleLabel.setText(QCoreApplication.translate("Form", u"PICO 2D APP Far to Near tool", None))
        self.SubtitleLabel.setText(QCoreApplication.translate("Form", u"Made By Misaka18848", None))
        self.TitleLabel.setText(QCoreApplication.translate("Form", u"How to use\uff1f", None))
        self.BodyLabel.setText(QCoreApplication.translate("Form", "Put the apk into the apks folder \n or put the decompiled AndroidManifest.xml into the work folder (in this case the apk folder cannot have apk) \n and click the Start button below", None))
        self.PushButton.setText(QCoreApplication.translate("Form", "start", None))
        self.BodyLabel_2.setText(QCoreApplication.translate("Form", "Current status: No operation", None))

    

