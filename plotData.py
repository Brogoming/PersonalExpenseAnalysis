import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def tableView(originDataFrame, masterFrame):
	"""
	Creates a table frame to see the contents of the data frame
	:param originDataFrame: Original data frame before any edits
	:param masterFrame: Frame to add the table to
	"""
	# Clear the frame first (if reloading data)
	for widget in masterFrame.winfo_children():
		widget.destroy()

	# Create a frame for Treeview + scrollbars
	treeFrame = ttk.Frame(masterFrame)
	treeFrame.pack(expand=True, fill="both")

	# Create scrollbars
	scrollY = ttk.Scrollbar(treeFrame, orient="vertical")
	scrollX = ttk.Scrollbar(treeFrame, orient="horizontal")

	# Create the Treeview widget
	tree = ttk.Treeview(treeFrame, columns=list(originDataFrame.columns), show="headings", yscrollcommand=scrollY.set,
		xscrollcommand=scrollX.set)

	# Configure scrollbars
	scrollY.config(command=tree.yview)
	scrollX.config(command=tree.xview)
	scrollY.pack(side="right", fill="y")
	scrollX.pack(side="bottom", fill="x")

	# Setup Treeview headings and column widths
	for col in originDataFrame.columns:
		tree.heading(col, text=col)
		tree.column(col, width=100, anchor="center")  # Adjust width as needed

	# Insert DataFrame rows into the Treeview
	for index, row in originDataFrame.iterrows():
		tree.insert("", "end", values=list(row))

	tree.pack(expand=True, fill="both")

def barPieCharts(originDataFrame, amountType, masterFrame):
	"""
	Creates a bar and pie chart to share the same frame
	:param originDataFrame: Original data frame before any edits
	:param amountType: Either Spent or Earned
	:param masterFrame: Frame to add the graphs to
	"""
	fig, ax = plt.subplots(1,2, figsize=(5, 4))
	for widget in masterFrame.winfo_children():
		widget.destroy()

	barChart(originDataFrame, amountType, ax[0])
	pieChart(originDataFrame, amountType, ax[1])

	canvas = FigureCanvasTkAgg(fig, master=masterFrame)
	canvas.draw()
	canvas.get_tk_widget().pack(expand=True, fill="both")

def pieChart(originDataFrame, amountType, ax):
	"""
	Creates a pie diagram for the amount type
	:param originDataFrame: Original data frame before any edits
	:param amountType: Either Spent or Earned
	:param ax: One of the axes to add the frame to
	"""
	categories = originDataFrame.columns.tolist()
	categories.pop(0) # removes the months column
	values = []

	for column in categories:
		values.append(abs(originDataFrame[column].cumsum().sum()))

	ax.pie(values, labels=categories, autopct='%.2f %%')
	ax.set_title( f'{amountType} Overall by Category' )

def barChart(originDataFrame, amountType, ax):
	"""
	Plots the data on a bar chart
	:param originDataFrame: Original data frame before any edits
	:param amountType: Either Spent or Earned
	:param ax: One of the axes to add the frame to
	"""
	labels = originDataFrame['Months']
	x = np.arange( len( labels ) )  # the label locations
	width = 1 / len( originDataFrame.columns.tolist() )  # the width of the bars
	multiplier = 0

	for column in originDataFrame.columns.tolist():
		if column != 'Months':
			offset = width * multiplier
			rects = ax.bar( x + offset, abs( originDataFrame[column] ), width, label=column )
			ax.bar_label( rects, padding=3 )
			multiplier += 1

	ax.set_ylabel( 'Amounts (usd)' )
	ax.set_title( f'{amountType} per Month' )
	ax.set_xticks( x + width, labels )
	ax.grid(True)
	ax.legend()

def plotNextSixMonths(originDataFrame, futureDates, allPredictions, accountColumns, masterFrame):
	"""
	Creates a line chart of each of the accounts and predicts the next 6 months
	:param originDataFrame: Original data frame before any edits
	:param futureDates: List of the next 6 months
	:param allPredictions: List of all the predicted values for the next 6 months
	:param accountColumns: Names of the accounts
	:param masterFrame: Frame to add the graph to
	"""
	fig, ax = plt.subplots(figsize=(5, 4))
	for widget in masterFrame.winfo_children():
		widget.destroy()

	for i, column in enumerate(accountColumns):
		ax.plot( originDataFrame['Dates'], originDataFrame[column], '.-', label=f'{column} Actual' )
		ax.plot( futureDates, allPredictions[i], '.-', label=f'{column} Prediction' )

	ax.xaxis.set_major_locator( mdates.MonthLocator() )
	ax.xaxis.set_major_formatter( mdates.DateFormatter( '%b %Y' ) )
	fig.autofmt_xdate()

	ax.legend()
	ax.set_xlabel( 'Date' )
	ax.set_ylabel('Amount (usd)')
	ax.set_title( f'Account Forecast Over Time' )
	ax.grid( True )

	# Embed the Matplotlib figure into the Tkinter frame
	canvas = FigureCanvasTkAgg(fig, master=masterFrame)
	canvas.draw()
	canvas.get_tk_widget().pack(expand=True, fill="both")