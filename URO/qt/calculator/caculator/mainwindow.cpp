#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <memory>
#include <format>
#include <ranges>
#include <iostream>
#include <array>
#include <sstream>
#include <cctype>

#include <QVBoxLayout>
#include <QGridLayout>
#include <QGroupBox>
#include <QLineEdit>
#include <QLabel>


// Test:
// Evaluate("563 + 669 * 32 / 98")
// Evaluate("1 + 1")

// works only for integer addition
int Evaluate(const std::string& expression)
{
    std::cout << "Expression: " << expression << "\n";

    std::stringstream tokens(expression);
    std::vector<int> values;
    std::vector<char> ops;

    char token;

    // remove white space
    while (tokens >> std::ws >> token)
    {
        std::cout << "Token: " << token << "\n";
        if (std::isdigit(token))
        {
            tokens.putback(token);
            int value;
            tokens >> value;
            values.push_back(value);
        } 
        else if (token == '+')
        {
            ops.push_back(token);
        }
    }

    while (!ops.empty())
    {
        ops.back(); ops.pop_back(); // is the add symbol
        int a = values.back(); values.pop_back();
        int b = values.back(); values.pop_back();
        values.push_back(a + b);
    }

    return (!values.empty()) ? values.back() : -9999;
}



MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , m_CalcButtons()
    , m_ExpressionLine()
{
    Evaluate("563 + 669 * 32 / 98");
    Evaluate("1 + 1");


    // Main Frame
    // auto* frame = new QGroupBox("Main Frame", this);
    auto* frame = new QFrame(this);
    frame->setStyleSheet(R"(
        QFrame { 
            background-color: #ecf0f1;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        }
    )");

    QMainWindow::setCentralWidget(frame);

    auto* frameLayout = new QVBoxLayout(frame);
    frameLayout->setSpacing(10);
    frameLayout->setContentsMargins(10, 10, 10, 10);

    // Text output frame. Has the string buffer inputted by user.
    // auto* outputFrame = new QGroupBox("Output Frame", frame);
    auto* outputFrame = new QFrame(frame);
    auto* outputFrameLayout = new QVBoxLayout(outputFrame);
    outputFrame->setStyleSheet(R"(
        QFrame {
            background-color: #ecf0f1;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        })");


    // Lay it out in the main frame.
    frameLayout->addWidget(outputFrame);


    // Output frame's child.
    m_ExpressionLine.setParent(outputFrame);
    m_ExpressionLine.setMinimumHeight(60);
    m_ExpressionLine.setAlignment(Qt::AlignRight);
    m_ExpressionLine.setReadOnly(true);
    m_ExpressionLine.setStyleSheet(R"(
        QLineEdit {
            background-color: #2c3e50;
            color: white;
            font-size: 36px;
            border: 2px solid #34495e;
            border-radius: 8px;
            padding: 10px;
        }
        QLineEdit:focus {
            border: 2px solid #3498db;
        })");

    // m_ExpressionLine.setText("neco");
    

    // Layout the output frame.
    outputFrameLayout->addWidget(&m_ExpressionLine);

    // Controls frame. Has the numbers and operands
    // auto* controlsFrame = new QGroupBox("Controls Frame", frame);
    auto* controlsFrame = new QFrame(frame);
    auto* controlsFrameLayout = new QGridLayout(controlsFrame);
    controlsFrame->setStyleSheet(R"(
        QFrame { 
            background-color: #ecf0f1;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        }
    )");

    // Add this controlls frame to the main frame.
    frameLayout->addWidget(controlsFrame);


    // F: Inserting buttons into a map.
    auto addCalcButton = [&](const QString& nameOfButton, const QColor& color) {
        std::shared_ptr<QPushButton> button = std::make_shared<QPushButton>(nameOfButton, controlsFrame);
        button->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);

        // Set custom style
        QString buttonStyle = QString(R"( 
            QPushButton {
                font-size: 20px; 
                padding: 10px;
                border-radius: 10px;
                background-color: %1;
                color: white;
            }
            QPushButton:pressed { background-color: %2; }
        )").arg(color.name(), color.darker(150).name());

        // qInfo("%s, %s", color.name().toStdString().c_str(), color.darker(150).name().toStdString().c_str());

        button->setStyleSheet(buttonStyle);
        m_CalcButtons.insert(nameOfButton, button);
        return button;
    };

    // Numeric Buttons 
    for (qint32 i = 0; i < 10; i++)
    {
        addCalcButton(QString::number(i), QColor("#3498db"));
    }

    // Special Operations
    addCalcButton("AC", QColor("#e74c3c"));   // Red
    addCalcButton("+/-", QColor("#f39c12"));  // Orange
    addCalcButton("%", QColor("#f39c12"));    // Orange

    // Basic Operators
    addCalcButton("/", QColor("#e67e22"));    // Dark Orange
    addCalcButton("*", QColor("#e67e22"));
    addCalcButton("-", QColor("#e67e22"));
    addCalcButton("+", QColor("#e67e22"));

    // Decimal and Equals
    addCalcButton(".", QColor("#3498db"));   // Same as numbers
    addCalcButton("=", QColor("#2ecc71"));   // Green

    QString buttonGrid[5][4] = {
        { "AC", "+/-", "%", "/" },
        { "7", "8", "9", "*" },
        { "4", "5", "6", "-" },
        { "1", "2", "3", "+" },
        { "0", "#0", ".", "=" }
    };

    for (int row = 0; row < 5; ++row) 
    {
        for (int col = 0; col < 4; ++col) 
        {
            QString key = buttonGrid[row][col];
            if (!m_CalcButtons.contains(key)) continue;

            controlsFrameLayout->addWidget(m_CalcButtons[key].get(), row, col, (key == "0" ? 1 : 1), (key == "0" ? 2 : 1));
        }
    }

    // Binding
    for (const QString& key : std::vector<QString>({ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0" }))
    {
        QObject::connect(m_CalcButtons[key].get(), &QPushButton::clicked, this, &MainWindow::OnDigitButtonClick);
    }
    for (const QString& key : std::vector<QString>({ "+", "-", "*", "/", "%" }))
    {
        QObject::connect(m_CalcButtons[key].get(), &QPushButton::clicked, this, &MainWindow::OnOpButtonClick);
    }

    QObject::connect(m_CalcButtons["="].get(), &QPushButton::clicked, this, &MainWindow::OnEvalButtonClick);
    QObject::connect(m_CalcButtons["AC"].get(), &QPushButton::clicked, this, &MainWindow::OnAllClearButtonClick);
    QObject::connect(m_CalcButtons["."].get(), &QPushButton::clicked, this, &MainWindow::OnDotButtonClick);
}

MainWindow::~MainWindow()
{
}

void MainWindow::OnDigitButtonClick()
{
    auto* button = qobject_cast<QPushButton*>(QObject::sender());
    if (!button) return;
    qInfo("Button clicked! Text: %s", button->text().toStdString().c_str());
    m_ExpressionLine.setText(m_ExpressionLine.text() + button->text());
}

void MainWindow::OnOpButtonClick()
{
    auto* button = qobject_cast<QPushButton*>(QObject::sender());
    if (!button) return;
    qInfo("Button clicked! Text: %s", button->text().toStdString().c_str());
    m_ExpressionLine.setText(m_ExpressionLine.text() + " " + button->text() + " ");
}

void MainWindow::OnEvalButtonClick()
{
    auto* button = qobject_cast<QPushButton*>(QObject::sender());
    if (!button) return;
    // Evaluate expression
    QString expression = m_ExpressionLine.text();
    // expression.back();
    qInfo("Evaluate: %s", expression.toStdString().c_str());
    m_ExpressionLine.clear();

    m_ExpressionLine.setText(QString::number(Evaluate(expression.toStdString())));
}

void MainWindow::OnAllClearButtonClick()
{
    auto* button = qobject_cast<QPushButton*>(QObject::sender());
    if (!button) return;
    m_ExpressionLine.clear();
}

void MainWindow::OnDotButtonClick()
{
    auto* button = qobject_cast<QPushButton*>(QObject::sender());
    if (!button) return;
    m_ExpressionLine.setText(m_ExpressionLine.text() + button->text());
}


