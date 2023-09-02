# The One Ring Advesary Card Generator with NanDeck (WIP)
Project to generate Advesary Cards for The One Ring with NanDeck. 

I would like to thank Free League Publishing for a fantastic game: https://freeleaguepublishing.com/en/games/the-one-ring/.

I would like to thank Oliver K. for the inspiration. His example can be cound here: https://www.youtube.com/watch?v=f6jtqekhn04.

## NanDeck
To install NanDeck, go to https://www.nandeck.com/ and install the latest version. When installed go to "Open Deck" and the go the location with tor.txt (in this directory), this should open the project.

To have the same fonts as the books, go to the fonts folder in this directory and copy them to the same folder as nandeck.exe. The fonts wil automatically load on start.

For all the advesary card art, drop you images in "./images/advesaries". The name of the advesary should be exacly the same as in the csv file.

The data file is in csv format. It contains all the information that is needed to generator the cards. It is strucutred in two parts, the front and the back card. First all the information of the front cards is listed. After this all the back cards are shown. 

Change the LINK variable to the location of you advesary csv file.

## Advesary data generator
Script made to generator the csv file from a text file. The text file contains the table information from the books. Just copy the advesary table and past it into the text file. Leave a new line between advesaries. 