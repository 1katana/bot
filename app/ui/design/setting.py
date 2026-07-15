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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QGroupBox, QLineEdit, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(358, 534)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineEdit_6 = QLineEdit(Form)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        font = QFont()
        font.setFamilies([u"Rage"])
        font.setPointSize(11)
        font.setBold(True)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_6.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.lineEdit_6)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textEdit = QTextEdit(self.groupBox_2)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setEnabled(True)
        self.textEdit.setMinimumSize(QSize(320, 0))
        self.textEdit.setSizeIncrement(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(11)
        self.textEdit.setFont(font1)
        self.textEdit.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEdit)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.jupiter_url_8 = QLineEdit(self.groupBox_2)
        self.jupiter_url_8.setObjectName(u"jupiter_url_8")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jupiter_url_8.sizePolicy().hasHeightForWidth())
        self.jupiter_url_8.setSizePolicy(sizePolicy)
        self.jupiter_url_8.setMinimumSize(QSize(0, 0))
        self.jupiter_url_8.setMaximumSize(QSize(100, 16777215))
        self.jupiter_url_8.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.jupiter_url_8.setReadOnly(True)

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.jupiter_url_8)

        self.jitoTipLamports = QLineEdit(self.groupBox_2)
        self.jitoTipLamports.setObjectName(u"jitoTipLamports")
        self.jitoTipLamports.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.jitoTipLamports)

        self.jupiter_url_4 = QLineEdit(self.groupBox_2)
        self.jupiter_url_4.setObjectName(u"jupiter_url_4")
        sizePolicy.setHeightForWidth(self.jupiter_url_4.sizePolicy().hasHeightForWidth())
        self.jupiter_url_4.setSizePolicy(sizePolicy)
        self.jupiter_url_4.setMinimumSize(QSize(0, 0))
        self.jupiter_url_4.setMaximumSize(QSize(100, 16777215))
        self.jupiter_url_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.jupiter_url_4.setReadOnly(True)

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.jupiter_url_4)

        self.userpriority = QLineEdit(self.groupBox_2)
        self.userpriority.setObjectName(u"userpriority")
        self.userpriority.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.userpriority)


        self.verticalLayout.addLayout(self.formLayout_3)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.formLayout_2 = QFormLayout(self.groupBox_3)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.jupiter_url_12 = QLineEdit(self.groupBox_3)
        self.jupiter_url_12.setObjectName(u"jupiter_url_12")
        self.jupiter_url_12.setMinimumSize(QSize(0, 0))
        self.jupiter_url_12.setMaximumSize(QSize(100, 16777215))
        self.jupiter_url_12.setReadOnly(True)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.jupiter_url_12)

        self.SOLANA_API = QLineEdit(self.groupBox_3)
        self.SOLANA_API.setObjectName(u"SOLANA_API")
        self.SOLANA_API.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.SOLANA_API)

        self.jupiter_url = QLineEdit(self.groupBox_3)
        self.jupiter_url.setObjectName(u"jupiter_url")
        self.jupiter_url.setMinimumSize(QSize(0, 0))
        self.jupiter_url.setMaximumSize(QSize(100, 16777215))
        self.jupiter_url.setReadOnly(True)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.jupiter_url)

        self.jupiter_url_7 = QLineEdit(self.groupBox_3)
        self.jupiter_url_7.setObjectName(u"jupiter_url_7")
        self.jupiter_url_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.jupiter_url_7)

        self.jupiter_url_10 = QLineEdit(self.groupBox_3)
        self.jupiter_url_10.setObjectName(u"jupiter_url_10")
        self.jupiter_url_10.setMinimumSize(QSize(0, 0))
        self.jupiter_url_10.setMaximumSize(QSize(100, 16777215))
        self.jupiter_url_10.setReadOnly(True)

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.jupiter_url_10)

        self.jito_url = QLineEdit(self.groupBox_3)
        self.jito_url.setObjectName(u"jito_url")
        self.jito_url.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.jito_url)

        self.jupiter_url_11 = QLineEdit(self.groupBox_3)
        self.jupiter_url_11.setObjectName(u"jupiter_url_11")
        self.jupiter_url_11.setMinimumSize(QSize(0, 0))
        self.jupiter_url_11.setMaximumSize(QSize(100, 16777215))
        self.jupiter_url_11.setReadOnly(True)

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.jupiter_url_11)

        self.pump_fun_url = QLineEdit(self.groupBox_3)
        self.pump_fun_url.setObjectName(u"pump_fun_url")
        self.pump_fun_url.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.pump_fun_url)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.jupiter_url_6 = QLineEdit(self.groupBox)
        self.jupiter_url_6.setObjectName(u"jupiter_url_6")
        sizePolicy.setHeightForWidth(self.jupiter_url_6.sizePolicy().hasHeightForWidth())
        self.jupiter_url_6.setSizePolicy(sizePolicy)
        self.jupiter_url_6.setMinimumSize(QSize(0, 0))
        self.jupiter_url_6.setMaximumSize(QSize(150, 16777215))
        self.jupiter_url_6.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.jupiter_url_6)

        self.sol_mint = QLineEdit(self.groupBox)
        self.sol_mint.setObjectName(u"sol_mint")
        self.sol_mint.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sol_mint)

        self.jupiter_url_2 = QLineEdit(self.groupBox)
        self.jupiter_url_2.setObjectName(u"jupiter_url_2")
        sizePolicy.setHeightForWidth(self.jupiter_url_2.sizePolicy().hasHeightForWidth())
        self.jupiter_url_2.setSizePolicy(sizePolicy)
        self.jupiter_url_2.setMinimumSize(QSize(0, 0))
        self.jupiter_url_2.setMaximumSize(QSize(150, 16777215))
        self.jupiter_url_2.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.jupiter_url_2)

        self.wrapUnwrapSol = QCheckBox(self.groupBox)
        self.wrapUnwrapSol.setObjectName(u"wrapUnwrapSol")
        self.wrapUnwrapSol.setMinimumSize(QSize(0, 25))
        self.wrapUnwrapSol.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.wrapUnwrapSol)

        self.jupiter_url_3 = QLineEdit(self.groupBox)
        self.jupiter_url_3.setObjectName(u"jupiter_url_3")
        sizePolicy.setHeightForWidth(self.jupiter_url_3.sizePolicy().hasHeightForWidth())
        self.jupiter_url_3.setSizePolicy(sizePolicy)
        self.jupiter_url_3.setMinimumSize(QSize(0, 0))
        self.jupiter_url_3.setMaximumSize(QSize(150, 16777215))
        self.jupiter_url_3.setToolTipDuration(0)
        self.jupiter_url_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.jupiter_url_3.setAutoFillBackground(False)
        self.jupiter_url_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.jupiter_url_3.setReadOnly(True)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.jupiter_url_3)

        self.dynamicCompute = QCheckBox(self.groupBox)
        self.dynamicCompute.setObjectName(u"dynamicCompute")
        self.dynamicCompute.setMinimumSize(QSize(0, 25))
        self.dynamicCompute.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.dynamicCompute)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QSize(0, 0))
        self.lineEdit.setMaximumSize(QSize(150, 16777215))
        self.lineEdit.setReadOnly(True)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lineEdit)

        self.dynamic_slippage = QCheckBox(self.groupBox)
        self.dynamic_slippage.setObjectName(u"dynamic_slippage")
        self.dynamic_slippage.setMinimumSize(QSize(0, 25))
        self.dynamic_slippage.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.dynamic_slippage)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.reset = QPushButton(Form)
        self.reset.setObjectName(u"reset")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.reset.setFont(font2)

        self.verticalLayout_2.addWidget(self.reset)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lineEdit_6.setText(QCoreApplication.translate("Form", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Priorityzation", None))
        self.textEdit.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u0418\u0421\u041f\u041e\u041b\u042c\u0417\u0423\u0415\u0422\u0421\u042f JitoTip</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u0417\u0430 \u043f\u0440\u0438\u043e\u0440\u0438\u0442\u0438\u0437\u0430\u0446\u0438\u044e \u043e\u0442\u0432\u0435\u0447\u0430\u0435\u0442 JitoTip</p></body>"
                        "</html>", None))
        self.jupiter_url_8.setText(QCoreApplication.translate("Form", u"jitoTip", None))
        self.jupiter_url_4.setText(QCoreApplication.translate("Form", u"priorityLevel", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"URLS", None))
        self.jupiter_url_12.setText(QCoreApplication.translate("Form", u"SOLANA_API", None))
        self.jupiter_url.setText(QCoreApplication.translate("Form", u"jupiter_url", None))
        self.jupiter_url_10.setText(QCoreApplication.translate("Form", u"jito_url", None))
        self.jupiter_url_11.setText(QCoreApplication.translate("Form", u"pump_fun_url", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Transaction", None))
        self.jupiter_url_6.setText(QCoreApplication.translate("Form", u"sol_mint", None))
        self.jupiter_url_2.setText(QCoreApplication.translate("Form", u"wrapUnwrapSOL", None))
        self.wrapUnwrapSol.setText("")
        self.jupiter_url_3.setText(QCoreApplication.translate("Form", u"dynamicComputeUnitLimit", None))
        self.dynamicCompute.setText("")
        self.lineEdit.setText(QCoreApplication.translate("Form", u"dynamic_slippage", None))
        self.dynamic_slippage.setText("")
        self.reset.setText(QCoreApplication.translate("Form", u"\u0421\u0411\u0420\u041e\u0421", None))
    # retranslateUi

