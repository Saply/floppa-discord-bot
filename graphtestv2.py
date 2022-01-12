import matplotlib.pyplot as plt, matplotlib
import numpy as np, pandas as pd

class Plotta:
    def __init__(self):
        self.vaccination_by_state_csv = pd.read_csv(r'https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv').tail(16)
        self._daily_first_dose = self.vaccination_by_state_csv['daily_partial'].tolist()
        self._daily_second_dose = self.vaccination_by_state_csv['daily_full'].tolist()
        self._daily_booster = self.vaccination_by_state_csv['daily_booster'].tolist()
        self._daily_total = self.vaccination_by_state_csv['daily'].tolist()
        self._cumul = self.vaccination_by_state_csv['cumul'].tolist()[-1]
        self._states = self.vaccination_by_state_csv['state'].tolist()

        plt.style.use("fivethirtyeight")
        self.BAR_WIDTH = 0.25

    
    def actualplot(self):
        plt.figure(figsize = (4, 3), dpi = 300)

        # Plotting the bar graph
        position = np.arange(len(self._states))
        plt.bar(position - self.BAR_WIDTH, self._daily_first_dose, label = "First Doses", width = self.BAR_WIDTH, color = '#485696')
        plt.bar(position, self._daily_booster, label = "Booster Doses", width = self.BAR_WIDTH, color = '#FFBF81')
        plt.bar(position + self.BAR_WIDTH, self._daily_total, label = "Total Doses", width = self.BAR_WIDTH, color = '#2D9F83')

        # Rotates x-axis text by 90 degrees, and aligns the dates with the X-Axis (states)
        plt.xticks(position + self.BAR_WIDTH / 2, rotation = 90, labels = self._states)

        # Labels X and Y labels, and title of the graph as well as the properties like font size etc
        font_properties = {'family': 'Arial',
                           'color':  'black',
                           'weight': 'heavy',
                           'size': 7,
                           'style': 'oblique'
        }

        plt.xlabel("States", fontdict = font_properties)
        plt.ylabel("Vaccinations", fontdict = font_properties)
        plt.title("Daily Vaccination by State", fontdict = font_properties)
        plt.rc('legend', fontsize = 4.5)
        plt.legend(loc = 'best')
        
        # Honestly I have no idea what these do but without them, the graph doesn't work properly
        plt.tick_params(labelsize = 5)
        plt.tight_layout()

        plt.savefig("images/_graphs/testfig.png")
        plt.show()

def main():
    big_plotta = Plotta()
    big_plotta.actualplot()

main()