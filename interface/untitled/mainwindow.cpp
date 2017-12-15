#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFont>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->textEdit->setStyleSheet("font: 36pt;");
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked()
{
//     show poem and play sound
    ui->textEdit->setText("");

}

void MainWindow::on_pushButton_2_clicked()
{
    ui->textEdit->setText(ui->textEdit_2->toPlainText());
//     after recv poem and sound file
//     start botton activate
//    send seed to serv
    ui->pushButton->setEnabled(1);
}
