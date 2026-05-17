# ST1_Assessment-3
# Macroinvertebrate Image Analyser
This project performs EDAs on a macroinvertebrate dataset from Kaggle.com
It can show the distribution of classes and image sizes, as well as plots of the width and heights, and the heights by class.

# Usage
You can upload more images to the dataset by using the interface, BUT MAKE SURE THEY ARE .PNG FILES, as the system in its current state does not support any other file formats, and will not work correctly as it does not contain error handling for the upload of other file types.
To upload files, first ensure you're in the 'manage files' menu, then press 'upload file' and select an image. Next select what class that image belongs to from the dropdown menu, and once that's ready you can press 'upload' and your image will be added to the database.

To view the data analysis, you'll first need to head to the EDA menu, then press 'refresh' to index the dataset. Once that's done, select your desired classes and press 'Perform EDA' to perform the analysis.
From there you can click on each graph option to toggle its visibility.

# Installation
Once you have the project installed, you'll need to make sure you have all the python libraries listed in 'requirements.txt' (pathlib, dataclasses, pandas, opencv-python, matplotlib, seaborn, tkinter, joblib, typing, pillow, shutil, threading) installed, which can be done by entering 'pip install [library name here]' into the command shell.

After that, you should be good to go! Just run 'main.py' and you're off.
(Side note: windows users *may* need to replace line 5 of 'main.py' ("import macro_project.src.gui as gui") with "import gui as gui")