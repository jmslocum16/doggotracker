# Overview
Tracking when new dogs become available for adoption  by using Beautiful Soup to parse rescue and shelter websites.
I made this tool because finding a dog that met my family's requirements (small, hypoallergenic, non-puppy, gets along with other dogs, etc...) was non-trivial, and many of these sites weren't  indexed on PetFinder or the other similar aggregation sites.
So I started tracking breed-specific rescues, as well as filtering my local rescues by size/age and whatever other information I could.
It has now fufilled its purpose, as we adopted a dog found on one of these websites.

# Setup
Create a directory called last_run where you can store the state from the previous run.

# Running
Once you run the program, it will go through the list of provided dog sources, fetch the new set of available dogs, and note all differences (+  for new dogs added, -  for dogs no longer available.)
It uses random sleeps, random request order, and  time-of-day awareness to not overwhelm the shelter sites and to avoid getting blocked.

To run it once-off, just start it and kill it after it is done.

# Contributing/Forking
It was designed to be extensible - all you have to do to add a new site is specify the url, provide a python function that parses the contents and returns a list of dog names, and add that site to the listt of sites to run.
