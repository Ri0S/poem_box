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
    ui->textEdit->setStyleSheet("font: 20pt;");
}

MainWindow::~MainWindow()
{
    delete ui;
}

string GetHangul(string english)
{
    string cmd = "python3 /home/pi/poem_box/interface/heconverter/heconverter.py " + english;
    cout << cmd << endl;
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
    //string seed = GetHangul(seed_eng);
    //cout << "seed get!! " + seed << endl;
    cout << seed_eng << endl;
    string cmd = string("python ") + string("/home/pi/poem_box/interface/recv.py ") + seed_eng;
    system(cmd.c_str());
    cout << cmd << endl;

    int f = open("/home/pi/poem_box/interface/sample.txt", O_RDONLY);
    char buffer[4000];
    read(f, buffer, 4000);
    ui->textEdit->setText(buffer);
    int pid = fork();
    if(pid == 0)
        system("omxplayer /home/pi/poem_box/interface/sample.mp3");
}

void MainWindow::on_textEdit_2_selectionChanged()
{
    ui->textEdit_2->setPlainText("");
}
