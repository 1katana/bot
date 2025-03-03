# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QMainWindow, QPlainTextEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpinBox, QStatusBar,
    QToolButton, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(976, 677)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 100, 30))
        self.horizontalLayout_9 = QHBoxLayout(self.widget)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, 17, -1)
        self.toolButton = QToolButton(self.groupBox)
        self.toolButton.setObjectName(u"toolButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy1)
        self.toolButton.setMinimumSize(QSize(0, 0))
        icon = QIcon(QIcon.fromTheme(u"applications-development"))
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QSize(25, 25))

        self.verticalLayout.addWidget(self.toolButton)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.input_secret = QLineEdit(self.groupBox)
        self.input_secret.setObjectName(u"input_secret")
        self.input_secret.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.input_secret.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.input_secret)

        self.add_wallet_button = QPushButton(self.groupBox)
        self.add_wallet_button.setObjectName(u"add_wallet_button")
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.add_wallet_button.setFont(font1)

        self.horizontalLayout_2.addWidget(self.add_wallet_button, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, 30, -1)
        self.input_raspr = QLineEdit(self.groupBox)
        self.input_raspr.setObjectName(u"input_raspr")

        self.horizontalLayout.addWidget(self.input_raspr)

        self.raspr_button = QPushButton(self.groupBox)
        self.raspr_button.setObjectName(u"raspr_button")
        self.raspr_button.setFont(font1)

        self.horizontalLayout.addWidget(self.raspr_button)

        self.sobr_button = QPushButton(self.groupBox)
        self.sobr_button.setObjectName(u"sobr_button")
        self.sobr_button.setFont(font1)

        self.horizontalLayout.addWidget(self.sobr_button)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.spinBox = QSpinBox(self.groupBox)
        self.spinBox.setObjectName(u"spinBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy2)
        self.spinBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.spinBox.setAutoFillBackground(False)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(5)

        self.horizontalLayout_3.addWidget(self.spinBox, 0, Qt.AlignmentFlag.AlignRight)

        self.create_wallets = QPushButton(self.groupBox)
        self.create_wallets.setObjectName(u"create_wallets")
        self.create_wallets.setFont(font1)

        self.horizontalLayout_3.addWidget(self.create_wallets, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.load_direct = QPushButton(self.groupBox)
        self.load_direct.setObjectName(u"load_direct")
        self.load_direct.setFont(font1)

        self.verticalLayout_6.addWidget(self.load_direct)

        self.update_button = QPushButton(self.groupBox)
        self.update_button.setObjectName(u"update_button")
        self.update_button.setFont(font1)

        self.verticalLayout_6.addWidget(self.update_button)

        self.scrollArea = QScrollArea(self.groupBox)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 560, 18))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy3)
        self.scroll_Wallets = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_Wallets.setObjectName(u"scroll_Wallets")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_6.addWidget(self.scrollArea)


        self.horizontalLayout_6.addWidget(self.groupBox)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy4)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.token_adress = QLineEdit(self.groupBox_4)
        self.token_adress.setObjectName(u"token_adress")
        self.token_adress.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.token_adress.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.token_adress)

        self.use_token_adress = QPushButton(self.groupBox_4)
        self.use_token_adress.setObjectName(u"use_token_adress")
        self.use_token_adress.setFont(font1)

        self.horizontalLayout_4.addWidget(self.use_token_adress, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.groupBox_2 = QGroupBox(self.groupBox_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy5)
        self.groupBox_2.setMinimumSize(QSize(0, 0))
        self.groupBox_2.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.buy_sol_input = QLineEdit(self.groupBox_2)
        self.buy_sol_input.setObjectName(u"buy_sol_input")
        self.buy_sol_input.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_2.addWidget(self.buy_sol_input)

        self.buy_button = QPushButton(self.groupBox_2)
        self.buy_button.setObjectName(u"buy_button")
        self.buy_button.setFont(font1)

        self.verticalLayout_2.addWidget(self.buy_button)


        self.horizontalLayout_5.addWidget(self.groupBox_2, 0, Qt.AlignmentFlag.AlignTop)

        self.groupBox_3 = QGroupBox(self.groupBox_4)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy5.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy5)
        self.groupBox_3.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.sell_input = QLineEdit(self.groupBox_3)
        self.sell_input.setObjectName(u"sell_input")
        self.sell_input.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.sell_input)

        self.sell_button = QPushButton(self.groupBox_3)
        self.sell_button.setObjectName(u"sell_button")
        self.sell_button.setFont(font1)

        self.verticalLayout_3.addWidget(self.sell_button)


        self.horizontalLayout_5.addWidget(self.groupBox_3, 0, Qt.AlignmentFlag.AlignTop)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)


        self.verticalLayout_4.addWidget(self.groupBox_4, 0, Qt.AlignmentFlag.AlignTop)

        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy6)
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label = QLabel(self.groupBox_5)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(80, 80))
        self.label.setMaximumSize(QSize(140, 140))
        self.label.setBaseSize(QSize(0, 0))
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setFrameShadow(QFrame.Shadow.Plain)
        self.label.setPixmap(QPixmap(u"empty.jpg"))
        self.label.setScaledContents(False)

        self.verticalLayout_9.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.name_token_label = QLineEdit(self.groupBox_5)
        self.name_token_label.setObjectName(u"name_token_label")
        self.name_token_label.setMinimumSize(QSize(0, 0))
        self.name_token_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_token_label.setReadOnly(True)

        self.verticalLayout_9.addWidget(self.name_token_label)


        self.horizontalLayout_7.addLayout(self.verticalLayout_9)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lineEdit = QLineEdit(self.groupBox_5)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy7)
        self.lineEdit.setMinimumSize(QSize(0, 0))
        self.lineEdit.setMaximumSize(QSize(100, 16777215))
        font2 = QFont()
        font2.setPointSize(10)
        self.lineEdit.setFont(font2)
        self.lineEdit.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lineEdit)

        self.time = QLineEdit(self.groupBox_5)
        self.time.setObjectName(u"time")
        sizePolicy7.setHeightForWidth(self.time.sizePolicy().hasHeightForWidth())
        self.time.setSizePolicy(sizePolicy7)
        self.time.setMaximumSize(QSize(80, 16777215))
        self.time.setFont(font2)
