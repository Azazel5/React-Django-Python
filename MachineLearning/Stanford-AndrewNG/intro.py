"""
What will we learn in this class?
---------------------------------

The relevant algorithms and mathematics in addition to how to implement them in scenarios you care about.
To that end, you must complete the exercises! What exactly is machine learning though? There are many 
definitions out there, such as the ability for computers to learn without explicitly being programmed.
There are two types of learning: supervised and unsupervised. As the names suggest, unsupervised 
learning is the one where the machine will learn by itself. There are also other kinds of machine 
learning algorithms like reinforcement learning and recommender systems. 

The carpenter analogy - It is not enough to simply learn the tools; you must also learn how to 
practically use the given tools.

Supervised learning 
-------------------

Think about which sort of line to use to fit the graph, whether it's a straight line or a quadratic
equation. We give the algorithm a dataset with the right answers given, so the algorithm will 
try to produce more of these right answers. This is a regression problem. 
An example of a classification problem is when you're plotting tumor sizes with respect to whether 
they're malignant or not. The problem "What is the probability of a tumor being malignant given
the size" is a classification (discrete value problem i.e. 0/1, or yes/no). There doesn't have to 
be 2 possible outcomes for it to be a classification problem. 

What happens if you have two features in the tumor problem, namely tumor size AND age? We could 
plot both in a graph, create a line seperating the patients in the dataset who have malignant 
tumors and those which don't, and do our predictions. In a real world scenario, there are usually
many different features in a particular problem. What if you wanna use infinite number of attributes?
We can use support vector machines. 

Unsupervised learning 
---------------------

In unsupervised learning, we no longer have labels to tell the algorithm whether an answer is right 
or not. They have the same labels. The algorithm may break the dataset into clusters and is called
clustering algorithms. Google News uses clustering, amongst may other applications. 

The cocktail party problem - there's a lot of people talking at the same time, so it is hard to 
identify when the person in front of you is speaking. Imagine there are two speakers and two 
microphones (at different distances); there'll be an overlap of voices from both microphones
because they're at different distances from both speakers. Clustering algorithms may be used
to seperate out the different voices! It can be seen how this can be used in video chat 
technologies to filter out background noises. 
"""

"""
Model and Cost functions
------------------------


"""