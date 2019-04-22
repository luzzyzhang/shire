# Code style guide

<!-- TOC -->

- [Code style guide](#code-style-guide)
    - [docsting format 规范](#docsting-format-规范)

<!-- /TOC -->

## docsting format 规范

[What is the standard Python docstring format][docstring-format-guide]

个人更倾向于 reStructuredText 和 Google 风格

- reStructuredText 风格（PyCharm 默认风格）

    ```python
    """
    This is a reST style.

    :param param1: this is a first param
    :param param2: this is a second param
    :returns: this is a description of what is returned
    :raises keyError: raises an exception
    """
    ```

- Google 风格

    ```python
    """
    This is an example of Google style.

    Args:
        param1: This is the first param.
        param2: This is a second param.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    """
    ```

- Numpydoc 风格

    ```python
    """
    My numpydoc description of a kind
    of very exhautive numpydoc format docstring.

    Parameters
    ----------
    first : array_like
        the 1st param name `first`
    second :
        the 2nd param
    third : {'value', 'other'}, optional
        the 3rd param, by default 'value'

    Returns
    -------
    string
        a value in a string

    Raises
    ------
    KeyError
        when a key error
    OtherError
        when an other error
    """
    ```

---
[docstring-format-guide]:https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format