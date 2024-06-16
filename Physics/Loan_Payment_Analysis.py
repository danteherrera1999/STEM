from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import numpy as np

"""
This script shows the potential gains and losses of paying for college up front v.s. taking out loans and investing.
Because the interest paid on a loan is acting on a diminishing principal, the interest lost is capped, while interest gained on investments is not.
This does not show the comparison of investing in stocks as that is highly variable, but it does show that over a large enough term, it is more cost effective
to take out a loan (federal fixed rate as of the time of making this script is 5.5%) and put your money in a high yield savings account. Of course, APYs can change
and this does not show the whole story, but barring market downturn, it could be a better option to take out student loans than to pay up front.
"""



r_loan = 5.5 / 100 # Loan interest rate from federal gov
r_tax = .24 + .049 # Based on my current federal and state tax bracket

loan_terms = np.array([10,25]) # years
loan_terms_months = loan_terms * 12
loan_amount = 30000
# Monthly payment calculation
M = loan_amount * (r_loan/12) * (1 + r_loan/12) ** loan_terms_months / ((1 + r_loan/12)**loan_terms_months - 1)

# Calculate monthly amoritization
I_m = [np.repeat(r_loan * loan_amount / 12,2)]
for i in range(1,loan_terms_months[1]):
	I_m.append(r_loan/12*(loan_amount + np.sum(I_m,axis=0) - M*i))
I_m = np.array(I_m).T
I_m = np.where(I_m>0,I_m,0)
I_m = np.array([np.sum(I_m[:,:i],axis=1) for i in range(I_m.shape[1])]).T

# Interest gained on high yield savings account as a function of APR and uncle sam's cut
interest_gained = lambda n,r_hys: loan_amount * ((1 + r_hys/100/12) ** n - 1) * (1 - r_tax)

# Instantiate rate slider
d = np.arange(loan_terms_months[1])
fig,ax = plt.subplots()
ax_rate = fig.add_axes([0.125, 0.05, 0.77, 0.03])
rate_slider = Slider(ax=ax_rate,label='HYS APR',valmin=0,valmax=15,valinit=4.5)

# Instantiate Plots
ax.set_title('Interest Paid to Federal Loan vs Interest Gained from High Yield Savings')
ax.plot(d/12,I_m[0],'--',label='Interest Paid on 10 Year Loan')
ax.plot(d/12,I_m[1],'--',label='Interest Paid on 25 Year Loan')
hys_line, = ax.plot(d/12,interest_gained(d,4.5),label='Interest Gained From High Yield Savings (After Tax)')
ax.set_ylabel('Dollars')
ax.set_xlabel('Time (years)')
ax.set_ylim(0,interest_gained(12*25,rate_slider.val))
ax.legend()

# Set up function to update plot on slider change
def update(i):
	# Redraw gains plot
	hys_line.set_data(d/12,interest_gained(d,rate_slider.val))
	# Adjust y axis range to maximum value displayed
	ax.set_ylim(0,max(I_m[1,-1],interest_gained(12*25,rate_slider.val)))

rate_slider.on_changed(update)
plt.show()





