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

Preformatting(code samples)
===========================

An example::

    Whitespace, newlines, blank lines, and all kinds of markup
      (like *this* or \this) is preserved by literal blocks.
  Lookie here, I've dropped an indentation level
  (but not far enough)

no more example


::

    This is preformatted text, and the
    last "::" paragraph is removed


Section
=======

To break longer text up into sections, you use section headers.

These are a single line of text (one or more words) with adornment: 
an underline alone, or an underline and an overline together, 
in dashes “``-----``”, equals “``======``”, tildes “``~~~~~~``”
or any of the non-alphanumeric characters “`= -  :  ' " ~ ^ _ * + # < >`”
that you feel comfortable with. 

An underline-only adornment is distinct from an overline-and-underline adornment using the same character.

*The underline/overline must be at least as long as the title text.*

Be consistent, since all sections marked with the same adornment style are deemed to be at the same level:


::

    Chapter 1 Title
    ===============

    Section 1.1 Title
    -----------------

    Subsection 1.1.1 Title
    ~~~~~~~~~~~~~~~~~~~~~~

    Section 1.2 Title
    -----------------

    Chapter 2 Title
    ===============


Document Title / Subtitle
-------------------------


::
    ================
    Document Title
    ================
    ----------
    Subtitle
    ----------

    Section Title
    =============

    ... 
