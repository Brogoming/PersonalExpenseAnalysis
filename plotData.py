import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plotAccounts(originFrame):
	fig, ax = plt.subplots(figsize=(10,5))
	for column in originFrame.columns.tolist():
		if 'Account' in column:
			ax.plot(originFrame['Dates'], originFrame[column], '.-',label=column)

	ax.xaxis.set_major_locator( mdates.MonthLocator() )
	ax.xaxis.set_major_formatter( mdates.DateFormatter( '%b %Y' ) )
	fig.autofmt_xdate()

	plt.title('Accounts Overtime')
	plt.xlabel('Dates')
	plt.ylabel('Amount (usd)')

	plt.legend()
	plt.show()