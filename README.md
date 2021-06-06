# RPA Challenge - IT Dashboard
[**https://www.notion.so/RPA-Challenge-IT-Dashboard**](https://www.notion.so/RPA-Challenge-IT-Dashboard-ec59bc2659e64323a7af99fcd4d24c21)

Our mission is to enable all people to do the best work of their lives—the first act in achieving that mission is to help companies automate tedious but critical business processes. This RPA challenge should showcase your ability to build a bot for purposes of process automation.

## Challenge
Your challenge is to automate the process of extracting data from [**itdashboard.gov**](http://itdashboard.gov/).

- The bot should get a list of agencies and the amount of spending from the main page
    - Click "**DIVE IN"** on the homepage to reveal the spend amounts for each agency
    - Write the amounts to an excel file and call the sheet "**Agencies**".
- Then the bot should select one of the agencies, for example, National Science Foundation (this should be configured in a file or on a Robocloud)
- Going to the agency page scrape a table with all "**Individual Investments**" and write it to a new sheet in excel.
- If the "**UII**" column contains a link, open it and download PDF with Business Case (button "**Download Business Case PDF**")
- Your solution should be submitted and tested on [**Robocloud**](https://cloud.robocorp.com/).
- Store downloaded files and Excel sheet to the root of the `output` folder


## Notes
Please leverage pure python using the **[rpaframework](https://rpaframework.org/)** for this exercise

> Bonus: We are looking for people that like going the extra mile if time allows or if your curiosity gets the best of you 😎

> Extract data from PDF. You need to get the data from **Section A** in each PDF. Then compare the value "**Name of this Investment**" with the column "**Investment Title**", and the value "**Unique Investment Identifier (UII)**" with the column "**UII**"

Up for the challenge? Share your organization on the [**Robocloud**](https://cloud.robocorp.com/) with [**support@thoughtfulautomation.com**](mailto:support@thoughtfulautomation.com) once your are done!
