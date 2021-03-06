# NLPProject
Question Generation
Our pipeline for generating questions started with storing relevant information, creating rules to formulate questions, and finally ranking the questions to output the best ones.

Information Storage
To store the information from the text, we created dictionaries that delved into the syntactic structure of the sentence given by a parse tree. Using Stanford’s Core NLP parser and NER tagger, we were able to store features in our dictionaries such as Noun Phrase, Verb Phrase, plurality of the noun, tense of the verb, and named entity.

Question Formulation
By creating rules in form of dictionaries, we were able to use the information gathered in step one to create questions. We focused primarily on Who-What type questions. The key of the rule dictionary specified all the values that should match the question format as shown. We then used the information from the sentence's dictionary from step one to determine if there was a match between the sentence and the rule. For example, a "Who" rule would match with a sentence which contained a singular, proper noun. The question generator would then add a "Who" to that sentence's verb phrase to create a question.

Question Ranking
Our criteria for ranking our questions were the question types, and the length. We analyzed and assigned points to certain question types that we were confident in which were the Who questions. What date, and what place questions were also accurate, but we tended to generate less of them. Many of the what questions had vague meanings so we had to adjust it to be scored lower. Also, we found that concise questions with length of 8-15 words were the most ideal as short questions were not grammatical and long questions were wordy. Based on these scores, we returned the top N questions.

Answer Generation
Our pipeline for answer generation was based off of the general outline from the speech and language processing textbook by Jurafsky and Martin. We started with classifying each question, extracting passages likely to contain the answer, and outputting a constituent of a passage that was most likely to be the answer.

Question Classification
To classify each question into their respective classes, we used Xin Li and Dan Roth’s training set of 5500 labeled questions. These types include the overall class and subgroup to specify further. For example, if the question was “What is the fastest mammal on Earth?” it would be classified as ENT:animal as we expect the answer to be pertaining to an animal entity.
In order to train our system to correctly classify questions, we used Keras to train a neural network using a bag of words method. Our model reached 80.2% test accuracy, which was not the ideal accuracy. To make up for this, we used additional features in passage retrieval.

Passage Retrieval
The additional features used in passage retrieval were the number of times certain bigrams appeared, number of keywords and NER matches. Looking at the constituency tree from the Stanford parser, we found that most questions contained inverted clauses such as "Was John hungry?". We un-inverted this clause to come up with a sentence like "John was hungry". Then we created bigrams out of this new sentence. Finally, we assigned each passage a score based on the number of times the bigrams showed up in the passage, along with the number of keywords and NER matches.

Answer Processing
Once we had relevant passages, we looked at all of the constituents in the passage and assigned each one a score based on several features. The first feature was the type of the constituent. If we were looking for an ENTY or a HUM type for example, the answer would most likely be contained in a Noun Phrase. On the other hand, a DESC is likely to be found as a complete clause. 

The second feature was the dependency relationship of the constituents. We classed each question into one of three types: subject, object, or boolean. A subject question looks like, "Who framed Roger Rabbit?" In this question, the Wh- word is a stand-in for the subject of "framed". If we have a subject question, we give a higher score to constituents in the passage which are subjects. Similarly, an object question such as “Who did Doom frame?” would give a higher score to constituents that are objects. We gave extra points if the governor of the dependency relationship is the same as in the original question (ie. "framed"). 
Boolean questions were a special case. They usually lacked wh- words, so we looked for a clause similar to the inversion of the question. For example, "Was Roger Rabbit framed?" would be answered, "Roger Rabbit was framed."

The third feature involved the number of NER and keyword matches in the constituent. Certain question types tended to map to certain NER tags. For example, human individual question types would map to constituents containing PERSON tag. The scoring for keyword matches also varied based on question type. Descriptions, for example, tended to contain a lot of keywords from the original question, so description type constituents with more keyword matches received higher scores. By figuring out tendencies, we were able to accurately assign scores.

The final feature was a special case of ENTY questions which often required answers that were not named entities and therefore not captured by our NER matches. For example, the correct answer to the ENTY:animal question, "What is a young horse called?" is "Foal". To rank the constituents in ENTY questions, we converted them to word vector representation and looked at their cosine similarity to certain keywords. These keywords depended on the subcategory of ENTY. For example, constituents for an ENTY:animal question would be compared to keywords such as "animal", "creature", and "beast".

After considering all the features, we ultimately returned the constituent with the best score as our final answer.
