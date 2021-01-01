This project currently prices options in discrete time. It uses a N-period 
binomial model with a market that has a bank with interest rate r and a stock 
with initial stock price S_0. Included is code to calculate the number of stocks
held in the replicating portfolio at any given time and also the value of a 
portfolio holding securities (S^0, S^1, ..., S^n) with quanities
(c^1, c^2, ..., c^n).

Types of securities supported:
 - Bank
 - Stock
 - European Call
 - European Put
 - European Straddle
 - American Call
 - American Put
 - American Straddle
 - Down and In Barrier
 - Up and In Barrier
 - Down and Out Barrier
 - Up and Out Barrier

Space for future improvement: This code has room to become faster and more 
encompassing of other securities and include features like finding risk neutral
measures in a market that contains securities (S^0, S^1, ..., S^n).

Securities not yet supported:
 - Balloon Options
 - Binary Options
 - Chooser Options
 - Bermuda Options
 - Look-Back Options
 - Asian Call
 - Asian Put
 - Basket Options
 - Extendable Options
 - Spread Options
 - Shout Options
 - Range Options
 - Quantity Adjusting Options
 - Compound Options

List of options: https://www.investopedia.com/terms/e/exoticoption.asp