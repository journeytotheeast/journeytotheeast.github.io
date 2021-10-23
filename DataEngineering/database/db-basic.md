# Relational Database Design

## Database Normalization (3NF)
1. Primary key
  - A table should always have a primary key.
  - Primary keys always uniquely identify a row, so that whenever you find a row by its primary key, you know you've found the only row.
2. Atomic columns
  - A "non-atomic" column is one where you want to use a part of the column for a primary key or foreign key. For atomic columns, split the parts into separate columns in your design.
3. No repeating groups
  - Split a column that contains multiple elements into separate "detail" table, with multiple rows, each having a single element.
4. Non-key columns describe only with the whole key
  - Each row represents a single entity uniquely referenceable by the primary key. The other columns give details about that entity only. If a column gives detailed data about some other non-PK column, then a normalized approach is to create a separate table with a row for each entity in the non-PK column, and other columns giving further detail in that new table.
5. No derived columns


## Database Denormalization
1. Allowing duplicate rows
2. Pre-joined tables
3. Derived columns
4. Summary tables

## Trade-offs
### Normalization
1. Limiting data anomalies
2. Enforcing data structure
  - INSERT: If adding, must use existing key from source
  - UPDATE: If changing, still must use existing key from source
  - DELETE: Cannot delete from source if references to key exist
3. Size

### Denormalization
4. SELECT speed

# Operational and Analytic Databases

## Operational Database
- What is the current state?
- CRUD (Create - Retrieve - Update - Delete)

## Analytic Database
- Long-term question.
- Deep, complex queries
- ETL

# Database Transaction
## ACID
  - Atomicity: COMMIT
  - Consistency: keep design constraints
  - Isolation
  - Durability: make permanent

## Enforcing Business Rules: Constraints and Triggers


## OLTP (Online Transaction Processing)
  - CRUD
  - ACID-compliant transactions

# Data Warehouse
- Gathers accumulated data from one data source,  such as an operational database.

# Database Indexes
- In a conventional RDBMS, indexes are special datasets that help to greatly improve performance of selected queries. 

## Indexes and queries performance
|ID|Row|
|------|-----|
|22|7|
|29|6|
|30|2|
|41|4|
|50|5|


Look at this figure, which illustrates an index on the ID column.

Notice that the ID column is ordered, and that each record in the index shows the row where that ID occurs. You can use the fact of ordering to quickly locate ID 50 in the index. This gives you row number 5, which you can then find quickly in the original table for details about the person with ID 50.

An index like this would allow you to quickly find the data for any person given their ID.

In order for the index to help accelerate table access, a few features are required:
- **Random access** The system must have some capability of random access of rows in the table. That is, the system should be able to move to some spot partway in the table and read rows from there, without having to perform a disk read from the beginning of the table. A database system will store some kind of location information, like row number, or file block number, that the system can then use to quickly locate and read the row without scanning the entire table.
- **Well ordered index data** In the table that indexes on ID, the ID values are ordered, and this allows you to quickly locate the ID in the list. 
- **Alignment of index and table** 

## Indexes and Key Constraints
In addition to using indexes to aid query performance, many systems that have table indexing will use unique indexes as a way to enforce primary key constraints. A unique index will permit to no more than one entry for its key value (the value being indexed). Because the indexed system are well organized , the system can very quickly determine if some new rows submitted for insert repeats an existing primary key, and it can reject that row right away. It is fortuitous that the primary key is also a common value to use for finding a row in a table, so the unique index on primary key does two things: it helps to enforce uniqueness on the primary key values, and it delivers speed to many queries.

Foreign keys are also often enforced with the help of indexes. A database system will often create an index on a column when that column is declared as a foreign key. Consider this example, a **department** table, and a related **employee** table. Each record in the **employee** table has a **department_id** as a foreign key to the **department** table. If the system build an index on **employee.department_id**, then it becomes a simple matter to enforce some foreign key constraints: if a user attempts to delete **department** row, a quick check of the index on **employee.department_id** can determine whether this delete would leave some employees without a department, and so whether the delete should be prevented.

## Maintaining Indexes
Notice that every index on a table requires a dataset in addition to the original table, and that the index necessarily contains data that is a repeat of the table data. To make use of the index, there must always be a way to maintain consistency between the index and the indexed table. Some systems maintain a table's indexes automatically. along with the changes to the table, and some do not.

