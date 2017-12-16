#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFont>
#include <string>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <fstream>
#include <iostream>
#include <stdio.h>
#include <fcntl.h>
using namespace std;
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->textEdit->setStyleSheet("font: 24pt;");
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

string GetHangul(string english)
{
    string cmd = "python3 /home/rios/poembox/poem_box/interface/heconverter/heconverter.py " + english;
    FILE* file = popen(cmd.c_str(), "r");
    // use fscanf to read:
    char buffer[2000];
    fscanf(file, "%2000s", buffer);
    pclose(file);

    return string(buffer);
}

bool fexists(const char* filename)
{
    ifstream ifile(filename);
    return ifile.good();
}

void MainWindow::on_pushButton_2_clicked()
{
    string seed_eng = ui->textEdit_2->toPlainText().toStdString();
    string seed = GetHangul(seed_eng);
    cout << "seed get!! " + seed << endl;
    string cmd = string("python ") + string("/home/rios/poembox/poem_box/interface/recv.py ") + seed;
    system(cmd.c_str());
    cout << cmd << endl;
//    while(!fexists("/home/rios/poembox/poem_box/interface/sample.txt"))
//    {
//        cout << "wating sample" << endl;
//        cout << "wating sample" << endl;
//        cout << "wating sample" << endl;
//        cout << "wating sample" << endl;
//        cout << "wating sample" << endl;

//        ui->textEdit->setText("receiving poem...");
//    }

    int f = open("/home/rios/poembox/poem_box/interface/sample.txt", O_RDONLY);
    char buffer[4000];
    read(f, buffer, 4000);
    ui->textEdit->setText(buffer);

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


void MainWindow::on_textEdit_2_selectionChanged()
{
    ui->textEdit_2->setPlainText("");
}
