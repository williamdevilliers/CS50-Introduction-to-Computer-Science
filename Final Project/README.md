# Our Solar System
#### Video Demo: https://www.youtube.com/watch?v=sufsyd8VdHw&t=89s
#### Description:
This website is powered by three separate APIs. The primary celestial data (mass, volume, density, gravity, temperature etc.) are provided by the Solar System OpenData API.
The images captured by the Mars rovers are provided by the Mars Rover Photos API.
The weather data captured by the InSight rover is provided by the InSight: Mars Weather Service API.

application.py is the primary script with which all other pages interact with. helpers.py contains the API urls from which JSON formatted data is retrieved. This data is parsed and can be requested by application.py.

home.html serves as the landing page for the website. This page displays introductory text in a box, images of each planet, and a dropdown with each planet (and sun) with a submit button.
If any image is clicked or the submit button is used, a post request is made (/planet). application.py will accept this post request and run planet() with the value from the dropdown form or any image clicked.
This function will retrieve data from the Solar API and define several variables such as mass or average temperature. planet.html is then rendered with these variables passed to the html page.

planet.html will display the variables in a box with a picture of the corresponding planet (or sun) selected in the dropdown (or image) on home.html. For those planet.html pages that have non-empty moon lists, a moon dropdown is
displayed. If a moon is selected and the submit button clicked, a similar post request will be made but it will be to /moon. This will perform moon() which will render moon.html. This is different from planet.html in that different
variables are used such as "discovered by".

If Mars is selected on the home.html page, planetmars.html will be rendered and display information on Mars with two additional features. The first is a weather button which will make a post request to application.py (/weather).
application.py will accept this and perform weather(). This retrieves parsed information from the InSight: Mars Weather Service API (from helpers.py). Variables are defined and weather.html is rendered. On weather.html,
these variables are displayed. The second function consists of three forms. These forms accept "sol days" as input with a selected camera option. The button for each form also has its own value. The sol days,
camera option, and button value are all passed via a post request (/photo) to application.py to perform photo(). This retrieves parsed information from the Mars Rover Photos API (from helpers.py). Variables are defined and
photo.html is rendered. On photo.html, these variables are displayed.

Users to the website can register through register.html. This page makes a post request to application.py (/register) which inserts the user's username and password into a sql database (space.db). login.html queries the database
to see if the username and password matches with the entry on the database.

Once logged in, users can select "Quizz" on any html page to load quizz.html. This page is filled with forms that with a single submit button, will make a post request to applciation.py (/quizz). application.py will run quizz()
which declares variables from the values of the forms on quizz.html. It also saves these answers to space.db. quizzresult.html will be rendered for quizz() with these variables. quizzresult.html will display these variables.

The "About" option on the navbar will load about.html. This is a simple html with text, three href links, and an image.

