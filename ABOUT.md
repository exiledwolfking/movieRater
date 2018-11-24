This is an application that stores movie and tv show reviews via an sms interface.

There are multiple actions a user can make:
1) Create a review
2) Delete a review
3) View previous reviews
4) View personal averages of tv shows across all seasons
5) View application averages of tv shows or movies (averages updated once an hour at the start)
6) View your rating of a specific review


The commands for the following are (Note: braces only indicate a grouping in this documention, not an actual character to enter):  
1.1 Creating movie option) {movie name} {rating integer or decimal 0.0 - 10.0}  
1.2 Creating movie option) {rating integer or decimal 0.0 - 10.0} {movie name}  
1.3 Creating tv show option) {show name} {season int} {episode int} {rating decimal}  
1.4 Creating tv show option) {show name} {rating decimal} {season int} {episode int}  
1.5 Creating tv show option) {season int} {episode int} {rating decimal} {show name}  
1.6 Creating tv show option) {season int} {episode int} {show name} {rating decimal or int}  
1.7 Creating tv show option) {rating decimal or int} {show name} {season int} {episode int}  
1.8 Creating tv show option) {rating decimal} {season int} {episode int} {show name}  

2.1 Delete movie option) delete review {movie name}  
2.2 Delete movie option) delete {movie name without delete as first word}  
2.3 Delete tv show option) delete review {season} {episode} {tv show name}  
2.4 Delete tv show option) delete review {tv show name} {season} {episode}  
2.5 Delete tv show option) delete {season} {episode} {tv show name}  
2.6 Delete tv show option) delete {tv show name without delete as first word} {season} {episode}  
2.7 Delete tv show option NOTE: Deletes all reviews for that show) delete {tv show name without delete as first word}  
2.8 Delete tv show option NOTE: Deletes all reviews for that show) delete review {tv show name}  

3.1 View previous review option) previous review  
3.2 View previous review option) last review  
3.3 View previous reviews option up to 20) previous {int <= 20 | optional} reviews  
3.4 View previous reviews option up to 20) last {int <=20 | optional} reviews  
3.5 View highest rated review) highest review
3.6 View lowest rated review) lowest review
3.7 View previous reviews up to 20 sorted by rating descending) {int <= 20 | optional} highest reviews  
3.8 View previous reviews up to 20 sorted by rating ascending) {int <= 20 | optional} lowest reviews  
3.9 View previous reviews up to 20 sorted by rating descending) {int <= 20 | optional} highest  
3.10 View previous reviews up to 20 sorted by rating ascending) {int <= 20 | optional} lowest  


4.1 View personal tv show average) my average of {tv show name}  
4.2 View personal tv show average) {tv show name}  

5.1 View application movie average) average of {movie name}  
5.2 View application tv show average) average of {tv show name}  

6.1 View your rating of movie review) {movie name}  
6.2 View your rating of tv show review) {tv show name} {season} {episode}  
6.3 View your rating of tv show review) {season} {episode} {tv show name}