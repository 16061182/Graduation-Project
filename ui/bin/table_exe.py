from ui.bin import table
from PyQt5 import QtWidgets


def set_table_item(item1='data1', item2='data2', item3='data3'):
    ui.tableWidget.setItem(0 , 0, QtWidgets.QTableWidgetItem(item1))
    ui.tableWidget.setItem(1 , 1, QtWidgets.QTableWidgetItem(item2))
    ui.tableWidget.setItem(2 , 2, QtWidgets.QTableWidgetItem(item3))

def button_clicked():
    ui.pushButton.setText('按钮被点击')
    set_table_item(item2='changed')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = table.Ui_MainWindow()
    ui.setupUi(MainWindow)

    set_table_item()
    ui.pushButton.clicked.connect(button_clicked)

    MainWindow.show()
    sys.exit(app.exec_())