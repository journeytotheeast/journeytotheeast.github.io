# Introduction to Map/Reduce

`Lots of data means we should bring computation to data.`
- Possibilities:
  - Case 1: data needs updating -> Database/Indices & Tables
  - Case 2: need to sweep through data & perform some relatively simple processing -> need a system that helps you apply functions to pieces of the data that are spread out and then organize the output. 

## The framework
Using the Map/Reduce framework will help us process big data but we have to adopt the Map/Reduce requirements -> must write functions in exchange for taking care of the logistics.
- User defines: 
  - a. <key, value>: all of our data is gonna be placed into key-value pairs (basic unit of data)
  - b. mapper & reducer functions: mapper is the function that is applied to the data, and the reducer is the function that applied to the intermediate results
- Hadoop handles the logistics (parallel execution, of the map and reduce functions, and produce the intermediate results, and communicating those results to the reducer). Hadoop handles the distribution and execution: it distributes the map functions to the data; Hadoop shuffling and grouping data according to the key-value pairs so that all pairs with the same key are grouped together and passed to the same reducer.
- Map/Reduce flow:
  - User defines a `map()` function
  - `map()` reads data and outputs <key,value>
  - User defines a `reduce()` function
  - `reduces` reads <key,value> and output your result
  - Hadoop will take care of the logistics (distribute `map` to the cluster nodes, run `map` on the data partitions at the same time)
    - it will take the `map()` function, apply it to wherever the data is sitting (the `map` function will be replicated and distributed)
    - it will take the `map` output, and it will shuffle and group the data according to the key to produce intermediate results.
    - it replicate and distribute the `reduce` function to process those intermediate results.

### Example: WordCount (Count word frequencies)
- Wordcount Strategy:
  - Let <word,1> be the <key,value> pair
  - Let Hadoop do the hard work
  - The Mapper:
  ```
  Loop until done:
    get word
    emit <word><1>
  ```
  - The Reducer:
  ```
  Loop over key-values:
    Get next <word><value>
    If <word> is the same as previous word
      add <value> to count
    else
      emit <word><count>
      set count to 0
  ```
  
## Map/Reduce Examples and Principles
- Hadoop Rule of Thumb
  - 1 Mapper per data split (typically)
  - 1 reducer per computer core (best parallelism): but optimal number could depend on blocksize in the task itself. It's good to have fewer output files (ie) but also tasks that don't run too long. (processing time >< number output files)
- Wordcount Strategy:
  - Let <word,1> be the <key,value>
  - Simple mapper and reducer
  - Hadoop did the hardwork of shuffling and grouping
- Group key-value properties:
  - simple
  - enable reducers to get correct output
  - Shuffling and Grouping `><` Key-Value simplicity
- Good Task Decomposition:
  - Mappers: simple and separable
  - Reducers: Easy consolidation

### Example: Trending WordCount
- Twitter Data: date, message, location, [other metadata]
- Task 1 Get word count by day
  - Design: Use composite key
  - Map/Reduce: <date word, count>
- Task 2 Get total word count
  - Cascading M/R

### Example: Joining Data
- Tasks: combine datasets by key
  - A standard data management function
  - In pseudo SQL:
    ```
    SELECT * FROM table_a A, table_b B
    WHERE A.key=B.key
    ```
  - JOINs can be inner, left or right
- Result wanted: File AjoinB: <word date, day-count total-count>
```
able    Jan-16,    2    5
actor    Feb-22,    15    18
actor    May-03,    1    18
burger    Jul-04,    20    25
```
- Recall that data can be split in parts: How to gather the right pieces?

### Key-Value & Task Decomposition
- Main design consideration:
  - Join depends on matching words (e.g. SELECT * WHERE A.word=B.word) -> So if words are grouped together, then all the information for the join could be carried out.
- For the join:
  - Let <key> = word
  - Let <value> = other info
  <word, ...>
- Task Decomposition:
  - Reducer now has all the data for same word grouped together
  ```
  actor,    18
  actor,    Feb-22 15
  actor,    May-03 3
  ```
  - Reducer can now join the data and put date back into key
  ```
  Feb-22 actor, 15 18
  May-03 actor, 3  18
  ```

### Example: Vector Multiplication
- Task: multiply 2 arrays of N numbers (N >>)
- Main design consideration:
  - need elements with the same index together
Let <key, value> = <index, number>
- Problem: array partitions don't have an index
- Hadoop makes environmental information available
```
A               B
<index,num>     <index,num>
1, 5            1, 2.7
2, 4            2, 1.9
```
- Mapper:
  - `map()` can access this extra info
  - This info can be passed along in the key value output, or it can be used as a side effect in which the mapper puts some data outside the Hadoop system.
    - Let assume:
      - each line already has <index, number>
      - mapper only needs to pass data (identity function)
- The Hadoop M/R system will then shuffle and group the indices
- Reducer:
  - get pairs of <index,number>
  - multiply & add
(still need get total sum, but should be largely reduced)

#### Computational costs for vector multiplication
- How many <index, number> are output from `map()`?
  - For: 2 Vectors with N indices each
  - Then: 2N <index, number> are output from `map()`
- How many <index> groups have to be shuffled?
  - For: 2N indices and N pairs
  - Then: N groups are shuffled to reducers   
- In general: the more groups the more shuffle work
- Now shuffling costs depend on N/R groups:
  - If R > 1
  - Then: N/R < N (less shuffling to do)
- Trade-offs:
  - If size of N/R >>
  - Then shuffle cost >> 
  - But reducer complexity << (the reducer needs to partition the indices for the same bin into the original index values)

### M/R Summary:
- Summary:
  - First, MapReduce works best when tasks can be decomposed. The main features:
    - mappers are separate and independent
    - mappers work on data parts
- Design Considerations:
  - `<key,value>` must enable correct output
  - Let Hadoop do the hard work
  - Trade-offs
  - Common mappers:
    - Filter (subset data)
    - Identity (just past data)
    - Splitter (as for counting)
- Design Strategy that go beyond WordCount:
  - Composite `<keys>`: when we had 2 fields that needed to be grouped
  - Extra info in `<value>`: we used `value` field to carry extra info
  - Cascade Map/Reduce jobs
  - Bin keys into ranges: can reduce shuffling work
  - Aggregate map output when possible (combiner option): 
- Potential Limitations M/R:
  - Must fit `<key,value>` paradigm
  - M/R data not persistent
  - Requires programming/debugging
  - Not interactive
- Beyond Map/Reduce
  - Data access tools (Pig, HIVE)
    - SQL like syntax
  - Interactively and Persistency (Spark)
