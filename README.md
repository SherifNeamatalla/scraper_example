To prepare the environment for running the scripts please do the following:

1.Make sure you have python3 installed.

2.Make sure you have pip installed.

3.Run pip install -r requirements.txt.

To run the script please run main.py first to scrap the webpage, this should generate result.html which will contain all
the scrapped participants tags.

After this you should be able to run excel_creator.py which will transform each tag in the previously saved file to a
row in a pandas dataframe and save the whole thing to result.xlsx excel file.