# Path finder
## Task
### Mathematical formulation 
To find the most valuable path through a graph when it's not enough time to visit all the locations, 
locations have different value points, and some locations have additional conditions regarding the state - 
is accessible or not.
### Real-life formulation
There is world map from board game "Arkham Horror LCG", campaign "Scarlet Keys".
Every location is assigned some "value" that counts in total path value when you visit the location.
To visit the location you have to pay 1 time unit.
You can also not to stop at the location. In such a case neither time counts time nor value is earned.
Every path between 2 directly linked locations also cost "1 time".
You could visit every location only one time but there is no limitations for transit.
Red marked locations are locked for visiting until certain amount of time units will pass, transit is possible any time.
Some locations have additional conditions to become accessible to visit.
Goal: find path to maximize total earned value in a limited time.


## Solution 
Since classical shortest paths algorithms like Dijkstra's algorithm could not be applied, 
I decided to use recursion algorithm and my main goal was to reduce run time. 

### Version 1: To write funcs for raw data handling and recursion algorithm realization
I needed to write a code to build the best path for 30 time units when the map includes 31 locations
(graph vertices) and 68 connections (graph edges). But already with 17 locations, 27 connections and 
16 time units I had 1 hour runtime. So I added func to discard each path that has no chance to earn 
current max value. It helps to stop calling recursion earlier. 
Execution time decreased dramatically but still not enough. 

### Version 2: Rewrite to class-based design
On 3 month I came back to this code. Who wrote this awful spaghetti code?? - I was horrified! 
I applied OOP, but .. ups. To initialize the objects - it's so time-consuming operation. 
So I used Object pool pattern and - wow - effect was awesome - but still not enough.

### Version 3: Multiprocessing 
I need to apply multiprocessing to my recursion algorithm!  
(Disclaimer: don't do this in real life!) Just kidding, but it was small brain explosion :)
I used manager.Value to provide a piece of shared memory for my processes was able to share 
current best value and stop calling recursion earlier. It helps. You can see the runtime difference
on the plot below. But it still not enough :)  So I hope ... to be continued) 

Thanks for your time! 
