import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

"""
This code shows the gains and losses of taking a loan with a few assumption.
It primarily compares 2 scenarios which both assume you have enough to pay off the loan up front and make monthly payments:
		1. You take a loan, invest the loan amount immediately, and make monthly payments towards the loan
		2. You pay the purchase amount instead of taking a loan, and make a contribution to the investment account equal to the monthly payment you would have paid
				had you taken the loan
	The reason only these two options are considered is because you will almost always lose money when taking a loan that you cannot afford up front.
	The aim of this script is to take account of more of the nuances associated with taking a loan such as the tax you will pay on investment gains as well
	as the lost investment potential associated with each monthly payment. This phenomena can be seen when you adjust the loan APR slider. While it may not 
	seem like loan APR would affect investment gains, A higher loan APR means a higher monthly payment, and more lost investment potential. The green line
	reresents the difference between investment gains if you took a loan and if you didnt assuming you invested the money you save by not having a monthly payment.
	Thus the green line will shift even as you adjust loan APR. The default values for the slider are the current federal student loan interest rate as the loan APR,
	and my personal current high yield savings account APR. I chose a high yield savings account because it is less volatile than stocks but there are certainly even more
	consistent options. It is also important to consider risk, which has a different value for every person. This is mostly a tool for me to decide if I want to take student 
	loans for my biosphysics degree or not and is by no means financial advice.
"""

loan_term_years = 30
loan_term_months = loan_term_years * 12
tax_rate = 24+4.7
principal = 300000


M = lambda n,r_l: principal * (r_l/100/12)*(1+r_l/100/12)**n / ((1+r_l/100/12)**n-1)
total_paid = lambda n,r_l: M(n,r_l)*n
interest_paid= lambda n,r_l: total_paid(n,r_l) - principal
total_gained = lambda n,r_g: principal * (1 + r_g/12/100)**n
interest_gained = lambda n,r_l,r_g: ( total_gained(n,r_g) - principal - mpil(n,r_l,r_g) ) * (1-tax_rate/100)

def mpil(n,r_l,r_g):
	m = M(n,r_l)
	tg = np.zeros(n.size)
	for i in range(n[-1]+1):
		tg *= np.where(n>i,1+r_g/100/12,1)
		tg += np.where(n>i,m,0)
	return tg - m*n

d = np.arange(1,loan_term_years*12)

fig,ax = plt.subplots()

# Make a horizontal slider to control the investment APR
ax_r_g = fig.add_axes([0.25, 0.02, 0.65, 0.03])
r_g_slider = Slider(ax=ax_r_g,label='Investment APR',valmin=1,valmax=10,valinit=4.6)

# Make a horizontal slider to control the investment APR
ax_r_l = fig.add_axes([0.25, 0.04, 0.65, 0.03])
r_l_slider = Slider(ax=ax_r_l,label='Loan APR',valmin=1,valmax=10,valinit=5.5)

ax.set_xlabel('Loan Term (years)')
ax.set_ylabel('Dollars')
ax.ticklabel_format(useOffset=False,style="plain")

ln_l, = ax.plot(d/12,interest_paid(d,5.5),c='r',label=f"Net Interest Paid")
ln_g, = ax.plot(d/12,interest_gained(d,5.5,4.6),c='g',label=f"Net Investment Profits")
ax.legend(loc='upper left')
def update(i):
	ip = interest_paid(d,r_l_slider.val)
	ig = interest_gained(d,r_l_slider.val,r_g_slider.val)
	ln_l.set_ydata(ip)
	ln_g.set_ydata(ig)
	ax.set_ylim(0,max(ip[-1],ig[-1]))

r_l_slider.on_changed(update)
r_g_slider.on_changed(update)

plt.show()





