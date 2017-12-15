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
    ui->textEdit->setText(ui->textEdit_2->toPlainText());
}

void MainWindow::on_pushButton_2_clicked()
{
    ui->textEdit_2->toPlainText();
}