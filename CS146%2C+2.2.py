
# coding: utf-8

# # Call center data modeling
# 
# You are advising a client on the number of call center agents they need to handle their customer support load. We start by modeling the number of phone calls we expect to come into the call center during each hour of the day.
# 
# You are provided with a data set of the intervals between phone calls arriving during one day. Each value is a time in minutes indicating the amount of time that passed between receiving two consecutive phone calls.
# 
# ## Loading the data

# In[1]:

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


# In[2]:

# Load the data set containing durations between calls arriving at the call center.
# All values are in minutes.
waiting_times_day = np.loadtxt('call_center.csv')


# In[4]:

print('Size of data set:', len(waiting_times_day))
print('First 5 values in data set:', waiting_times_day[:5])
print('Sum of data set:', sum(waiting_times_day))


# Since the values are intervals between calls measured in minutes, this means
# 
# * we assume the first call happened at 00:00 (midnight),
# * the second call happened at about 00:05 (5.36 minutes after midnight),
# * the third call happened at about 00:07 (5.36 + 2.48 minutes),
# * the fourth call happened at about 00:15, etc.
# 
# When we sum the values, we get about 1440 minutes (1 day).

# You are told that the number of calls arriving varies quite a lot, depending on which hour of the day it is. The smallest number of calls usually occur around 3am or 4am. Most calls usually come in between 11am and 1pm.
# 
# ## Data pre-processing
# Since we expect different call rates during different hours, we split the data set into 24 separate series — one for each hour of the day.

# In[5]:

# Split the data into 24 separate series, one for each hour of the day
current_time = 0
waiting_times_per_hour = [[] for _ in range(24)]  # Make 24 empty lists, one per hour
for t in waiting_times_day:
    current_hour = int(current_time // 60)
    current_time += t
    waiting_times_per_hour[current_hour].append(t)

for hour, waiting_times_hour in enumerate(waiting_times_per_hour):
    print('%02i:00-%02i:00 - %i calls' % (hour, hour + 1, len(waiting_times_hour)))


# ## Task 1: Plot the number of calls per hour
# Use Matplotlib to visualize the number of calls that arrive during each hour of the day. The numbers are shown in the output above. You should find an appropriate way to visualize it.

# In[12]:

calls = []
for i in waiting_times_per_hour:
    calls.append(len(i))
plt.figure(figsize=(8, 4))
plt.plot(calls)
plt.show()


# ## Task 2: Plot a histogram of the durations for one hour
# Take the data for the 11th hour (so between 11am and 12pm) and plot a histogram showing the distribution over waiting times between calls during that hour.

# In[17]:

eleven = waiting_times_per_hour[11]
plt.hist(eleven)
plt.title('Distribution Over Waiting Times')
plt.show()


# ## Task 3: Guess the distribution
# What type of distribution best represents the data in your histogram?
# 
# * Identify a type of distribution.
# * Guess what the parameters of the distribution are.
# * Plot the pdf of your best guess on top of your histogram, to see if they match.
# * Important: you have to normalize your histogram so that it will have the same vertical scale as the plot of the pdf. You can normalize a histogram by using the argument `normed=True` in the `hist` function.

# The Gamma (or exponetial, to be more precise) distribution is approprite for modeling waiting times because it is the distribution of a sum of independent exponential random variables, and the exponential distribution is a natural model for individual waiting times, due to its memorylessness.
# To identify the parameters, I simply looked at the rate of change of the histigram and found out that the scale parameter should be around 10 to closely fit the distribution.

# In[74]:

gamma = stats.gamma(a=1., scale=1/10.3)
# Plot the pdf
plt.figure(figsize=(8, 4))
x = np.linspace(0, 1)
plt.hist(eleven, normed = True)
plt.plot(x, gamma.pdf(x))
plt.show()

