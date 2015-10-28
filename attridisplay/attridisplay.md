###Report

Here we show how data visualization helps users discover
and reduce their attributes, and also makes easier to write some queries.
(Naive thoughts, many typos and grammar mistakes because of limited time and personal
ability. Sorry about this)

####Datasets:
- [The race, age, and sex of everyone the NYPD stopped on the street and frisked in 2013]
(http://www.nyc.gov/html/nypd/html/analysis_and_planning/stop_question_and_frisk_report.shtml)
   - 112 attributes and 191851 records
- [311 Requests for NYC]
(https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9)
   - 53 attributes and 50000 records

#####45 attributes with binary entries Y/N
In NYPD datasets, it has about 45 attributes with binary entries Y/N
- for example pf_hcuff means PHYSICAL FORCE USED BY OFFICER - HANDCUFFS

```
 pf_pepsp   pf_hcuff   pf_ptwep   rf_othsw    knifcuti   machgun    othrweap    
 N:187405   N:191486   N:191834   N:191839   N:189128   N:191848   N:191009      
 Y:  4446   Y:   365   Y:    17   Y:    12   Y:  2723   Y:     3   Y:   842  
```

We can visualize these 45 attributes in one box, why?
- reduce visualization space, and good for users to understand
- these data is more likely to be compared to each other
- query operation on these attributes is almost the same. for example:
`WHERE pf_hcuff = Y` pf_hcuff can be any one of these attributes

Therefore, we do it this way:
![pic1](/attridisplay/images/pic1.png)
####30 attributes with say less than 20 possible values
For other attributes with say less than 20 possible values, their discoveries and
operations are similar as the above binary ones. Thus, we can group them to
visualize them together.

```
city                     premname                    haircolr
BRONX        : 6825      STREET     :18160           BK     :33473
BROOKLYN     :13368      SIDEWALK   : 6779           BR     : 9429
MANHATTAN    : 7261      RESIDENTIAL: 1097           BA     : 1039           
QUEENS       :13335      LOBBY      : 1056           BL     :  604                  
STATEN ISLAND: 4998      (Other)    : 4694           XX     :  295
```
We notice above attribute prename has 10 more different values in `(Other)`. They
total only represents about 8% of all records, then we may put them together as
one value to visualize. Of course, we should highlight this modification, and
users can click on it to expand details.
In NYPD table, it contains about 20 this kind of attributes.
![pic](/images/pic2.png)
#####15 attributes with null, one possible entry or sparse inputs
Visualization of this kind of attributes can be tricky. To our knowledge, we
think the attributes with all nulls can be ignored but just show users the stats
of total number of missing data. While for sparse data, we should provide histogram
of missing entries and non-missing ones, and also show detailed visualization of
non-missing entries.


```
state            addrtyp         offverb             officrid
Mode:logical     L:191851          :145306              :44898
NA's:191851                      V : 46545           I  :  889
```
For sparse data, we will curious about how this spare data appear in other
attributes. It maybe occurs when an attribute is a specific values.

#####Function of highlight to dark or light other attributes
To find out this, for instance, in the following pictures, user can highlight
`offverb = v` as a filter condition, say we have 500 records with this entry.
In visualization section of sparse data, user can see attribute `forceuse = DO or DS`
not appearing with `offverb = v` in the same records so often. Thus, their colors
are very dark.
![pic](/images/pic3.png)
Then user can un-click sparse data and click grouping data to see
the second pic. The color of all attributes is modified into dark or light.
![pic](/images/pic2.png)
- In this way, even sparse data is visualized in different section, user can still
find the link between this data and other attributes
- If we have this `highlight to dark or light other attributes`, user can discover
the dataset cross different attributes to link them together effectively. Therefore
it helps user to come up with some interesting or useful query they want.


#####other about 15 unique attributes
For this kind of data, it is common to segment them in some sections and then
visualize in histogram. Key function we may provide is searching range filter.

#####Reducing number of attributes based on this classification
We personally use it to select small amount of attributes we would like to use
when writing our queries.

`45 attributes with binary entries Y/N`
- since they are different important attributes with the same type of entries, we
think it is fine to keep them as a group.

`30 attributes with say less than 20 possible values`
- We have some attributes with hierarchical relationship. For example, `street`
in `zip` in `city`. We only selected one to represent this group. Also, we got
rid of some attribute with complicated inputs. -> kept about 7 attributes

`15 attributes with null, one possible entry or sparse inputs`
- after highlighting each sparse data entries we kept about 3 of them.

`other about 15 unique attributes`
- we threw majority of them because they were not useful for us. Only date remained

![pic](/images/pic4.png)
#####Extend to JOIN
Here we show the visualization if user want to join these two tables NYPD and
311 NYC Requests. Because (we assume) if user click two more tables, the main
reason of doing this is to find out whether these tables can join together.

Our interface will only show the visualization of their common attributes (have
some part of same inputs). For examples, `city` in NYPD and `Borough` in 311 NYC
have the same values, which indicates they can join through this two attributes.
So we put this two names together with the same color.

Also, user can highlight some 'boxes' to do filtering, and do back to NYPD table
to see the changes in darkness of all other attributes.
![pic](/images/pic5.png)
#####Data with a long name
In 311 NYC table, we found that some attribute have less then 10 possible values,
but these values are long strings. If we visualize them without doing any
modification, it would be ugly. Thus, if our system can recognize this (long string)
and abbreviate it randomly(or combine first character of first 3 words). Since we
make some changes on them, we should tell user by highlighting them in different
color. And user can click on them to see original names or rename them.
![pic](/images/pic6.png)
#####Question
For those monthly released government data, can we use some statistical methods
such as ANOVA or chi-squared test on the same attributes in 2013 and 2014 tables?
So we can see whether there is a significant difference between them. If so, then visualize
them, if not, ignore them first.
