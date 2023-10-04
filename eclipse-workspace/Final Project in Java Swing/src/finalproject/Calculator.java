package finalproject;
import javax.swing.*;
import java.awt.Font;
import java.awt.*;
import java.awt.event.*;

public class Calculator extends JFrame {
    private JTextField textField;
    private JPanel panel;

    public Calculator() {
    	//initializing layout
        panel = new JPanel();
        panel.setLayout(new GridLayout(6, 5));
        
        //initializing buttons
        String[] buttonLabels = {"√", "^2", "^", "%", "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "=", "+", "AC"};
        
        Font font = new Font("Arial", Font.PLAIN, 50);
        for (String label : buttonLabels) {
            JButton button = new JButton(label);
            button.setFont(font);
            panel.add(button);
        }

        //initializing textfield
        textField = new JTextField();
        textField.setFont(font);
        panel.add(textField);

        //providing functionality to buttons
        ButtonListener buttonListener = new ButtonListener();

        for (Component c : panel.getComponents()) {
            if (c instanceof JButton) {
                ((JButton)c).addActionListener(buttonListener);
            }
        }

        //implementing keyboard functions
        KeyboardFocusManager manager = KeyboardFocusManager.getCurrentKeyboardFocusManager();
        manager.addKeyEventDispatcher(new KeyEventDispatcher() {
            @Override
            public boolean dispatchKeyEvent(KeyEvent e) {
                if (e.getID() == KeyEvent.KEY_TYPED) {
                    char keyChar = e.getKeyChar();
                    switch (keyChar) {
                        case '+':
                        case '-':
                        case '*':
                        case '/':
                        case '=':
                        case '.':
                            buttonListener.actionPerformed(
                                    new ActionEvent(new JButton(Character.toString(keyChar)), ActionEvent.ACTION_PERFORMED, null));
                            break;
                        case '\n':
                            buttonListener.actionPerformed(
                                    new ActionEvent(new JButton("="), ActionEvent.ACTION_PERFORMED, null));
                            break;
                        case 'c':
                            buttonListener.actionPerformed(
                                    new ActionEvent(new JButton("AC"), ActionEvent.ACTION_PERFORMED, null));
                            break;
                        default:
                            if (Character.isDigit(keyChar)) {
                                buttonListener.actionPerformed(
                                        new ActionEvent(new JButton(Character.toString(keyChar)), ActionEvent.ACTION_PERFORMED, null));
                            }
                            break;
                    }
                }
                return false;
            }
        });
        
        //displaying calculator
        add(panel);
        setTitle("Calculator");
        setSize(1600, 1000);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    public static void main(String[] args) {
        Calculator calculator = new Calculator();
    }

    class ButtonListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
        	//keeping track of the current operation and the number entered
            String buttonText = ((JButton)e.getSource()).getText();
            String currentText = textField.getText();

            //providing different functionalities to every operation
            switch(buttonText) {
                case "+":
                	decimalPoint = false;
                    operation = "+";
                    operand1 = Double.parseDouble(textField.getText());
                    textField.setText(currentText + operation);
                    break;
                case "-":
                	decimalPoint = false;
                    operation = "-";
                    operand1 = Double.parseDouble(textField.getText());
                    textField.setText(currentText + operation);
                    break;
                case "*":
                	decimalPoint = false;
                    operation = "*";
                    operand1 = Double.parseDouble(textField.getText());
                    textField.setText(currentText + operation);
                    break;
                case "/":
                	decimalPoint = false;
                    operation = "/";
                    operand1 = Double.parseDouble(textField.getText());
                    textField.setText(currentText + operation);
                    break;
                case ".":
                	decimalPoint = true;
                	textField.setText(currentText + ".");
                	break;
                case "√":
                	decimalPoint = false;
                	operation = "√";
                	operand1 = Double.parseDouble(textField.getText());
                	result = 0;
                	result = Math.sqrt(operand1);
                    textField.setText(Double.toString(result));
                    operation = null;
                    operand1 = 0;
                    operand2 = 0;
                	break;
                case "^2":
                	decimalPoint = false;
                	operation = "^2";
                	operand1 = Double.parseDouble(textField.getText());
                	result = 0;
                	result = Math.pow(operand1, 2);
                    textField.setText(Double.toString(result));
                    operation = null;
                    operand1 = 0;
                    operand2 = 0;
                	break;
                case "^":
                	decimalPoint = false;
                    operation = "^";
                    operand1 = Double.parseDouble(textField.getText());
                    textField.setText(currentText + operation);
                    break;
                case "%":
                	decimalPoint = false;
                    operation = "%";
                    operand1 = Double.parseDouble(textField.getText());
                    textField.setText(currentText + operation);
                    break;
                //calculating the result
                case "=":
                    if (operation != null && !textField.getText().equals("")) {
                        result = 0;

                        switch (operation) {
                            case "+":
                                result = operand1 + operand2;
                                break;
                            case "-":
                                result = operand1 - operand2;
                                break;
                            case "*":
                                result = operand1 * operand2;
                                break;
                            case "/":
                                result = operand1 / operand2;
                                break;
                            case "^":
                            	result = Math.pow(operand1, operand2);
                            	break;
                            case "%":
                            	result = operand1 % operand2;
                            	break;
                        }
                        textField.setText(Double.toString(result));
                        operation = null;
                        operand1 = 0;
                        operand2 = 0;
                        decimalPoint = false;
                    }
                    break;
                //all clear button
                case "AC":
                    textField.setText("");
                    operation = null;
                    operand1 = 0;
                    break;
                //entering numbers to the textfield
                default:
                	if (operation != null) {
                		if (operand2 == 0) {
                    		operand2 = Double.parseDouble(buttonText);
                		} else if (decimalPoint) {
                			if ((int)operand2 == operand2) {
                				operand2 = Double.parseDouble((int)operand2 + "." + buttonText);
                			} else {
                				operand2 = Double.parseDouble(Double.toString(operand2) + buttonText);
                			}
                		} else {
                    		operand2 = Double.parseDouble((int)operand2 + buttonText);
                		}
                	}
                	textField.setText(currentText + buttonText);
                    break;
            }
        }
        //initializing variables to keep track of the operands and the operation to perform
        private String operation;
        private double operand1;
        private double operand2;
        private boolean decimalPoint;
        private double result;
    }
}
