# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(612, 428)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.lineEdit_6 = QLineEdit(Form)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_6.setReadOnly(True)

        self.verticalLayout_7.addWidget(self.lineEdit_6)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.jupiter_url_6 = QLineEdit(Form)
        self.jupiter_url_6.setObjectName(u"jupiter_url_6")
        self.jupiter_url_6.setMaximumSize(QSize(100, 16777215))
        self.jupiter_url_6.setReadOnly(True)

        self.verticalLayout_4.addWidget(self.jupiter_url_6, 0, Qt.AlignmentFlag.AlignLeft)

        self.jupiter_url_8 = QLineEdit(Form)
        self.jupiter_url_8.setObjectName(u"jupiter_url_8")
        self.jupiter_url_8.setMaximumSize(QSize(100, 16777215))
        self.jupiter_url_8.setReadOnly(True)

        self.verticalLayout_4.addWidget(self.jupiter_url_8, 0, Qt.AlignmentFlag.AlignLeft)

        self.jupiter_url_9 = QLineEdit(Form)
        self.jupiter_url_9.setObjectName(u"jupiter_url_9")
        self.jupiter_url_9.setMaximumSize(QSize(100, 16777215))
        self.jupiter_url_9.setReadOnly(True)

        self.verticalLayout_4.addWidget(self.jupiter_url_9, 0, Qt.AlignmentFlag.AlignLeft)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.sol_mint = QLineEdit(Form)
        self.sol_mint.setObjectName(u"sol_mint")
        self.sol_mint.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_5.addWidget(self.sol_mint)

        self.api_key = QLineEdit(Form)
        self.api_key.setObjectName(u"api_key")
        self.api_key.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_5.addWidget(self.api_key)

        self.wallet_dir = QLineEdit(Form)
        self.wallet_dir.setObjectName(u"wallet_dir")
        self.wallet_dir.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_5.addWidget(self.wallet_dir)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.jupiter_url = QLineEdit(self.groupBox)
        self.jupiter_url.setObjectName(u"jupiter_url")
        self.jupiter_url.setMinimumSize(QSize(200, 0))
        self.jupiter_url.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.jupiter_url)

        self.jupiter_url_2 = QLineEdit(self.groupBox)
        self.jupiter_url_2.setObjectName(u"jupiter_url_2")
        self.jupiter_url_2.setMinimumSize(QSize(200, 0))
        self.jupiter_url_2.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.jupiter_url_2)

        self.jupiter_url_4 = QLineEdit(self.groupBox)
        self.jupiter_url_4.setObjectName(u"jupiter_url_4")
        self.jupiter_url_4.setMinimumSize(QSize(200, 0))
        self.jupiter_url_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.jupiter_url_4.setReadOnly(True)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.jupiter_url_4)

        self.jupiter_url_7 = QLineEdit(self.groupBox)
        self.jupiter_url_7.setObjectName(u"jupiter_url_7")
        self.jupiter_url_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.jupiter_url_7)

        self.jupiter_url_3 = QLineEdit(self.groupBox)
        self.jupiter_url_3.setObjectName(u"jupiter_url_3")
        self.jupiter_url_3.setMinimumSize(QSize(200, 0))
        self.jupiter_url_3.setToolTipDuration(0)
        self.jupiter_url_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.jupiter_url_3.setAutoFillBackground(False)
        self.jupiter_url_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.jupiter_url_3.setReadOnly(True)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.jupiter_url_3)

        self.userpriority = QLineEdit(self.groupBox)
        self.userpriority.setObjectName(u"userpriority")
        self.userpriority.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.userpriority)

        self.dynamicCompute = QCheckBox(self.groupBox)
        self.dynamicCompute.setObjectName(u"dynamicCompute")
        self.dynamicCompute.setMinimumSize(QSize(0, 25))
        self.dynamicCompute.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.dynamicCompute)

        self.wrapUnwrapSol = QCheckBox(self.groupBox)
        self.wrapUnwrapSol.setObjectName(u"wrapUnwrapSol")
        self.wrapUnwrapSol.setMinimumSize(QSize(0, 25))
        self.wrapUnwrapSol.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.wrapUnwrapSol)

        self.jupiter_url_5 = QLineEdit(self.groupBox)
        self.jupiter_url_5.setObjectName(u"jupiter_url_5")
        self.jupiter_url_5.setMinimumSize(QSize(200, 0))
        self.jupiter_url_5.setReadOnly(True)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.jupiter_url_5)

        self.auto_slippage = QCheckBox(self.groupBox)
        self.auto_slippage.setObjectName(u"auto_slippage")
        self.auto_slippage.setMinimumSize(QSize(0, 25))
        self.auto_slippage.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.auto_slippage)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(200, 0))
        self.lineEdit.setReadOnly(True)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.lineEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit_5 = QLineEdit(self.groupBox)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_5.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit_5)

        self.MIN = QLineEdit(self.groupBox)
        self.MIN.setObjectName(u"MIN")
        self.MIN.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.MIN)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineEdit_3 = QLineEdit(self.groupBox)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_3.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.lineEdit_3)

        self.MAX = QLineEdit(self.groupBox)
        self.MAX.setObjectName(u"MAX")
        self.MAX.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.MAX)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout)


        self.verticalLayout_6.addWidget(self.groupBox)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.reset = QPushButton(Form)
        self.reset.setObjectName(u"reset")

        self.verticalLayout_7.addWidget(self.reset, 0, Qt.AlignmentFlag.AlignHCenter)


        self.gridLayout.addLayout(self.verticalLayout_7, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lineEdit_6.setText(QCoreApplication.translate("Form", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.jupiter_url_6.setText(QCoreApplication.translate("Form", u"sol_mint", None))
        self.jupiter_url_8.setText(QCoreApplication.translate("Form", u"api_key", None))
        self.jupiter_url_9.setText(QCoreApplication.translate("Form", u"wallets_dir", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Transaction", None))
        self.jupiter_url.setText(QCoreApplication.translate("Form", u"jupiter_url", None))
        self.jupiter_url_2.setText(QCoreApplication.translate("Form", u"wrapUnwrapSOL", None))
        self.jupiter_url_4.setText(QCoreApplication.translate("Form", u"usepriorityLevelWithMaxLamports", None))
        self.jupiter_url_3.setText(QCoreApplication.translate("Form", u"dynamicComputeUnitLimit", None))
        self.dynamicCompute.setText("")
        self.wrapUnwrapSol.setText("")
        self.jupiter_url_5.setText(QCoreApplication.translate("Form", u"auto_slippage", None))
        self.auto_slippage.setText("")
        self.lineEdit.setText(QCoreApplication.translate("Form", u"dynamic_slippage", None))
        self.lineEdit_5.setText(QCoreApplication.translate("Form", u"MIN", None))
        self.lineEdit_3.setText(QCoreApplication.translate("Form", u"MAX", None))
        self.reset.setText(QCoreApplication.translate("Form", u"\u0421\u0411\u0420\u041e\u0421", None))
    # retranslateUi

