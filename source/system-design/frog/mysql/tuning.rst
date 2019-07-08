=======================
SQL Indexing and Tuning
=======================

.. contents::
  :depth: 2


Reference
=========

`Use the index Luke!`_

.. _Use the index Luke!: https://use-the-index-luke.com/

Preface: why is indexing is a development task
==============================================

Separate **what** and **how**:

  An SQL statement is a straight description what is needed without instructions as to how to get it done.

  Developer must know a little bit about the database **how** run ``SQL`` to prevent performance problems

The most important information for indexing is *how the application queries the data*.

Anatomy of an Index (索引解剖)
==============================

.. note::

     It is about the fundamental structure of an index


What is `index`
    An index is a distinct structure in the database that is built using the ``create index`` statement. 
    It requires its own disk space and holds a copy of the indexed table data. 
    That means that an index is pure redundancy.
    Creating an index does not change the table data; it just creates a new data structure that refers to the table. 
    A database index is, after all, very much like the index at the end of a book: 
    it occupies its own space, it is highly redundant, 
    and it refers to the actual information stored in a different place.

Why use `index`
    - An index makes the query fast

SQL database must process `insert, delete and update statements` *immediately*, 
keeping the index order without moving large amounts of data.

The database combines two data structures to meet the challenge: a ``doubly linked list`` and a ``search tree``. 
These two structures explain most of the database's performance characteristics.

The Index Leaf Nodes
--------------------

How to structure index
~~~~~~~~~~~~~~~~~~~~~~



