TV Slagalica or simply Slagalica is a Serbian quiz show produced by RTS.

There is this one game on there where you are supposed to arrange letters they give you in order to make the longest word possible.

I was pretty bad at it, which annoyed me so i decided to try and make a script that would do it better than even the champions of the show.

Suffice to say my approach in python here was too slow (this should probably be done in C), but hey it is still better than most people at the game.

I tried 2 approaches (they both use Serbian dictionary included here as recnik.rar):

Slag1:

Single-threaded, no concurrency.

Only one search strategy: starts from longest words first (descending length).

Uses a local max_word variable.

Has a single loop, simpler logic, easier to understand and maintain.

Also includes a timeout check (if time.time() - start_time > 50) to prevent long execution because they give you like 1 minute on the show.

Slag2: 

Uses multi-threading: launches two threads in parallel:

One starts searching from shortest to longest words.

The other starts from longest to shortest words.

Uses a global shared variable (longest_word) protected by a Lock to update the longest word found.

Tries to potentially speed up the search by having two different search strategies running at the same time.

Includes a timeout check (if time.time() - start_time > 50) in each thread to stop if taking too long.

Structure
find_longest_word_from_short_to_long(): starts from 1 letter up to 12 letters.

find_longest_word_from_long_to_short(): starts from 12 letters down to 1 letter.

Threads run these functions in parallel.

Slag3:

Still did not implement this one, but the idea is to have threads start in parallel just for longer words. 

So for example 14,13,12,11 letter words all start in parallel since looking for 1 letter word like in slag2 is useless for winning.


