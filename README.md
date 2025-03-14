# PSA Calculator

A Perfect Sensitivity Analyzer (PSA) calculator designed to help gamers find their ideal mouse sensitivity through systematic testing and binary search methodology.

![PSA Calculator Screenshot]([screenshot.png](https://ibb.co/FqbjQX33))

## Description

PSA Calculator is a desktop application that helps users find their perfect mouse sensitivity for gaming. It uses a methodical approach where users test different sensitivity values and choose which feels better, gradually narrowing down to their ideal sensitivity.

## Features

- Clean and modern user interface
- Real-time sensitivity calculations
- Detailed calculation history
- Copy-to-clipboard functionality
- Input validation (0.001 to 100)
- Tooltips for better user guidance
- Interactive buttons with hover effects

## How to Use

1. Launch the application
2. Enter your current sensitivity (between 0.001 and 100)
3. Click "Start Calculation" to begin
4. Test the two provided sensitivity values in your game:
   - Higher value (1.5x your current sensitivity)
   - Lower value (0.5x your current sensitivity)
5. Click the corresponding button based on which sensitivity feels better
6. Repeat the process until you find your perfect sensitivity
7. Click "Found my sensitivity!" when you're satisfied
8. Use the copy button to save your final sensitivity

## Requirements

- Python 3.x
- tkinter (included with Python)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/psa-calculator.git
