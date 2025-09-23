from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Скрапер")
        self.resize(980, 560)
        
        # Стиль
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f5fcfc, stop:1 #e6f7f7
                );
                color: #083a3a;
            }
            QWidget {
                font-family: "Segoe UI", "Inter", Arial;
                font-size: 11pt;
                color: #083a3a;
            }
            QTabWidget::pane {
                border: 1px solid #cceaea;
                border-radius: 10px;
                background: #ffffff;
                top: -1px;
            }
            QTabBar::tab {
                background: #ebfafa;
                border: 1px solid #cceaea;
                padding: 8px 14px;
                margin-right: 6px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:hover { background: #dff5f5; }
            QTabBar::tab:selected {
                background: #ffffff;
                border-bottom-color: #ffffff;
                font-weight: 600;
            }
            QLabel#heroTitle { color: #007d7d; letter-spacing: 0.3px; }
            QPushButton {
                background: #00b3b3; color: white; border: none; border-radius: 10px;
                padding: 10px 18px; font-weight: 600; transition: all 0.15s ease-in-out;
            }
            QPushButton:hover { background: #009999; transform: scale(1.04); }
            QPushButton:pressed { background: #008080; transform: scale(0.98); }
            QPushButton:disabled { background: #b3e5e5; color: #e0f2f2; }
            QTextEdit {
                background: #ffffff; border: 1px solid #cceaea; border-radius: 8px;
                padding: 10px 12px; color: #083a3a;
            }
            QProgressBar {
                background: #cceaea; border: none; border-radius: 6px; height: 10px;
            }
            QProgressBar::chunk { background-color: #00b3b3; border-radius: 6px; }
        """)
        
        # Центральный виджет
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        root = QtWidgets.QVBoxLayout(central)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)
        
        # Заголовок
        self.title = QtWidgets.QLabel("Скрапинг криптовалют",
                                      alignment=Qt.AlignCenter)
        self.title.setObjectName("heroTitle")
        f = self.title.font()
        f.setPointSize(22)
        f.setBold(True)
        self.title.setFont(f)
        root.addWidget(self.title)
        
        # Ряд кнопок
        row = QtWidgets.QHBoxLayout()
        row.addStretch(1)
        self.btnStart = QtWidgets.QPushButton("Начать сбор данных");
        self.btnStart.setMinimumHeight(42)
        self.btnStop = QtWidgets.QPushButton("Закончить сбор данных");
        self.btnStop.setMinimumHeight(42)
        self.btnExport = QtWidgets.QPushButton("Выгрузить в Excel");
        self.btnExport.setMinimumHeight(42)
        self.btnPlot = QtWidgets.QPushButton("Построить график");
        self.btnPlot.setMinimumHeight(42)
        
        for w in (self.btnStart, self.btnStop, self.btnExport, self.btnPlot):
            row.addWidget(w);
            row.addSpacing(10)
        row.addStretch(1)
        root.addLayout(row)
        
        # Индикатор
        self.busy = QtWidgets.QProgressBar()
        self.busy.setTextVisible(False)
        self.busy.setRange(0, 0)
        self.busy.setVisible(False)
        root.addWidget(self.busy)
        
        # Одно окно для обеих вкладок
        self.tabs = QtWidgets.QTabWidget()
        root.addWidget(self.tabs, 1)
        
        # Вкладка "Логи"
        self.logsTab = QtWidgets.QWidget()
        vlogs = QtWidgets.QVBoxLayout(self.logsTab)
        vlogs.setContentsMargins(10, 10, 10, 10)
        self.txtLog = QtWidgets.QTextEdit()
        self.txtLog.setReadOnly(True)
        self.txtLog.setPlaceholderText("Здесь будут появляться логи…")
        vlogs.addWidget(self.txtLog)
        self.tabs.addTab(self.logsTab, "Логи")
        
        # Вкладка "График"
        self.chartTab = QtWidgets.QWidget()  # <= добавили атрибут
        vchart = QtWidgets.QVBoxLayout(self.chartTab)
        vchart.setContentsMargins(10, 10, 10, 10)
        self.chartHost = QtWidgets.QWidget(objectName="chartHost")
        vchart.addWidget(self.chartHost)
        self.tabs.addTab(self.chartTab, "График")
