# A/B Test Bayesian Approachs

## Overview

A/B Test is one of the crucial points of test your new developments. At this point, Data Analysts or Data Scientists are most of the time using the Traditional A/B Testing Approaches. Statistical Hyphothesis is one of them. Statistically it gives idea 95 of 100 correct answer. It also leave %5 error posibilities jus in case. However, it is a very crucial point that we need to use how well our new implementation worked. 

### Traditional A/B Test

This approachs claims that there are estimated parameters and our aim of testing these parameters of accuracy with Statistical Testes Most of the time it works fine with Hyphothesis Test.
However, without knowing a parameter, Testing that prameter is not a good idea.

### Non - Parameteric Statistical Test (Chi-Square Test)

In order to use unknown estimated parameter, we might ork with Non-Parametric Statistical Testes. However, this is going to give a general answer

### Bayesian Approaches

Rather than frequentist methods with using estimated parameters, Bayesian Approach allows us to calculate parameters without using estimated values. This works with Bayesian Model with given priors try to find the posterior.

Priors have 2 term.
### 1. P(Q): 
One of them is parameter of probabilty which is P(Q) and it has Beta Distribution. 

### P(X | Q)
The another term is P(X | Q). 
With given X data conditon, probability of appearing Q parameters. 
Let`s explain this with an coin toasting;
- X will be Binary (Head or Tails). ratio will be 1/2 for each instance. Q = 1/2.
- We toast the coin 5 times each test of toasting coins will have to outputs which are head or tail. 
- X = [head, head, head, tails, tails]. What is the probability of each instance of Toasting coin?
- The answer is X has Bernolli Distribution. P(X | Q) will be the Bernolli Probabilty Density Fonction (PDF)
Let`s we implement an A/B Test on web page of user Interface of a button of color.
- First user land your page with test data set. New Developed feature has seen the user. 
- Click!!!
- Bayesian approach our parameters are updates with a = click count, b = non-click count. In This case a = 1, b = 0
- Now, We need to calcualte X given data set what is the Q parameter. With Beyes Theorem, it is possible

### Assumption Of Distributions:


