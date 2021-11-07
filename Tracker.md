



### Focus 

* The focus of this part is to create a page that displays the details of each listing and allows users to place bids on them.*


####In Progress
- display auction listings based on selected category
- bid should only be added if the bid is greater or equal than the starting value and greater than highest bid
- only auctions that are not closed should be displayed
- creator of an auctions should be able to close an auction
- if a bid is closed, no comments should be allowed.
- if a bid is closed, no new bids should be allowed.
- If a bid is closed, the owner should not be able to close it again
- The owner should be able to see the details of the winner of a bid
- a signed in user should be able to see if the won a bid
- The owner of the bid should not be able to bid 
- The owner of the bid should not be able to comment on their bid
- once an auction is closed, remove all watchers from that bid



####Done
- Added the WatchList model that captures all active listings a user is watching.
- Added the highest bid status to the Bid model to mark if a bid is the highest for an active listing.
- Added the closed status to the Listing Model to mark when a bid is closed.
- Impelemented a view and template for displaying the details of an active auction listings and enable features based on whether the user is logged in or not.
- Implemented the feature to allow logged in users bid on an auction item
- Implemented a feature to allow logged in users comment on an auction item and see the comments of other users
- Signed in users can add a listed auction item to their watchlist
- Signed in users can remove a listed auction item from their watchlist it's there.
- Signed in users can view a list of items in their watch list
- All users can visit the categories page to view the list of all available categories.
- User can click on a category and view all items in that category

