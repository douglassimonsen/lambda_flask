# Why?

This library is part of a larger project to build a Marey's String Chart site with as few dependencies as possible. I like the flask framework, but:

1. I only use a small subset of the functionality
2. I didn't want to fight integrating werkzeug into lambda
3. I wanted to see what if I could re-implement the functionality.


 # Worries

 I need to study lambda's thread safety in more depth. There's global state that may be poisoning 