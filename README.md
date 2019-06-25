# Book-Recommender
This application will recommend books based on the collaborative filtering
# Description
The application has already trained on the data. You just have to download all the code and run the book-recommender.py file and 
It will start recommending books.
The formula used for recommendation is pearson coefficient formula. The application selects a random user(lets say userA)
and checks the correlation value with other users. Pick the user having maximum correlation value and finds all the books 
that userA has not read yet. Then predict the rating of all these books and recommend the books with predicted rating >3.0.

Note:
Every time you run the program it selects new random user to whom it recommends the books.


