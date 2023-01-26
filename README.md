# path_finder
Graph traversing (world map from board game "Arkham Horror LCG", campaign "Scarlet Keys"). 
Every location is assigned some "value" that counts in total path value when you visit the location.
Every path between 2 directly linked locations cost "1 time" as well as one location visiting.
You can also not to stop at the location - in such a case you will not pay "1 time" for visiting, you will pay time only for travelling. 
You could "visit" every location only one time but there is no limitations for transit.
Red marked locations are locked for visiting untill certain amoutn of time units will pass, transit is possible any time.
Goal: find path to maximize total earned value in a limited time. 

![IMG_4183](https://user-images.githubusercontent.com/121285272/214615592-b17f9741-9635-4983-97c1-d4883961e20a.jpg)
