import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import matplotlib.patches as mpatch
from matplotlib.patches import FancyBboxPatch
import numpy as np
import keyboard  # using module keyboard
import threading
from datetime import datetime

from firebase import firebase
firebase = firebase.FirebaseApplication('https://python-firebase-70524.firebaseio.com/', None)

#file io
#fileStore = open('charityVotes.txt')

#..
label = ['Noah\'s Ark Children\'s Hospice', 'Mind', 'Homeless Action in Barnet']

no_votes = [
    17, 10, 97
]

money = [0, 0, 0]

maxValue = 0;

def getData():
	#DB
	#result = firebase.get('/python-firebase-70524/users/', '')
	no_votes[0] = firebase.get('/python-firebase-70524/users/', 'ch0002')
	no_votes[1] = firebase.get('/python-firebase-70524/users/', 'ch0001')
	no_votes[2] = firebase.get('/python-firebase-70524/users/', 'ch0003')
	#File...........
	#print(no_votes)
	maxValue = max(no_votes[0], no_votes[1])


def getVote(self):
	if self.key == 'a': 
		no_votes[0] += 1
		firebase.put('/python-firebase-70524/users/','ch0001', no_votes[0])
		print('You pressed a')
	elif self.key == 'w':
		no_votes[1] += 1
		firebase.put('/python-firebase-70524/users/','ch0002', no_votes[1])
		print('You pressed w')
	elif self.key == 'd': 
		no_votes[2] += 1
		firebase.put('/python-firebase-70524/users/','ch0003', no_votes[2])
		print('You pressed d')
	#print(no_votes)
	#updateFile()


#no longer in use; put in if statement 'getVote()' to make faster
def updateDB():
	firebase.put('/python-firebase-70524/users/','ch0001', no_votes[0])
	firebase.put('/python-firebase-70524/users/','ch0002', no_votes[1])
	firebase.put('/python-firebase-70524/users/','ch0003', no_votes[2])
	print('Record Updated')

def updateFile():
	lines = fileStore.readlines()
	lines[0] = no_votes[0]
	lines[1] = no_votes[1]
	lines[2] = no_votes[2]
	out = open('charityVotes.txt', 'w')
	out.writelines(lines)
	out.close

def plot_bar_x():
	#print(no_votes)
	plt.clf()
	money[0] = no_votes[0] * 5
	money[1] = no_votes[1] * 5
	money[2] = no_votes[2] * 5
	ax2 = plt.subplot(1, 2, 1)
	barlist = ax2.bar(label, money)
	barlist[0].set_color('b')
	barlist[1].set_color('g')
	barlist[2].set_color('r')

	for rect in barlist:
		height = rect.get_height()
		plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom', fontsize=12)
	
	bb = mtransforms.Bbox([[0.3, 0.4], [0.7, 0.6]])
	p_fancy = FancyBboxPatch((2.5, bb.ymin), 0.3, 2000, boxstyle="round,pad=0.1", fc=(1., .8, 1.), ec=(1., 0.5, 1.))
	ax = plt.subplot(1, 2, 2)
	ax.add_patch(p_fancy)
	ax.text(0.1, 0.8, r' boxstyle="round,pad=0.1"', size=10, transform=ax.transAxes)
	
	size = plt.figure(1).get_size_inches()*plt.figure(1).dpi
	ylim = plt.gca().get_ylim()
	top = (ylim[1]/(0.91*size[1]))*size[1];
	print(top)
	maxValue = max(max(money[0], money[1]), money[2])
	plt.text(2.8, top, 'Raised last year', fontsize=14, bbox={'facecolor': '#888888', 'alpha': 0.5, 'pad': 10})
	plt.subplots_adjust(left=0.05, right=0.8)

	plt.ylabel('Money Raised', fontsize=8)
	plt.title('To vote, please email engagement@mdx.ac.uk with the name of your chosen charity', fontsize=20, ha='center')
	plt.suptitle('NSS Charity Donations', fontsize=26)
	plt.draw()


def vote_and_plot(self):
	getVote(self)
	getData()
	plot_bar_x()

def rep():
	threading.Timer(0.8, rep).start()
	getData()
	plot_bar_x()

def dailySave(self):
	if self.key == 'q':
		firebase.put('/python-firebase-70524/votes' + datetime.date(datetime.now()).strftime('%d_%m_%Y') + '/','ch0002', no_votes[0])
		firebase.put('/python-firebase-70524/votes' + datetime.date(datetime.now()).strftime('%d_%m_%Y') + '/','ch0001', no_votes[1])
		firebase.put('/python-firebase-70524/votes' + datetime.date(datetime.now()).strftime('%d_%m_%Y') + '/','ch0003', no_votes[2])

def sav(self):
	dailySave(self)

#main run
getData()
rep()
plt.figure(1).canvas.mpl_connect('key_press_event', sav)
plot_bar_x()
plt.get_current_fig_manager().window.state('zoomed')
plt.show()
