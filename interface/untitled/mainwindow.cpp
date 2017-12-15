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
    ui->pushButton->setDisabled(true);
    ui->pushButton_3->setEnabled(true);
}

void MainWindow::on_pushButton_2_clicked()
{
    ui->textEdit->setText(ui->textEdit_2->toPlainText());
//    after recv poem and sound file
//    start botton activate
//    send seed to serv
    ui->pushButton->setDisabled(true);
//    after receiving done, activate start button
    ui->pushButton->setEnabled(true);

//    if generate button is pushed while play
//    stop play
    ui->pushButton_3->setDisabled(true);
}

void MainWindow::on_pushButton_3_clicked()
{
    ui->pushButton->setEnabled(true);
    ui->pushButton_3->setDisabled(true);
}
