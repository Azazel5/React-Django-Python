# The-Learning-Path

These are my efforts to gain real world experience in anything related to full-stack development (React.js, Django) and programming languages (python, javascript). 
Each invidual folder is a sma. I focus on building the core functionality of the projects and select them based on my interests and what they might potentially teach me.

## Structure and type of projects

Each folder is its own project, and it contains a text file which lists the project requirements.
Here's a general overview of each project and some new things I learnt during the process

* react-freecodecamp - Completed the FreeCodeCamp's tutorial on React.js to learn more about the framework. Created controlled forms and a basic meme generator.
New things learnt - Class based components, states, controlled form and event handling in React.

* Twitter-DjangoReact - Followed the CodingEntreprenerus guide to use Django/REST framework and React.js in conjunction to create a twitter clone. It is a full fledged application featuring tweeting, retweeting, liking, unliking, authentication, and user profiles. <br>
New things learnt - Django side: passing requests to the serializer, template with tag, custom model managers, testing, fixing CORS issues with the React components. <br>
React side - Proper project structuring, terneries, props, components, event handlers, useState and useEffect, building the component/deploying it to the Django side

* ImageServerAPI - Create an image server API with functionalities such as viewing list of registered users, adding images with unique IDs and titles, downloading images. The project should be containeried. <br>
New things learnt: Containerization using Docker, adding dependencies, and building images. Created custom viewsets for the API and understood how and when to override methods like get_queryset, create, or validate. Learnt to use the OAuth toolkit in register applications and provide access tokens for your REST API. 

* BrandScraping - Look up a well known brand (such as Nike) and get a list of followers. Go to each follower, and check what
other verified brands they are following and generate a list of common brands. <br>
New things learnt: Using the python -i command effectively. Very useful to break your script into components and test each
seperately. I also learnt how to execute javascript using selenium, which is a powerful way to manipulate the web DOM.

* ChatbotBusiness - Create a simple chatbot that takes orders for a business. <br>
New things learnt: Creating a chatbot, tokenizing and lemmatizing words

* StripeIntegration - Integrate Stripe to Django.
<br>New things learnt: Stripe forms and creating charges. Adding extra context to class based views by overriding the get_context_data method. 

* Webscrape-ImageZip - Search Amazon for a product, save product details in a csv file, and extract product's images into a zip file. <br>
New things learnt: Handling different layouts on same page, downloading images using requests, working with zip files in python
