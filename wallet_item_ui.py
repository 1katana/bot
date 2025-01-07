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
    QLineEdit, QSizePolicy, QToolButton, QVBoxLayout,
    QWidget)

class Ui_MyWidget(object):
    def setupUi(self, MyWidget):
        if not MyWidget.objectName():
            MyWidget.setObjectName(u"MyWidget")
        MyWidget.resize(513, 42)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MyWidget.sizePolicy().hasHeightForWidth())
        MyWidget.setSizePolicy(sizePolicy)
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
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 9, 5, 9)
        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout.addWidget(self.checkBox)

        self.name = QLineEdit(self.groupBox)
        self.name.setObjectName(u"name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy1)
        self.name.setMinimumSize(QSize(50, 0))
        self.name.setMaximumSize(QSize(80, 16777215))
        self.name.setReadOnly(True)

        self.horizontalLayout.addWidget(self.name)

        self.adress = QLineEdit(self.groupBox)
        self.adress.setObjectName(u"adress")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.adress.sizePolicy().hasHeightForWidth())
        self.adress.setSizePolicy(sizePolicy2)
        self.adress.setReadOnly(True)

        self.horizontalLayout.addWidget(self.adress)

        self.balance_sol = QLineEdit(self.groupBox)
        self.balance_sol.setObjectName(u"balance_sol")
        sizePolicy1.setHeightForWidth(self.balance_sol.sizePolicy().hasHeightForWidth())
        self.balance_sol.setSizePolicy(sizePolicy1)
        self.balance_sol.setMinimumSize(QSize(50, 0))
        self.balance_sol.setMaximumSize(QSize(80, 16777215))
        self.balance_sol.setReadOnly(True)

        self.horizontalLayout.addWidget(self.balance_sol)

        self.balance_use = QLineEdit(self.groupBox)
        self.balance_use.setObjectName(u"balance_use")
        sizePolicy1.setHeightForWidth(self.balance_use.sizePolicy().hasHeightForWidth())
        self.balance_use.setSizePolicy(sizePolicy1)
        self.balance_use.setMinimumSize(QSize(50, 0))
        self.balance_use.setMaximumSize(QSize(100, 16777215))
        self.balance_use.setReadOnly(True)

        self.horizontalLayout.addWidget(self.balance_use)

        self.priority = QLineEdit(self.groupBox)
        self.priority.setObjectName(u"priority")
        sizePolicy1.setHeightForWidth(self.priority.sizePolicy().hasHeightForWidth())
        self.priority.setSizePolicy(sizePolicy1)
        self.priority.setMinimumSize(QSize(30, 0))
        self.priority.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout.addWidget(self.priority)

        self.toolButton_2 = QToolButton(self.groupBox)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toolButton_2.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.WindowClose))
        self.toolButton_2.setIcon(icon)

        self.horizontalLayout.addWidget(self.toolButton_2)


        self.verticalLayout.addWidget(self.groupBox)


        self.retranslateUi(MyWidget)

        QMetaObject.connectSlotsByName(MyWidget)
    # setupUi

    def retranslateUi(self, MyWidget):
        MyWidget.setWindowTitle(QCoreApplication.translate("MyWidget", u"MyWidget", None))
        self.groupBox.setTitle("")
        self.checkBox.setText("")
        self.name.setPlaceholderText(QCoreApplication.translate("MyWidget", u"Name", None))
        self.adress.setPlaceholderText(QCoreApplication.translate("MyWidget", u"adress", None))
        self.balance_sol.setPlaceholderText(QCoreApplication.translate("MyWidget", u"balance sol", None))
        self.balance_use.setPlaceholderText(QCoreApplication.translate("MyWidget", u"balance use token", None))
        self.priority.setPlaceholderText(QCoreApplication.translate("MyWidget", u"priority", None))
        self.toolButton_2.setText(QCoreApplication.translate("MyWidget", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c"))
    # retranslateUi

