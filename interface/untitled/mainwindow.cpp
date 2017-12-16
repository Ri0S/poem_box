#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFont>
#include <string>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
using namespace std;
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

/*
string GetHangul(string english)
{
    FILE* file = popen("ls", "r");
    // use fscanf to read:
    char buffer[2000];
    fscanf(file, "%2000s", buffer);
    pclose(file);


}
*/

void MainWindow::on_pushButton_2_clicked()
{
    string seed = ui->textEdit_2->toPlainText().toStdString();
    //system("");
    ui->textEdit->setText(ui->textEdit_2->toPlainText());

//    after recv poem and sound file
//    start botton activate
//    send seed to serv
//    if can't type hangul in program
//    use heconvert.py with pipe
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
