# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLayout,
    QLineEdit, QMainWindow, QPlainTextEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpinBox, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1076, 732)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(10)
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
        self.input_secret = QLineEdit(self.groupBox)
        self.input_secret.setObjectName(u"input_secret")

        self.horizontalLayout_2.addWidget(self.input_secret)

        self.add_wallet_button = QPushButton(self.groupBox)
        self.add_wallet_button.setObjectName(u"add_wallet_button")

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

        self.horizontalLayout.addWidget(self.raspr_button)

        self.sobr_button = QPushButton(self.groupBox)
        self.sobr_button.setObjectName(u"sobr_button")

        self.horizontalLayout.addWidget(self.sobr_button)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.spinBox = QSpinBox(self.groupBox)
        self.spinBox.setObjectName(u"spinBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy1)
        self.spinBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.spinBox.setAutoFillBackground(False)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(5)

        self.horizontalLayout_3.addWidget(self.spinBox, 0, Qt.AlignmentFlag.AlignRight)

        self.create_wallets = QPushButton(self.groupBox)
        self.create_wallets.setObjectName(u"create_wallets")

        self.horizontalLayout_3.addWidget(self.create_wallets, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.load_direct = QPushButton(self.groupBox)
        self.load_direct.setObjectName(u"load_direct")

        self.verticalLayout_6.addWidget(self.load_direct)

        self.update_button = QPushButton(self.groupBox)
        self.update_button.setObjectName(u"update_button")

        self.verticalLayout_6.addWidget(self.update_button)

        self.scrollArea = QScrollArea(self.groupBox)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 540, 334))
        self.scroll_Wallets = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_Wallets.setObjectName(u"scroll_Wallets")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_6.addWidget(self.scrollArea)


        self.horizontalLayout_6.addWidget(self.groupBox)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.token_adress = QLineEdit(self.groupBox_4)
        self.token_adress.setObjectName(u"token_adress")

        self.horizontalLayout_4.addWidget(self.token_adress)

        self.use_token_adress = QPushButton(self.groupBox_4)
        self.use_token_adress.setObjectName(u"use_token_adress")

        self.horizontalLayout_4.addWidget(self.use_token_adress, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.groupBox_2 = QGroupBox(self.groupBox_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy2)
        self.groupBox_2.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.buy_sol_input = QLineEdit(self.groupBox_2)
        self.buy_sol_input.setObjectName(u"buy_sol_input")

        self.verticalLayout_2.addWidget(self.buy_sol_input)

        self.buy_button = QPushButton(self.groupBox_2)
        self.buy_button.setObjectName(u"buy_button")

        self.verticalLayout_2.addWidget(self.buy_button)


        self.horizontalLayout_5.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.groupBox_4)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy2.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy2)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.sell_input = QLineEdit(self.groupBox_3)
        self.sell_input.setObjectName(u"sell_input")

        self.verticalLayout_3.addWidget(self.sell_input)

        self.sell_button = QPushButton(self.groupBox_3)
        self.sell_button.setObjectName(u"sell_button")

        self.verticalLayout_3.addWidget(self.sell_button)


        self.horizontalLayout_5.addWidget(self.groupBox_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.webEngineView = QWebEngineView(self.groupBox_4)
        self.webEngineView.setObjectName(u"webEngineView")
        sizePolicy.setHeightForWidth(self.webEngineView.sizePolicy().hasHeightForWidth())
        self.webEngineView.setSizePolicy(sizePolicy)
        self.webEngineView.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_5.addWidget(self.webEngineView)


        self.horizontalLayout_6.addWidget(self.groupBox_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.console = QPlainTextEdit(self.centralwidget)
        self.console.setObjectName(u"console")
        sizePolicy2.setHeightForWidth(self.console.sizePolicy().hasHeightForWidth())
        self.console.setSizePolicy(sizePolicy2)
        self.console.setMaximumSize(QSize(16777215, 16777215))
        self.console.setReadOnly(False)

        self.verticalLayout_4.addWidget(self.console)

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
    # retranslateUi

