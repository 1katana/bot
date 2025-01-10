# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'item.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLineEdit, QPushButton, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget)

class Ui_MyWidget(object):
    def setupUi(self, MyWidget):
        if not MyWidget.objectName():
            MyWidget.setObjectName(u"MyWidget")
        MyWidget.resize(513, 44)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MyWidget.sizePolicy().hasHeightForWidth())
        MyWidget.setSizePolicy(sizePolicy)
        MyWidget.setMinimumSize(QSize(0, 0))
        MyWidget.setMaximumSize(QSize(16777215, 50))
        MyWidget.setAutoFillBackground(False)
        MyWidget.setStyleSheet(u"\n"
"background-color: rgb(55, 55, 55);")
        self.verticalLayout = QVBoxLayout(MyWidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(MyWidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(0, 0))
        self.groupBox.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 9, 5, 9)
        self.use = QCheckBox(self.groupBox)
        self.use.setObjectName(u"use")
        self.use.setIconSize(QSize(12, 12))
        self.use.setChecked(False)

        self.horizontalLayout.addWidget(self.use)

        self.is_master_button = QPushButton(self.groupBox)
        self.is_master_button.setObjectName(u"is_master_button")
        self.is_master_button.setMinimumSize(QSize(20, 0))
        self.is_master_button.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.is_master_button)

        self.name = QLineEdit(self.groupBox)
        self.name.setObjectName(u"name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy1)
        self.name.setMinimumSize(QSize(50, 0))
        self.name.setMaximumSize(QSize(63, 16777215))
        self.name.setReadOnly(True)

        self.horizontalLayout.addWidget(self.name)

        self.adress = QLineEdit(self.groupBox)
        self.adress.setObjectName(u"adress")
        sizePolicy.setHeightForWidth(self.adress.sizePolicy().hasHeightForWidth())
        self.adress.setSizePolicy(sizePolicy)
        self.adress.setReadOnly(True)

        self.horizontalLayout.addWidget(self.adress)

        self.balance_sol = QLineEdit(self.groupBox)
        self.balance_sol.setObjectName(u"balance_sol")
        sizePolicy1.setHeightForWidth(self.balance_sol.sizePolicy().hasHeightForWidth())
        self.balance_sol.setSizePolicy(sizePolicy1)
        self.balance_sol.setMinimumSize(QSize(50, 0))
        self.balance_sol.setMaximumSize(QSize(75, 16777215))
        self.balance_sol.setReadOnly(True)

        self.horizontalLayout.addWidget(self.balance_sol)

        self.balance_use = QLineEdit(self.groupBox)
        self.balance_use.setObjectName(u"balance_use")
        sizePolicy1.setHeightForWidth(self.balance_use.sizePolicy().hasHeightForWidth())
        self.balance_use.setSizePolicy(sizePolicy1)
        self.balance_use.setMinimumSize(QSize(50, 0))
        self.balance_use.setMaximumSize(QSize(85, 16777215))
        self.balance_use.setReadOnly(True)

        self.horizontalLayout.addWidget(self.balance_use)

        self.priority = QLineEdit(self.groupBox)
        self.priority.setObjectName(u"priority")
        sizePolicy1.setHeightForWidth(self.priority.sizePolicy().hasHeightForWidth())
        self.priority.setSizePolicy(sizePolicy1)
        self.priority.setMinimumSize(QSize(30, 0))
        self.priority.setMaximumSize(QSize(47, 16777215))

        self.horizontalLayout.addWidget(self.priority)

        self.delete_button = QToolButton(self.groupBox)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.delete_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.WindowClose))
        self.delete_button.setIcon(icon)
        self.delete_button.setIconSize(QSize(12, 12))

        self.horizontalLayout.addWidget(self.delete_button)


        self.verticalLayout.addWidget(self.groupBox)


        self.retranslateUi(MyWidget)

        QMetaObject.connectSlotsByName(MyWidget)
    # setupUi

    def retranslateUi(self, MyWidget):
        MyWidget.setWindowTitle(QCoreApplication.translate("MyWidget", u"MyWidget", None))
        self.groupBox.setTitle("")
        self.use.setText("")
        self.is_master_button.setText(QCoreApplication.translate("MyWidget", u"simple", None))
        self.name.setPlaceholderText(QCoreApplication.translate("MyWidget", u"Name", None))
        self.adress.setPlaceholderText(QCoreApplication.translate("MyWidget", u"adress", None))
        self.balance_sol.setPlaceholderText(QCoreApplication.translate("MyWidget", u"balance sol", None))
        self.balance_use.setPlaceholderText(QCoreApplication.translate("MyWidget", u"balance use token", None))
        self.priority.setPlaceholderText(QCoreApplication.translate("MyWidget", u"priority", None))
        self.delete_button.setText(QCoreApplication.translate("MyWidget", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c"))
    # retranslateUi

