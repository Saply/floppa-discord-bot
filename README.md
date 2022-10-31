# floppa-discord-bot
<p align = "center">
  <img src = "https://user-images.githubusercontent.com/88439700/198971371-e32ad9c7-3387-4a52-b47d-218582699e84.png">
 </p>
 
**The floppa bot is a utility Discord bot made for extremely specific purposes which may or may not be helpful.**

## Features
The bot has three main features

→ Schedule online class reminders to be posted in a specified channel a few minutes before it starts

→ Post Covid cases/vaccine doses statistics (Malaysia only, because I live here)

→ Post animal pictures and probably interesting facts about them

## Screenshots

*Adding a class reminder to the bot as well as the bot posting it to the specified channel 5 minutes before it starts*
<p align = "center">
  <img src = "https://user-images.githubusercontent.com/88439700/198967558-54e8295b-ffa9-4ebd-93dc-c1f23287ce23.png">
  <img src = "https://user-images.githubusercontent.com/88439700/198967653-953b24b9-d955-4a37-bf48-d2b3bae32c57.png">
</p>


## Usage

Each subcommand of the `/class` command has a brief description for what they do. 
<p align = "center">
  <img src = "https://user-images.githubusercontent.com/88439700/198968551-5912875c-7c85-4a48-80b6-bc98ac56762f.png">
</p>

Additionally, the parameters for each subcommand also includes descriptions on what each of them do and what details the user has to fill up. These descriptions apply to other commands as well.

<p align = "center">
  <img src = "https://user-images.githubusercontent.com/88439700/198968632-f7963d46-052d-4e04-82a7-68a49af7737c.png">
</p>

<p align="center">
  <img src = "https://user-images.githubusercontent.com/88439700/198968645-17a412c9-4085-41d4-a37e-bd9eba85f461.png">
</p>

## Libraries and Miscellaneous

The bot uses the following third-party libraries:

- [pycord](https://github.com/Pycord-Development/pycord)
- [mongoengine](http://mongoengine.org/)
- [requests](https://github.com/psf/requests)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [numpy](https://numpy.org/)

Additionally, the `/animal` command uses data from the following Public APIs:

- [Capybara API](https://capybara-api.xyz/)
- [shibe.online](https://shibe.online/)
- [catfact.ninja](https://catfact.ninja/) [(alt link)](https://documenter.getpostman.com/view/1946054/S11HvKSz)
- [Dog API](https://github.com/kinduff/dog-api)

## Additional Notes

The bot needs to stay online for class reminders to work, or else it wouldn’t post class reminders on time if it’s offline. I recommend spinning up a cheap/free VPS and having it run 24/7 by using the [pm2 npm module](https://pm2.keymetrics.io/).

When the bot is running, the console will output what the current time is, so you can cross-check if it’s using the correct timezone or not *(usually applicable to hosting on a VPS and others)*. Make sure to set the RTC time of the machine to match your local time as well, since the Python datetime library uses the RTC of the system to determine the current time. Incorrect timezones may lead to class reminders being posted at the incorrect times.
