import os, random

caracal_img_list = os.listdir("./images/caracals")
caracal_img_string = random.choice(caracal_img_list)
print(caracal_img_string)