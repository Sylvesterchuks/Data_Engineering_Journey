## Day 22: SQL Basics, Query Structure, Built In Clause

#### There are five Categories in SQL :

**🛠 DDL — Data Definition Language: Commands [CREATE, DROP, ALTER, TRUNCATE]**
DDL commands are used to define, modify, and manage the structure of database objects, such as tables, indexes, and constraints.
-  ✏ CREATE is used to create a new database, table or view.
-  ✏ ALTER is used to modify an existing table’s structure.
-  ✏ Drop used to delete a database, table, view.
-  ✏ TRUNCATE command is used to delete all the rows from the table and free the space containing the table.

**🔐 DCL — Data Control Language: Commands [GRANT, REVOKE]**
DCL are used to manage database security and access control to ensure that only authorized users can access and modify the database. 
-  🗝 GRANT: Used to grant specific privileges to database users or roles.
-  🔒 REVOKE: Used to revoke previously granted privileges.

**📝 DML — Data Manipulation Language: Commands [INSERT, UPDATE, DELETE]**
DML is responsible for performing all types of data modification in a database, the database instance is modified by inserting, modifying, and deleting its data.
-  ⬇ INSERT: Used to add new records to a table.
-  🔄 UPDATE: Used to modify existing records in a table.
-  ❌ DELETE: Used to remove records from a table.

**🛃 TCL — Transaction Control Language: Commands [ROLLBACK, COMMIT, SAVEPOINT]**
TCL commands are used to manage database transactions, they are important for maintaining the consistency of data in a database, thus ensuring data integrity.
-  🆗 COMMIT: Commits a transaction, saving changes permanently.
-  🔙 ROLLBACK: Undoes changes made during a transaction.
-  💾 SAVEPOINT: Sets a point within a transaction to which you can later roll back.

**❔ DQL — Data Query Language: Commands [ SELECT]**
Data Query Language (DQL) is used to retrieve data from the database.
-  🔎 SELECT: Used to retrieve data from one or more tables.

**THE “BIG 6 ELEMENTS OF A SQL SELECT STATEMENT**
<ol type="a">
<li> SELECT: specifies columns to return</li>
<li> FROM: specifies the table to query</li>
<li> WHERE: an optional clause that filters records based on the given logical conditions.</li>
<li> GROUP BY: an optional clause that specifies how to group data</li>
<li> HAVING: an optional clause that performs group-filtering based on criteria, works with group by</li>
<li> ORDER BY: an optional clause that specifies the order in which results are sorted.</li>
</ol>


#100DaysOfDataEngineering #DataEngineering #Data

![Basic SQL 1](carbon3.png)
![Basic SQL 2](carbon4.png)
