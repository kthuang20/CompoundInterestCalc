# Compound Interest Calculator

The inspiration for this user interactive calculator was based off of https://www.nerdwallet.com/calculator/compound-interest-calculator. 

I wanted to created this calculator because I wanted to learn the how compound interest works rather than simply plugging in the numbers into this website.

This web application allows the user to adjust the same parameters as on the website:
* Initial deposit
* Contribution amount
* Contribution frequency
* Years of growth
* Estimated rate of return

It also shows a scatter plot showing the total balance after each year with and without compound interest.

Adjusting any of the parameters will automatically adjust the results in the figure.

This web application was built in Python using the following libraries:
* streamlit 
* pandas
* plotly

This web application can be run locally by performing the following command in the terminal:
```bash
streamlit run https://github.com/kthuang20/CompoundInterestCalc/blob/master/interest_calc.py
```