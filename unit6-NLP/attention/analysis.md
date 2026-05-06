# Analysis

## Layer 5, Head 1

The model detects that preposition relate to their verbs, like how "on" has a connection with "relied". This s true even if the verb and preposition is not directly next to each other, such as "leaned back in". Although the the attention weight for "leaned" and "in" is not strong as "back" and "leaned". So, a preposition-verb relation is better detected if the preposition strongly modifies the verb. Ex. "relied" depends on "on" to modify it, but "leaned" already has "back" to modify it. 

Example Sentences: 
- harry relied on his friends for [MASK].
- Sherlock Holmes leaned back in [MASK] settee

## Layer 4, Head 11

BERT finds the relationship between the verb and its direct object, which in this case would be "made" and "mess" or "distorted" and "image". The diagram sitll strongly detects this relationship even with the ordering of the direct object and verb switched around. Because attention mechanisms assigns higher weighted values to words that are greatly influenced by each other, it will detect the verb-direct object relation from context no matter which one comes first. So, the program works well for both sentenecs.

Example Sentences:
- The icy surface distorted [MASK] image
- What a mess [MASK] have made!