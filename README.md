# A/B Test Bayesian Approaches
### Overview
### Dependencies
### Data Sets
### Parameters
### How it works?
### Example
### Visualizations

## Overview

A/B Test is a method that allows us to compare two or more samples at the same time. It helps companies better to measure their improvement of products of changes on users' attributes. It could be any web page of user interface development or an Advertisement Campaign running from the Marketing Department. The way of running an AB Test is splitting versions of what we are going to measure. For instance, if we running a web page of any bottom color, show A sample to version 1, B sample to version 2. Another example, you are running a very costly campaign. The change cost range assigns a new version of campaign to a treatment sample of users and compares the results of the control and treatment of users attributes.

Most of the time AB Test of samples (Control and Treatment Groups) is chosen with Random Sampling. However, this can cause a problem when we are running a very costly test. Let`s say that we updated our campaign to a very costly campaign and assigned it to the Treatment Group of users. We probably see the huge Conversions in the first couple of days. However, this gap will decrease in the next days. This causes a problem when we try to measure the actual difference in a couple of days and our costs are increasing even we haven not been sure yet about the test results. In order to find more accurate and faster results, 2 options can be implemented on Traditional AB Tests
- 1. Estimated Parameters On Traditional Test
- Traditional AB Test Approaches will help us to find the difference of Control / Treatment Group but Bayesian Approach will directly measure the parameters without using estimated parameters. In this example parameter is advertisement click ratios between each Group. On the first day of the result, the Traditional Test of output “ Treatment - Control Conversion of Ratios is range between X and Y”. However Bayesian Approaches will answer Point values, not a range. That will help us more than Traditional Statistical Test when it is a costly test. 
- 2. Compare Sub Groups of users on Control and Treatment
- Comparing the whole sample can not be a good idea to find the difference. We are running AB Test on Users of attributes. It is better to use customer segmentation in order to compare segmented Group Samples.RFM Customer Segmentation is a useful segmentation method which can be implemented on ABTest

### Traditional A/B Test

This approaches claims that there are estimated parameters and our aim of testing these parameters of accuracy with Statistical Testes Most of the time it works fine with Hypothesis Test.
However, without knowing a parameter, testing that parameter is not a good idea. Two-Sample T-Test is Statistical Test it can be implemented. 

H0: There is no difference between the Control and Treatment Tests significantly. If there a significant difference occurs, The probability of it is less than 0.05 when we assign confidence level 0.95. The Conversion Ratio will be the range of the confidence interval.

H1: There is a significant difference between Control and Treatment groups. Statistically, it can not be ignored.

### Non - Parametric Statistical Test (Chi-Square (χ2) Test) 

In order to use unknown estimated parameter, we might work with Non-Parametric Statistical Testes. However, this is going to give a general answer

### Bayesian Approaches

Rather than Frequentist methods with using estimated parameters, Bayesian Approach allows us to calculate parameters without using estimated values. This works with Bayesian Model with given priors try to find the posterior.

Priors have 2 term.
### 1. P(Q) 
One of them is parameter of probabilty which is P(Q) and it has Beta Distribution. 

### 2. P(X | Q)
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
- Now, We need to calculate X given data set what is the Q parameter. With Beyes Theorem, it is possible.

### Assumption Of Distributions:
The assumption of Bayesian Approach is related to priors and posteriors. With given parameter, sample of data X of distribution will be Bernolli Distribution (P(X | Q)). This trerm is Bernolli Distributed. It has combinotion of two choices of Q parameter "0 or 1", "True or False". Another term which is parameter of estimated value (P(Q)) when it is sampled many times, Max,mum likelihood Theorem will be worked at it will shape as Beta Distribution. P(Q) values provide two main assumption of beta distribution 1st) Every each P(Q) values are independent. 2nd) P(Q) values are distributed around [0,1]. 
Bernolli And Beta Distribution are going to be the Priors.
Multiplication of Bernolli And Beta Distribution are going to be the Posteriors and it will be Beta Distributed when Likelihood Estimation is worked.
