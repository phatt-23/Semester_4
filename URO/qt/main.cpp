#include <iostream>
#include <sstream>
#include <stack>
#include <cctype>
#include <stdexcept>
#include <vector>
#include <unordered_map>

// Function to determine precedence of operators
int precedence(char op) {
    if (op == '+' || op == '-') return 1;
    if (op == '*' || op == '/' || op == '%') return 2;
    return 0;
}

// Function to perform arithmetic operations
int applyOp(int a, int b, char op) {
    switch (op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': 
            if (b == 0) throw std::runtime_error("Division by zero");
            return a / b;
        case '%': 
            if (b == 0) throw std::runtime_error("Modulo by zero");
            return a % b;
        default: throw std::runtime_error("Invalid operator");
    }
}

// Evaluates an infix mathematical expression
int evaluate(const std::string& expression) {
    std::vector<int> values;   // Stack to store numbers
    std::vector<char> ops;     // Stack to store operators
    std::istringstream tokens(expression);
    char token;

    while (tokens >> std::ws >> token) {
        if (std::isdigit(token)) {  
            tokens.putback(token);
            int value;
            tokens >> value;
            values.push_back(value);
        } 
        else if (token == '(') {  
            ops.push_back(token);
        } 
        else if (token == ')') {  
            while (!ops.empty() && ops.back() != '(') {
                int b = values.back(); values.pop_back();
                int a = values.back(); values.pop_back();
                char op = ops.back(); ops.pop_back();
                values.push_back(applyOp(a, b, op));
            }
            ops.pop_back();
        } 
        else {  
            while (!ops.empty() && precedence(ops.back()) >= precedence(token)) {
                int b = values.back(); values.pop_back();
                int a = values.back(); values.pop_back();
                char op = ops.back(); ops.pop_back();
                values.push_back(applyOp(a, b, op));
            }
            ops.push_back(token);
        }
    }

    while (!ops.empty()) {
        int b = values.back(); values.pop_back();
        int a = values.back(); values.pop_back();
        char op = ops.back(); ops.pop_back();
        values.push_back(applyOp(a, b, op));
    }

    return values.back();
}

// Example usage
int main() {
    std::string expression;
    std::cout << "Enter an expression: ";
    std::getline(std::cin, expression);

    try {
        int result = evaluate(expression);
        std::cout << "Result: " << result << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}

