import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# add heading of the website
st.write("""
	
	# Compound Interest Calculator

	See how your savings and investment account balances 
	can grow with the magic of compound interest

	""")

# create a side bar for user input parameters
st.sidebar.header('User Input Parameters')

# function to initialize user input parameters
def user_input_params():
	# create a number input widget to store the APY
	rate_of_return = st.sidebar.number_input('Estimated rate of return (%)', value=4.5)

	# create a number input widget to store initial deposit
	starting_amt = st.sidebar.number_input('Initial deposit', value=1000)

	# create a number input widget to store the contribution amount
	money_to_add = st.sidebar.number_input('Contribution amount', value=100)

	# create a select box widget to select contribution frequency
	contribution_freq = st.sidebar.selectbox('Contribution frequency', 
						options = ['Daily', 'Monthly', 'Quarterly', 'Annually'],
						index=1)
	
	# convert contribution frequency to its numeric equivalent
	if contribution_freq == 'Daily':
		times_compounded = 365
	elif contribution_freq == 'Monthly':
		times_compounded = 12
	elif contribution_freq == 'Quarterly':
		times_compounded = 4
	else:
		times_compounded = 1


	# create a number input widget to store the years of growth
	yrs = st.sidebar.number_input('Years of growth', value=2)

	# add all variables used for the compound interest equation into a dictionary
	data = {'Rate of return': rate_of_return,
			'Initial deposit': starting_amt,
			'Contribution amount': money_to_add,
			'# of times compounded per year': times_compounded,
			'Years of growth': yrs}

	# convert the dictionary to a dataframe
	params = pd.DataFrame(data, index=[0])

	return params

# initialize the parameters in the side bar
params = user_input_params()

# create a header on the main page for the user input parameters
st.subheader('User Input Parameters')

# show the input parameters
st.write(params)

# calculate the change in the principal amount with simple interest
def calc_contributions(params):
	# store the principal amount
	P = params.loc[0, 'Initial deposit']
	# store the contribution amount
	C = params.loc[0, 'Contribution amount']
	# store the number of times compounded per year
	n = params.loc[0, '# of times compounded per year']
	# store the number of years
	t = params.loc[0, 'Years of growth']

	# initialize an empty dataframe to store the total amount of money over time
	total_contributed = {'Year': [],
						 'Total Contributed': []}

	# for each year,
	for yr in range(1, t+1):
		# calculate the total amount of money after compounded interest
		final_amt = P+C*n

		# add this to the dictionary
		total_contributed['Year'].append(yr+2024)
		total_contributed['Total Contributed'].append(final_amt)

		# update the principal amount
		P = final_amt
		
	# convert dictionary to a dataframe
	total_contributed= pd.DataFrame(total_contributed)

	return total_contributed

# calculate the total money added to account
without_interest = calc_contributions(params)

# calculate the change in principal amount with compound interest
def compound_interest(params):
	# store the principal amount
	P = params.loc[0, 'Initial deposit']
	# store the contribution amount
	C = params.loc[0, 'Contribution amount']
	# store the number of times compounded per year
	n = params.loc[0, '# of times compounded per year']
	# store the annual interest rate as a decimal
	r = params.loc[0, 'Rate of return']/100
	# store the number of years
	t = params.loc[0, 'Years of growth']

	# initialize an empty dataframe to store the total amount of money over time
	money_compounded = {'Compound Interest': []}

	# for each year,
	for yr in range(1, t+1):
		# calculate the total amount of money after compounded interest
		final_amt = P*(1+r/n)**n + C*((1+r/n)**n-1)/(r/n)

		# add this to the dictionary
		money_compounded['Compound Interest'].append(round(final_amt, 2))

		# update the principal amount
		P = final_amt

	# convert dictionary to a dataframe
	money_compounded = pd.DataFrame(money_compounded)

	return money_compounded

# calculate the total money in account after compound interest
with_interest = compound_interest(params)

# concatenate the dataframes
summary = pd.concat([without_interest, with_interest], axis=1)

# create a scatter chart showing the change in money 
def summarize_results(summary):
	# create an empty figure
	fig = go.Figure()

	# show the change in money contributed over time
	fig.add_trace(go.Scatter(x = summary['Year'], y = summary['Total Contributed'],
				  mode = 'lines+markers', 
				  name = 'Total Contributed'))

	# show the change in money with compound interest
	fig.add_trace(go.Scatter(x = summary['Year'], y = summary['Compound Interest'],
				  mode = 'lines+markers',
				  name = 'Compound Interest'))

	fig.update_layout(xaxis_title = 'Year',
					  yaxis_title = 'Amount ($)')

	return fig


# create the scatter plot summarizing the change in money through various methods
summary_fig = summarize_results(summary)

# create a subheading for the graph
st.subheader('Total Balance')

# show the figure in streamlit
st.plotly_chart(summary_fig)

# show the results at the end of the time period
st.subheader(f'Final amount after {summary.iloc[-1, 0]} years:')
st.write(f'\u2022 Total contributed: ${summary.iloc[-1, 1]}')
st.write(f'\u2022 With compound interest: ${summary.iloc[-1, 2]}')
st.write(f'\u2022 With compound interest, you will have gained ${round(summary.iloc[-1, 2] - summary.iloc[-1, 1], 2)} from passive income')
