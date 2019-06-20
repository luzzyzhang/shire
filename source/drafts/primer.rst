=========================
A reStructuredText Primer
=========================
:Author: David Goodger <goodger@python.org>
:Date: $Date: 2019-06-20 10:38:53 $
:Description: `reStructuredText` 入门教程

.. contents::


.. note::
    How to be a good software engineer

Structure
=========

This is a paragraph.  It's quite
short.

   This paragraph will result in an indented block of
   text, typically used for quoting other text.

This is another one.

Text styles
===========

*This is a italics* and **This is Bold** all of this called *inline markup*

``double back-block`` `code` ``*``  ``*no inside the double back-quotes work *``

Lists
=====

Lists of items come in three main flavours: **enumerated**, **bulleted** and **definitions**.
In all list cases, you may have as many paragraphs, sublists, etc. as you want,
as long as the left-hand side of the paragraph or whatever aligns with the first line of text in the list item.

Lists must always start a new paragraph – that is, they must appear after a blank line.

enumerated lists
----------------

1. numbers

A. upper-case letters
   and it goes over many lines

   with two paragraphs and all!

a. lower-case letters

   3. with a sub-list starting at a different number
   4. make sure the numbers are in the correct sequence though!

I. upper-case roman numerals

i. lower-case roman numerals

(1) numbers again

1) and again

bulleted lists
--------------

* a bullet point using "*"

  - a sub-list using "-"

    + yet another sub-list

  - another item

definition lists
----------------

what
  Definition lists associate a term with a definition.

*how*
  The term is a one-line phrase, and the definition is one or more
  paragraphs or body elements, indented relative to the term.
  Blank lines are not allowed between term and definition.