#if QT_CONFIG(tooltip)
        self.time.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.time.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.time.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.time)

        self.buy_dev = QLineEdit(self.groupBox_5)
        self.buy_dev.setObjectName(u"buy_dev")
        sizePolicy7.setHeightForWidth(self.buy_dev.sizePolicy().hasHeightForWidth())
        self.buy_dev.setSizePolicy(sizePolicy7)
        self.buy_dev.setMaximumSize(QSize(80, 16777215))
        self.buy_dev.setFont(font2)
        self.buy_dev.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.buy_dev)

        self.lineEdit_2 = QLineEdit(self.groupBox_5)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(0, 0))
        self.lineEdit_2.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_2.setFont(font2)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lineEdit_2)


        self.verticalLayout_7.addLayout(self.formLayout)

        self.all_sell_check = QCheckBox(self.groupBox_5)
        self.all_sell_check.setObjectName(u"all_sell_check")
        sizePolicy1.setHeightForWidth(self.all_sell_check.sizePolicy().hasHeightForWidth())
        self.all_sell_check.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.all_sell_check.setFont(font3)
        self.all_sell_check.setChecked(False)

        self.verticalLayout_7.addWidget(self.all_sell_check, 0, Qt.AlignmentFlag.AlignHCenter)


        self.horizontalLayout_7.addLayout(self.verticalLayout_7)


        self.verticalLayout_10.addLayout(self.horizontalLayout_7)

        self.form_create_token = QPushButton(self.groupBox_5)
        self.form_create_token.setObjectName(u"form_create_token")
        sizePolicy7.setHeightForWidth(self.form_create_token.sizePolicy().hasHeightForWidth())
        self.form_create_token.setSizePolicy(sizePolicy7)
        self.form_create_token.setMinimumSize(QSize(0, 0))
        self.form_create_token.setMaximumSize(QSize(1000, 35))
        self.form_create_token.setFont(font1)

        self.verticalLayout_10.addWidget(self.form_create_token)


        self.verticalLayout_4.addWidget(self.groupBox_5)


        self.horizontalLayout_6.addLayout(self.verticalLayout_4)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)

        self.console = QPlainTextEdit(self.centralwidget)
        self.console.setObjectName(u"console")
        sizePolicy5.setHeightForWidth(self.console.sizePolicy().hasHeightForWidth())
        self.console.setSizePolicy(sizePolicy5)
        self.console.setMaximumSize(QSize(16777215, 16777215))
        self.console.setReadOnly(False)

        self.verticalLayout_8.addWidget(self.console)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setLocale(QLocale(QLocale.Russian, QLocale.Russia))
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u0448\u0435\u043b\u044c\u043a\u0438", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.input_secret.setPlaceholderText(QCoreApplication.translate("MainWindow", u"secret key", None))
        self.add_wallet_button.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043a\u043e\u0448\u0435\u043b\u0435\u043a", None))
        self.input_raspr.setPlaceholderText(QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.raspr_button.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0441\u043f\u0440\u0435\u0434\u0435\u043b\u0438\u0442\u044c ", None))
        self.sobr_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0431\u0440\u0430\u0442\u044c \u0434\u0435\u043d\u044c\u0433\u0438", None))
        self.create_wallets.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043a\u043e\u0448\u0435\u043b\u044c\u043a\u0438", None))
        self.load_direct.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0438\u0437 \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0438\u0438", None))
        self.update_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u043c\u044b\u0439 \u0442\u043e\u043a\u0435\u043d", None))
        self.token_adress.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Token address", None))
        self.use_token_adress.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c \u0442\u043e\u043a\u0435\u043d", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0443\u043f\u043a\u0430", None))
        self.buy_sol_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0432 sol", None))
        self.buy_button.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0423\u041f\u0418\u0422\u042c", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0434\u0430\u0436\u0430", None))
        self.sell_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"AUTO FULL", None))
        self.sell_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0420\u041e\u0414\u0410\u0422\u042c", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u043c\u043e\u043d\u0435\u0442\u044b", None))
        self.label.setText("")
        self.name_token_label.setText(QCoreApplication.translate("MainWindow", u"TRUMP", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u044f \u0432\u044b\u0445\u043e\u0434\u0430", None))
        self.time.setText("")
        self.time.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0441", None))
        self.buy_dev.setText("")
        self.buy_dev.setPlaceholderText(QCoreApplication.translate("MainWindow", u"sol", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0443\u043f\u043a\u0430 DEV", None))
        self.all_sell_check.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0439\u0442\u044b \u0441\u043e \u0432\u0441\u0435\u043c\u0438", None))
        self.form_create_token.setText(QCoreApplication.translate("MainWindow", u"\u0424\u043e\u0440\u043c\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f \u043c\u043e\u043d\u0435\u0442\u044b", None))
    # retranslateUi

