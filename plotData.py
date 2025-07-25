import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def pieBar(originFrame, amountType, ax, fig):
	"""
	Shows both a pie chart and a bar chart in one panel
	:param originFrame: Data to plot
	:param amountType: Name of the data being plotted
	:return: void
	"""
	barChart( ax, originFrame, amountType )
	pieChart( ax, originFrame, amountType )

	plt.show()

def pieChart(ax, originFrame, amountType):
	"""
	Plots the data on a pie chart
	:param ax: axis
	:param originFrame: Data to plot
	:param amountType: Name of the data being plotted
	:return: void
	"""
	categories = originFrame.columns.tolist()
	categories.pop(0) # removes the months column
	values = []

	for column in categories:
		values.append(abs(originFrame[column].cumsum().sum()))

	ax[1].pie(values, labels=categories, autopct='%.2f %%')
	ax[1].set_title( f'{amountType} Overall by Category' )

def barChart(ax, originFrame, amountType):
	"""
	Plots the data on a bar chart
	:param ax: axis
	:param originFrame: Data to plot
	:param amountType: Name of the data being plotted
	:return: void
	"""
	labels = originFrame['Months']
	x = np.arange( len( labels ) )  # the label locations
	width = 1 / len( originFrame.columns.tolist() )  # the width of the bars
	multiplier = 0

	for column in originFrame.columns.tolist():
		if column != 'Months':
			offset = width * multiplier
			rects = ax[0].bar( x + offset, abs( originFrame[column] ), width, label=column )
			ax[0].bar_label( rects, padding=3 )
			multiplier += 1

	ax[0].set_ylabel( 'Amounts (usd)' )
	ax[0].set_title( f'{amountType} per Month' )
	ax[0].set_xticks( x + width, labels )
	ax[0].legend()

def plotNextSixMonths(originFrame, futureDates, allPredictions, accountColumns, ax, fig):
	"""
	Plots out what is predicted for the next 6 months
	:param ax:
	:param fig:
	:param originFrame: The original data
	:param futureDates: The next 6 months
	:param allPredictions: All predicted values
	:param accountColumns: column names of the accounts
	"""
	for i, column in enumerate(accountColumns):
		ax[0].plot( originFrame['Dates'], originFrame[column], '.-', label=f'{column} Actual' )
		ax[0].plot( futureDates, allPredictions[i], '.-', label=f'{column} Prediction' )

	ax[0].xaxis.set_major_locator( mdates.MonthLocator() )
	ax[0].xaxis.set_major_formatter( mdates.DateFormatter( '%b %Y' ) )
	fig.autofmt_xdate()

	ax[0].legend()
	ax[0].set_xlabel( 'Date' )
	ax[0].set_ylabel('Amount (usd)')
	ax[0].set_title( f'Account Forecast Over Time' )
	ax[0].grid( True )