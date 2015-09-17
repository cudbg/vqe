## Goals

Is SQL just text?  No!  That's just a _textual form_ of query specification.
Our goal is to take a look at some historically important projects that use
visual forms of query specification, understand their strong and weak points, and
create our own attempt of improvements.

As a first pass, we need to

1. do some background reading
1. brainstorm 
  * what interactions would be effective for complex queries
  * whether showing/visualizing query results during query formulation can help
1. implement prototypes

## Reading

Background Reading (read in order)

* [picasso](./docs/reading/picassoavi.pdf): One of the original visual query languages!
  * It's really long, just skim Section 5 to get a feel of how it works
* [polaris](./docs/reading/polaris.pdf): Spawned Tableau, a 7 billion dollar company!
  * Read Sections 3 and 4, which describes the key language features
* [gesturedb](./docs/reading/gesturedb.pdf): focus on Sections 1, 3 and skim 5
  * see the video on the [website](http://interact.osu.edu/gesturedb/)
* [queryviz](./docs/reading/queryviz.pdf) 
  * Section 2 is what's important
  * see [Wolfgang's presentation on youtube](https://www.youtube.com/watch?v=kVFnQRGAQls)
  * [Play with the queryviz demo](http://queryviz.com/online/)
* [dataplay](./docs/reading/dataplay.pdf) (optional)
  * Focus on:
    * INTRODUCTION
    * QUERYING WITH DATA PLAY
    * DATAPLAY’S GRAPHICAL QUERY LANGUAGE
  * [The demo paper](./docs/reading/dataplaydemo.pdf) may be easier to read
  * see [video of dataplay](https://vimeo.com/45918228)
  * see [dataplay's website](http://db.cs.yale.edu/dataplay/DB/DataPlay.html).  
* [datasquid](http://datasquid.co/)
  * watch the video on their website.



Questions

* What kind of user does each paper imagine?  What is that user trying to do?
* What seem to be useful or good features of each paper?
* What types of queries or expressions or analyses seem tricky,  annoying or impossible to do?
* What other things (for example, data distributions) would be really useful when formulating queries?
* Do you believe their evaluations?



# Below, write progress notes (latest at the top)


### 9/17 

Picasso

* positive points
  * good representation of joins
  * visual emphasis of what attrs you want or don't want
  * question mark telling which attributes you are concern with
  * dropdown menu process is pretty intuitive
    * click on attr, relational operators come up, then select constant/attr
    * like that it reduces your options to valid ones
  * visually separate subqueries
* negative points
  * doesn't scale
    * beyond 3 joins
    * beyond 20 attrs
  * subquery joins are not visually expressed as a join -- or maybe its not a join anyways
  * figure 9: with the loan_no, the ">" positioning is misleading, they are not related
  * would be nice to abstract joins out 
  * predicates are text and floating around
    * elements are not spatially organized in a useful way
  * assumes special hardware

GestureDB

* positive
  * joins seem intuitive 
    * like that the gesture is incremental with recomendations to choose which to join with
    * that it shows the query results
    * the recommendatioons
  * gestures are easy to do and fast to perform
  * sort interface is congruent with sql builder interfaces (click column header to sort)
  * spatially organizing things as you wish
  * scolling tables are nice
  * customize your own gestures
* negative
  * discoverability seems like a problem
  * data density is low
  * doesn't help with deciding on what query to compose
  * only looking at the result, no breadcrumbs in terms of the full query plan
  * need to look at each join pair one by one
  * undo?
  * how to update data?

Polaris

* positives
  * moves away from query syntax
  * great for analyzing data
  * started problem first
  * excellent for high management
    * specifying group by and aggregation functions
    * mapping those to facets marks
* negatives
  * where are joins?
  * where are updates?
  * don't really see the raw data
  * everything else in SQL aka joins, filters, unions, not really well supported

Data play


Properites

* joins visually
* nested queries in a visual manner
  * subquery should be able to interact with values (as set operations) or with sets as join/union/diff operations
* higher level operations 
* i should see my data
  * base data
  * query so far
  * next query
  * how can seeing my data help me construct query fragments?
    * e.g., crossfilter
* mixture of visual/text/forms
  * text: arithmetic, >, <, !=, 
  * "bigger than all of these", universally known operators
  * group by: for each state, show all of their sales

Homework

* create three benchmark queries that are hard to create based on the negative
  aspects of above systems
* propose way to implement/specify them (2 queries minimum)
* list of love-to-haves





###  (date) title

The goal

What you tried

What worked