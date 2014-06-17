# MMA Rankings Using Elo Rating System

The scripts in this folder contain the entire process of cleaning and producing
Elo Ratings from the records of Lightweight MMA fighters as found on their
corresponding Wikipedia pages.


## Algorithm For Obtaining Fighter Records
Data was scraped using the python script with the following algorithm.

### Initiation Portion

- Initiate with one lightweight mma fighter (in this case Nate Diaz).
- Initiate four sets
	1. An all fighters observed set (initiated with Diaz)
	2. A set of lightweight fighters
	3. A set of fighters whose status needs to be checked (initiated with Diaz)
	4. A set of fighters who have been checked
	
### Iterative Portion

- Randomly select one fighter from the need to be checked list.
- If that fighter is marked as a lightweight fighter put them in the lieghtweight fighters set.
- If that fighter also has more than ten fights then...
	- Record all matches
	- Grab any hyperlinks which link to other fighters pages.
	- Place them in the need to the all fighters observed set.
- Move the randomly selected fighter to the finished set. 
- The need to check set is now {All fighters} - {finished}
- Repeat for 10000 iterations or until the need to check set is empty.