# Project #1

Let's begin your first project. We are going to make a web application
for forum discussions. One of the most popular forum sites today
is reddit.com. If you visit reddit.com, you will find that
it has a rich assortment of features. We're going to begin with something
that's much simpler. For now, we're planning on having the following
functionality:

1. Users can visit the page and post a message. We won't require
users to login, so messages can be made by anyone.
2. A message should contain the date and time at which it was posted
and the message text. Most recent messages should be displayed first
(for the most part).
3. Users can reply to each other. When that happens, we want to nest
messages appropriately.

You haven't yet learned all the functionality needed to perform
these tasks. We'll get to it shortly. For now, we're going to focus
on getting Django to produce/render the HTML needed for this project.

As you work on this project, you should use git to periodically
update your work. I have no testing code in place to check the quality
of your work as yet, but I may elect to create some later. I'll let
you know if I do.

To get started on this project, you will need to use a variety of tools
(git, virtualenv, selenium, django, html, css, etc.). Our textbook
covers much of this content, but it is dispersed over multiple chapters.
As an alternative, feel free to use my 
[Cheat Sheet](https://github.com/brandonbate/Cheat-Sheet)
to quickly find the commands you need. To further aid you in this
project, I have a outline of the steps you should perform to get
started.

1. Clone the repository associated with this activity
into a folder you will use for this project.
2. Create and activate a virtual environment in this folder.
3. Install Selenium and Django in your virtual environment.
4. Make sure the Geckodriver is accessible to Selenium.
5. Create a Django project.
6. Create a file called ```functional_tests.py``` that will contain your functional tests.
Begin by creating a test that checks that the title of the HTML page is what you
expect.
7. Modify the appropriate files in your project so that this test
is satisfied.
8. If you haven't already, use the Django template feature to generate
your HTML. This will involved creating an app in your project. Implement the appropriate unit tests.
9. Design an HTML document, that Django renders, so that 
the HTML has the name of your web application and the HTML has an interface for a user to post a message (it doesn't have to work yet!).
As you create this HTML document, be sure to update your functional
and unit tests appropriately.
10. Continue improving the design your HTML. I strongly encourage taking
a look at the CSS document I provided in Activity #2. It includes
comments that help explain how to customize the appearance of HTML.

