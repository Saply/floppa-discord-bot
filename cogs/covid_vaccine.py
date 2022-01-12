import discord, pandas as pd, datetime, os, numpy as np
from discord_slash.context import SlashContext
import matplotlib.pyplot as plt
from discord.ext import commands
from discord_slash import cog_ext

class Vaccine(commands.Cog):
    # goal: 
    def __init__(self, client):
        self.client = client

        # Only initialised once since its always gonna be inaccurate fr fr
        self.yesterday = datetime.date.today() - datetime.timedelta(days = 1)
        self.dataGetter()

        # Plot graph styling
        plt.style.use("fivethirtyeight")
        self.BAR_WIDTH = 0.25

    # called each time the /vaccine slash command is called
    # @setattr
    def dataGetter(self):
        # Overwrites the date with yesterday
        self.yesterday = datetime.date.today() - datetime.timedelta(days = 1)

        self.vaccination_by_state_csv = pd.read_csv(r'https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv').tail(16)
        self._daily_first_dose = self.vaccination_by_state_csv['daily_partial'].tolist()
        self._daily_second_dose = self.vaccination_by_state_csv['daily_full'].tolist()
        self._daily_booster = self.vaccination_by_state_csv['daily_booster'].tolist()
        self._daily_total = self.vaccination_by_state_csv['daily'].tolist()
        self._cumul = self.vaccination_by_state_csv['cumul'].tolist()[-1]
        self._states = self.vaccination_by_state_csv['state'].tolist()
    
    # actual vaccine thing 
    @cog_ext.cog_slash(name = "vaccine", description = "You will never believe what this does", guild_ids = [536835061895397386])
    async def vaccine(self, ctx):
        # Reset each time (in case its a new day and new data got added to the csv file), else it will just use the current data 
        if self.yesterday != datetime.date.today() - datetime.timedelta(days = 1):
            self.dataGetter()
        
        daily_first_dose = ""
        daily_second_dose = ""
        daily_booster = ""
        daily_total = ""
        states = ""

        # i have to do this because discord sucks
        # SCUFFED SCUFFED SCUFFED SCUFFED SCUFFED SCUFFED SCUFFED 
        for i in range(len(self._states)):
            states += f"{self._states[i]}\n"
            daily_first_dose += f"{self._daily_first_dose[i]}\n"
            daily_second_dose += f"{self._daily_second_dose[i]}\n"
            daily_booster += f"{self._daily_booster[i]}\n"
            daily_total += f"{self._daily_total[i]}\n"

        vaccination_nationwide = pd.read_csv(r'https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv').iloc[-1].tolist()
        # booster
        nation_daily_booster = vaccination_nationwide[6]
        total_cumul_doses = vaccination_nationwide[9]

            ###
            # future idea: split it up into 1st and 2nd doses by state as well as percentage of population vaccinated
            # me from the future: dont do this anymore because its pointless
            ###
            
        vaxEmbed = discord.Embed(title = "Malaysia Vaccination Rate 2 electric boogaloo", 
                                description = f"As of __**{self.yesterday}**__\n**Booster Doses Given Out Today:** {nation_daily_booster}\n**Total Cumulative Doses Nationwide** {total_cumul_doses}", 
                                color = 0x33cc18)
        
        # Adding fields
        vaxEmbed.add_field(name = "__State__", value = f"{states}", inline = True)
        vaxEmbed.add_field(name = "__Booster Shots__", value = f"{daily_booster}", inline = True)
        vaxEmbed.add_field(name = "__Total Doses Today__", value = f"{daily_total}", inline = True)

        # Footer
        vaxEmbed.set_footer(text = "Data taken from the GitHub page of the COVID-19 Immunisation Task Force (CITF) for Malaysia's National COVID-19 Immunisation Programme (PICK)")
        vaxEmbed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/869934977381437500/870597552532242462/header-vax-microsite2x.png?width=675&height=675")

        """
        embed = discord.Embed(title = f"A random {animal}", description = random.choice(["cute", "funny", "hilarious"]), color = 0x3240a8)
        image_file = discord.File(path, filename = "image.jpg")
        embed.set_image(url = "attachment://image.jpg")
        await ctx.send(file = image_file, embed = embed)
        """


        await ctx.send(embed = vaxEmbed, hidden = False)
    
    # temporary test 
    @cog_ext.cog_slash(name = "vaccineplot", description = "aaaaaaaaa", guild_ids = [536835061895397386])
    async def vaccineplot(self, ctx: SlashContext):
        position = np.arange(len(self._states))
        fig = plt.figure(figsize = (13, 8), dpi = 100)

        # Plotting the bar graph
        plt.bar(position - self.BAR_WIDTH, self._daily_first_dose, label = "First Doses", width = self.BAR_WIDTH, color = '#485696')
        plt.bar(position, self._daily_booster, label = "Second Doses", width = self.BAR_WIDTH, color = '#FFBF81')
        plt.bar(position + self.BAR_WIDTH, self._daily_total, label = "Total Doses", width = self.BAR_WIDTH, color = '#2D9F83')

        # Rotates x-axis text by 90 degrees, and aligns the dates with the X-Axis (states)
        plt.xticks(position + self.BAR_WIDTH / 2, rotation = 90, labels = self._states)

        # Labels X and Y labels as well as Title of the graph
        plt.xlabel("States")
        plt.ylabel("Vaccinations")
        plt.title("Daily Vaccination by State")
        plt.legend(loc = 'best')

        fig.savefig("images/_graphs/testfig.png")
        plt.show()
        await ctx.send("trust me it works")
        # use os.remove(path) to remove the file after savefig() is used
        # i havent plotted this at all yet


        
def setup(client):
    client.add_cog(Vaccine(client))
