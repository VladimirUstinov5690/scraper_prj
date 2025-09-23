from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavToolbar

from scrapper_dir.db import get_symbol_all


def clear_layout(widget: QtWidgets.QWidget) -> None:
    """Очищает layout"""
    layout = widget.layout()
    if not layout:
        return
    while layout.count():
        item = layout.takeAt(0)
        w = item.widget()
        if w is not None:
            w.deleteLater()


def plot_price(symbol: str, host_widget: QtWidgets.QWidget) -> None:
    """Строит график цены для symbol внутрь вкладки «График»"""
    data = get_symbol_all(symbol)
    if not data:
        raise ValueError(f"Нет данных для символа: {symbol}")
    
    dates, prices = zip(*data)
    
    layout = host_widget.layout()
    if layout is None:
        layout = QtWidgets.QVBoxLayout(host_widget)
        host_widget.setLayout(layout)

    clear_layout(host_widget)
    
    # фигура matplotlib
    fig = Figure(figsize=(6, 3.5), dpi=100)
    ax = fig.add_subplot(111)
    
    # строим график
    ax.plot(dates, prices, linewidth=1.5)
    ax.set_title(f"Динамика цены: {symbol.upper()}")
    ax.set_xlabel("Время")
    ax.set_ylabel("Цена, USD")
    fig.autofmt_xdate()
    
    canvas = FigureCanvas(fig)
    
    # тулбар под графиком
    toolbar = NavToolbar(canvas, host_widget)
    
    layout.addWidget(toolbar)
    layout.addWidget(canvas)
