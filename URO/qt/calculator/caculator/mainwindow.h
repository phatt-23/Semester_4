#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <memory>

#include <QMainWindow>
#include <QPushButton>
#include <QLineEdit>


class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

public slots:
    void OnDigitButtonClick();
    void OnOpButtonClick();
    void OnEvalButtonClick();
    void OnAllClearButtonClick();
    void OnDotButtonClick();

private:
    QMap<QString, std::shared_ptr<QPushButton>> m_CalcButtons;
    QLineEdit m_ExpressionLine;
};
#endif // MAINWINDOW_H
