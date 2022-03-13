import datetime as dt

import discord, pandas as pd, numpy as np, matplotlib.pyplot as plt
from discord.ext import commands
from discord.commands import ApplicationContext, SlashCommandGroup

class CovidGraphs(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.yesterday = dt.date.today() - dt.timedelta(days = 1)

        self.font_properties = {
            'family': 'Arial',
            'color':  'black',
            'weight': 'heavy',
            'size': 7,
            'style': 'oblique'
        }

        self._vaxdataGetter() 
        self._vaccineGraphPlot()
        self._casesDataGetter()
        self._casesGraphPlot()
        

    covid_sub = SlashCommandGroup("covid", "List of covid-related subcommands", guild_ids = [871300534999584778, 536835061895397386, 497567524800561153])

    """
    FOR VACCINE DOSES
    """
    def _vaxdataGetter(self):
        # Overwrites the date with yesterday
        self.yesterday = dt.date.today() - dt.timedelta(days = 1)

        # Converts CSV data into lists
        vaccination_by_state: pd.DataFrame = pd.read_csv(r'https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv').tail(16)
        
        self._daily_first_dose = vaccination_by_state['daily_partial'].tolist()
        self._daily_second_dose = vaccination_by_state['daily_full'].tolist()
        self._daily_booster = vaccination_by_state['daily_booster'].tolist()
        self._daily_total = vaccination_by_state['daily'].tolist()
        self._cumul = vaccination_by_state['cumul'].tolist()[-1]
        self._states = vaccination_by_state['state'].tolist()

        # Overall data 
        vaccination_nationwide = pd.read_csv(r'https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv').iloc[-1].tolist()
        self._nation_daily_booster = vaccination_nationwide[6]
        self._total_cumul_doses = vaccination_nationwide[9]

    def _vaccineGraphPlot(self):
        # Set figure size and styling
        plt.figure(figsize = (6, 3), dpi = 300)
        plt.style.use("fivethirtyeight")
        BAR_WIDTH = 0.25

        # Plotting the bar graph
        position = np.arange(len(self._states))
        plt.bar(position - BAR_WIDTH, self._daily_first_dose, label = "First Doses", width = BAR_WIDTH, color = '#485696')
        plt.bar(position, self._daily_booster, label = "Booster Doses", width = BAR_WIDTH, color = '#FFBF81')
        plt.bar(position + BAR_WIDTH, self._daily_total, label = "Total Doses", width = BAR_WIDTH, color = '#2D9F83')

        # Rotates x-axis text by 90 degrees, and aligns the dates with the X-Axis (states)
        plt.xticks(position + BAR_WIDTH / 2, rotation = 90, labels = self._states)

        # Labels X and Y labels, and title of the graph as well as the properties like font size etc
        

        plt.xlabel("States", fontdict = self.font_properties)
        plt.ylabel("Vaccinations", fontdict = self.font_properties)
        plt.title("Daily Vaccination by State", fontdict = self.font_properties)
        plt.rc('legend', fontsize = 4.5)
        plt.legend(loc = 'best')
        
        # Make the graph display properly or else the text will cut out
        plt.tick_params(labelsize = 5)
        plt.tight_layout()

        # Save image in directory
        plt.savefig("images/_graphs/vaccination-by-state.png")
    
    
    @covid_sub.command(
        name = "vaccine", 
        description = "Sends the latest vaccination data from PICK"
        )
    async def vaccine(self, ctx: ApplicationContext):
        # Reset each time (in case its a new day in which new data got added to the csv file), if not it will just use the current data 
        if self.yesterday != dt.date.today() - dt.timedelta(days = 1):
            self._vaxdataGetter()
            self._vaccineGraphPlot()
        
        daily_first_dose = ""
        daily_second_dose = ""
        daily_booster = ""
        daily_total = ""
        states = ""

        for i in range(len(self._states)):
            states += f"{self._states[i]}\n"
            daily_first_dose += f"{self._daily_first_dose[i]}\n"
            daily_second_dose += f"{self._daily_second_dose[i]}\n"
            daily_booster += f"{self._daily_booster[i]}\n"
            daily_total += f"{self._daily_total[i]}\n"

            ###
            # future idea: split it up into 1st and 2nd doses by state as well as percentage of population vaccinated
            # me from the future: dont do this anymore because its pointless as nobody gets their 1st and 2nd doses anymore
            ###
            
        vaxEmbed = discord.Embed(title = "Malaysia Vaccination Rate 2 electric boogaloo", 
                                description = f"As of __**{self.yesterday}**__\n**Booster Doses Given Out Today:** {self._nation_daily_booster}\n**Total Cumulative Doses Nationwide** {self._total_cumul_doses}", 
                                color = 0x33cc18)
        
        # Adding fields
        vaxEmbed.add_field(name = "__State__", value = f"{states}", inline = True)
        vaxEmbed.add_field(name = "__Booster Shots__", value = f"{daily_booster}", inline = True)
        vaxEmbed.add_field(name = "__Total__", value = f"{daily_total}", inline = True)

        # Footer
        # it turns out you cant put hyperlinks in footers :(
        # vaxEmbed.set_footer(text = "[**Data taken from the GitHub page of the COVID-19 Immunisation Task Force (CITF) for Malaysia's National COVID-19 Immunisation Programme (PICK)**](https://github.com/CITF-Malaysia/citf-public)")
        vaxEmbed.set_footer(text = "Data sourced from the GitHub page of the COVID-19 Immunisation Task Force (CITF) for Malaysia's National COVID-19 Immunisation Programme (PICK)")
        vaxEmbed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/869934977381437500/870597552532242462/header-vax-microsite2x.png?width=675&height=675")
        

        graph_img_file = discord.File("images/_graphs/vaccination-by-state.png", filename = "image.png")
        vaxEmbed.set_image(url = "attachment://image.png")
        await ctx.respond(file = graph_img_file, embed = vaxEmbed)

    """
    FOR COVID CASES
    """
    def _casesDataGetter(self):
        # Overwrites the date with yesterday
        self.yesterday = dt.date.today() - dt.timedelta(days = 1)

        # Convert CSV data into lists
        cases_csv = pd.read_csv(r'https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv').tail(14)
        self.dates = cases_csv['date'].tolist()
        self.new_cases = cases_csv['cases_new'].tolist()
    
    def _casesGraphPlot(self):
        plt.figure(figsize = (13, 8), dpi = 100)
        plt.style.use("fivethirtyeight")

        # Plotting the line graph
        position = np.arange(len(self.dates))
        plt.plot(position, self.new_cases, label = "Cases")

        # Rotates x-axis text by 90 degrees, and aligns the dates with the X-Axis
        plt.xticks(position , rotation = 90, labels = self.dates)

        plt.xlabel("Dates", fontdict = self.font_properties)
        plt.ylabel("Cases", fontdict = self.font_properties)
        plt.title("Daily Covid-19 Cases For Past 2 Weeks", fontdict = self.font_properties)
        plt.rc('legend', fontsize = 4.5)
        plt.legend(loc = 'best')

        plt.tick_params(labelsize = 5)
        plt.tight_layout()

        # Save image in directory
        plt.savefig("images/_graphs/cases-past-fortnight.png")

    @covid_sub.command(
        name = "cases",
        description = "Displays amount of cases for the past 14 days"
    )
    async def covidcases(self, ctx: ApplicationContext):
        if self.yesterday != dt.date.today() - dt.timedelta(days = 1):
            self._casesDataGetter()
            self._casesGraphPlot()
        casesEmbed = discord.Embed(title = "Malaysia Daily Covid Cases (Past 14 Days)", 
                                   color = 0x33cc18)
        cases_img = discord.File("images/_graphs/cases-past-fortnight.png", filename = "image.png")
        casesEmbed.set_image(url = "attachment://image.png")
        await ctx.respond(file = cases_img, embed = casesEmbed)


def setup(client: commands.Bot):
    client.add_cog(CovidGraphs(client))
