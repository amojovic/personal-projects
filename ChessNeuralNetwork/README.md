This was an attempt to try and train a neural network on some chess games and see how it would perform.

Overall it ended up as a failed experiment because of small dataset, low number of epochs and bad approach to the problem because no reinforcement learning or position evaluation was done.

This was just 'let's feed the model data a see the results', it depends entirely on pattern repetition rather than proper game understanding.

It does not evaluate if the move is strong, if it leads to checkmate, etc. - it simply imitates moves from its training set (which does not work very well).
