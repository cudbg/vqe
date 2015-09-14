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



Questions

* What kind of user does each paper imagine?  What is that user trying to do?
* What seem to be useful or good features of each paper?
* What types of queries or expressions or analyses seem tricky,  annoying or impossible to do?
* What other things (for example, data distributions) would be really useful when formulating queries?
* Do you believe their evaluations?



# Below, write progress notes (latest at the top)

###  (date) title

The goal

What you tried

What worked