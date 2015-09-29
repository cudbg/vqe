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
* [datatone](http://www.cond.org/datatone.html)



Questions

* What kind of user does each paper imagine?  What is that user trying to do?
* What seem to be useful or good features of each paper?
* What types of queries or expressions or analyses seem tricky,  annoying or impossible to do?
* What other things (for example, data distributions) would be really useful when formulating queries?
* Do you believe their evaluations?

# Design Guidelines

In user interface design, it helps to design within a framework:

* pick a subset of the design parameters
* have a user persona (a story) to ground the design process
* have a set of design principles (~metrics) to evaluate how well the design is

The following are some incomplete thoughts on this:

### Design parameters

* Number of relations
  * small: feasible to search and find relation
  * medium: keyword-like search sufficient to reduce to small set of relations to search through
  * large: impossible to manually look for relation, may not know which relation of candidates to pick
* Number of attributes
  * small: feasible to look through manually
  * medium: feasible to look through if organized and summarized properly
  * large: infeasible if exact column/name is known
* What the user knows
  * The query and the data, but needs to formulate it
  * The intended query result and the data, needs help expressing it
  * What kind of result would be interesting, knows what type of data to expect, 
  * New dataset, looking for something interesting
*  Query complexity
  * Number of relations
  * Attributes picked
  * Number of predicates
  * Set-oriented predicates
  * (Correlated) Subqueries
* anything else?

### User Personas

Scenario: story about user using the system

* concrete, realistic, fictional
* user trying to achieve a goal
* follow how user achieve the goal step by step

Persona: description of a realistic user, their motivations, and their goals

Bob (Tableau persona)

* Marketer, can use excel, doesn't program
* Has a big table of sales data
* modest number (~20) attributes
* wants to look at total sales over time across a number of dimensions (states, seasons, economic indicators)

Joe 

* Can write small python scripts, can write SQL comfortably
* Small number of medical related relations (see medicare dataset medicare aca-compare-20142015)
* Relations have huge number of attributes, all encoded
* Have an idea of the set of query results he would like, but really hard to 
  dig through the relation attributes to get what he's looking for
  * may have to try many similar seeming attributes (CM1, CM2, CM3, ...) to find what he's looking for
* Queries themselves are not too complicated

Sally (expert querier)

* Can write large complex programs
* has a database of ~20 relations
* attributes have long names e.g., "labeler_kwargs.parameter_one"
* very familiar with ~5 of the relations, roughly knows about the result, could figure out by staring at relations long enough
* has a complex nested query across multiple relations 
  * sally knows most of the relations and how the join, but a few she needs to look up
* Will want to run multiple slight variations with different filtering parameters and compare


### Design Principles for Query Composition

1. Tell us what you know
1. Contextual recommendations
1. Operations are not superfluous
1. See the data all the time
  * base data
  * intermediate data
  * result data
  * changes in the intemediate results?

### Criteria

Operations

* join
  * what to join?
  * what attributes to join?


# Below, write progress notes (latest at the top)

### 9/24

Some benchmark queries


        Boat(bid, name, type, speed, color, manufactor_date, design_date, last_maintained_date)
        Reservation(bid, cid, price, reservation_date, reservation_length,  used_boat_date, boat_returned)
        Customer(cid, name, bday, address, license_no, level)

        names of customers that have rented a red boat and a blue boat
        names of customers that have rented at least 5 red boats and a blue boat
        names of customers that have rented the fastest boat and the slowest boat
        average age of customers whose average boat speed is above 10

        
Some more queries

        SELECT  c AS median 
        FROM    T 
        WHERE 
          (SELECT COUNT(*) FROM T AS T1 
            WHERE T1.c < T.c) 
          = 
          (SELECT COUNT(*) FROM T AS T2 
            WHERE T2.c > T.c); 

Friends of friends

        SELECT  F1.fromID,  count(distinct F3.toID)
        FROM    BothFriends F1, 
              BothFriends F2, 
              BothFriends F3
        WHERE   F1.toID = F2.fromID AND
              F2.toID = F3.fromID
        GROUP BY  F1.fromID;


Clustering coefficient in a friend graph

        CREATE VIEW NEIGHBOR_CNT AS 
        SELECT    fromID AS nodeID, count(*) AS friend_cnt 
        FROM    BothFriends 
        GROUP BY  nodeID; 

        CREATE VIEW TRIANGLES AS 
        SELECT  F1.toID as root, F1.fromID AS f1, F2.fromID AS f1
        FROM  BothFriends F1, BothFriends F2, Friends F3 
        WHERE F1.toID = F2.toID     /* j,k both point to i */   AND
            F1.fromID = F3.fromID   /* j two outgoing edges  */ AND
            F3.toID = F2.fromID     /* j and k are friends */ 

        CREATE VIEW NEIGHBOR_EDGE_CNT AS 
        SELECT    root, COUNT(*) as cnt 
        FROM    TRIANGLES 
        GROUP BY  root;

        CREATE VIEW CC_PER_NODE AS 
        SELECT  NE.root, 
            2.0*NE.cnt / (N.friend_cnt*(N.friend_cnt–1)) AS CC 
        FROM  NEIGHBOR_EDGE_CNT NE, NEIGHBOR_CNT N 
        WHERE   NE.root = N.nodeID; 

        SELECT AVG(cc) FROM CC_PER_NODE; 




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
  * this will be good to have a list of
* propose one possible visual/text query interface
  * it should be able to express at least one of them
  * go deeep in terms of detail
    * e.g., what interface/interaction for every little bit?
  * if can't do the other queries, why not?
* list of love-to-haves





###  (date) title

The goal

What you tried

What worked