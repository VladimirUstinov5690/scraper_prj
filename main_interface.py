import os
import sys
import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from gui.interface import Ui_MainWindow
from scrapper_dir.scraper import start_scraping
from scrapper_dir.db import add_to_db
from scrapper_dir.export_excel import export_to_excel
from scrapper_dir.analyze import plot_price


# подключение qt-плагинов для Win/macOS/Linux
def ensure_qt_platform_plugins():
    """
    Настройки поиска плагинов на Win/macOS/Linux.
    """
    base = os.path.dirname(PyQt5.__file__)
    candidates = [
        os.path.join(base, "Qt5", "plugins", "platforms"),
        os.path.join(base, "Qt", "plugins", "platforms"),
        os.path.join(base, "Qt", "plugins", "platforms"),
        os.path.join(base, "Qt", "plugins"),
        os.path.join(base, "Qt5", "plugins"),
    ]
    
    if getattr(sys, 'frozen', False):
        app_dir = os.path.dirname(sys.executable)
        candidates += [
            os.path.join(app_dir, "Qt", "plugins", "platforms"),
            os.path.join(app_dir, "plugins", "platforms"),
            os.path.join(app_dir, "platforms"),
        ]
    
    platforms_dir = None
    for p in candidates:
        if os.path.isdir(p) and os.path.isdir(os.path.join(p, "..")):
            if os.path.basename(p) == "platforms" or p.endswith(os.sep + "platforms"):
                platforms_dir = p
                break
    
    if platforms_dir:
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platforms_dir


ensure_qt_platform_plugins()


class ScraperWorker(QtCore.QObject):
    """Циклично собирает данные в фоновом потоке (не блокирует работу
    интерфейса)"""
    log = QtCore.pyqtSignal(str)
    saved = QtCore.pyqtSignal(int)
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    
    def __init__(self, interval_sec: int = 60):
        super().__init__()
        self._interval = interval_sec
        self._stop = False
    
    @QtCore.pyqtSlot()
    def start_cycle(self):
        self._stop = False
        self.started.emit()
        self.log.emit("Фоновый сбор запущен.")
        try:
            while not self._stop:
                try:
                    data = start_scraping()
                    if data:
                        count = add_to_db(data)
                        self.saved.emit(count)
                        self.log.emit(f"✅ Добавлено {count} записей.")
                    else:
                        self.log.emit("⚠ Не удалось собрать данные.")
                except Exception as e:
                    self.log.emit(f"❌ Ошибка сбора: {e}")
                
                # Ждём по секунде, для правильной остановки работы
                for _ in range(self._interval):
                    if self._stop:
                        break
                    QtCore.QThread.sleep(1)
        finally:
            self.finished.emit()
    
    @QtCore.pyqtSlot()
    def stop(self):
        self._stop = True


def main():
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.setWindowTitle("Скрапер")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "gui", "icons", "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        window.setWindowIcon(QIcon(icon_path))
    
    # состояние фонового потока
    worker_thread: QtCore.QThread | None = None
    worker: ScraperWorker | None = None
    
    # обработчики кнопок
    def start_scraping_clicked():
        nonlocal worker_thread, worker
        if worker_thread and worker_thread.isRunning():
            window.txtLog.append("⏳ Уже идёт сбор данных.")
            return
        
        window.busy.setVisible(True)
        window.txtLog.append("▶ Начинаю фоновый сбор каждые 60 сек...")
        
        worker_thread = QtCore.QThread()
        worker = ScraperWorker(interval_sec=60)
        worker.moveToThread(worker_thread)
        
        # сигналы
        worker.log.connect(window.txtLog.append)
        worker.saved.connect(lambda n: None)
        worker.finished.connect(lambda: (
            window.txtLog.append("⏹ Фоновый сбор остановлен."),
            window.busy.setVisible(False),
            window.btnStart.setEnabled(True),
            window.btnStop.setEnabled(False)
        ))
        
        # запуск/остановка
        worker_thread.started.connect(worker.start_cycle)
        worker.finished.connect(worker_thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker_thread.finished.connect(worker_thread.deleteLater)
        
        # UI блокировки
        window.btnStart.setEnabled(False)
        window.btnStop.setEnabled(True)
        
        worker_thread.start()
    
    def stop_scraper_clicked():
        nonlocal worker_thread, worker
        if worker:
            worker.stop()
        else:
            window.txtLog.append("ℹ Фоновая задача не запущена.")
    
    def export_to_excel_clicked():
        window.txtLog.append("📤 Выгружаю в Excel...")
        try:
            export_to_excel()
            window.txtLog.append(
                "✅ База данных выгружена в Excel! Файл «cryptocurrency data.xlsx» рядом с main_interface.py"
            )
        except Exception as e:
            window.txtLog.append(f"❌ Ошибка экспорта: {e}")
    
    def plot_price_clicked():
        symbol, ok = QtWidgets.QInputDialog.getText(
            window,
            "Построить график",
            "Введите символ (например, BTC):",
            text="BTC"
        )
        if not ok or not symbol.strip():
            return
        
        try:
            # нарисовать график
            plot_price(symbol.strip().upper(), window.chartHost)
            # переключение на вкладку «График»
            try:
                idx = window.tabs.indexOf(window.chartTab)  # если есть
            except AttributeError:
                idx = window.tabs.indexOf(window.chartHost.parentWidget())
            if idx >= 0:
                window.tabs.setCurrentIndex(idx)
            
            window.txtLog.append(
                f"📈 Построен график для {symbol.strip().upper()}")
        except Exception as e:
            window.txtLog.append(f"❌ Не удалось построить график: {e}")
    
    # привязки к кнопкам
    window.btnStart.clicked.connect(start_scraping_clicked)
    window.btnStop.clicked.connect(stop_scraper_clicked)
    window.btnExport.clicked.connect(export_to_excel_clicked)
    window.btnPlot.clicked.connect(plot_price_clicked)
    
    # изначально «Стоп» выключена
    window.btnStop.setEnabled(False)
    
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
