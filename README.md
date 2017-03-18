# course-eval-site

## Overview
This project is a dedicated course shopping site for Princeton University.

The minimal viable product includes all the information available on the [course registrar](https://registrar.princeton.edu/course-offerings/) (course description, meeting times, etc) along with all the information available on the course evaluation pages (overall ratings per semester, professor who taught it, student comments, etc).

For developers, data can be fetched through the OIT web feed url: http://etcweb.princeton.edu/webfeeds/courseofferings/?term=current&subject=all&fmt=json. <br>The parameters such as "term" or "subject" can be modified to return different results.

Sample [course evaluation page](https://reg-captiva.princeton.edu/chart/index.php?terminfo=1174&courseinfo=007998).
For each course, we will need to scrape from a similar evaluation page using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

There are currently three other teams working on review sites, so this space is potentially competitive.

### Getting Started
For backend, install MySQL on your local machine. Make sure to start the MySQL server. On MacOS, this can be done by opening  **System Preferences** and seleting **MySQL**.
Reset temporary root password to a password of your choice with the following commands in terminal.
```
mysql -u root -p
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('my-password');
```
Navigate to the project root directory. To create tables, run the script
```
python shopper/model_cloudsql.py
```
Then run the following script to fill tables with fall16-spring17 course offerings data.
```
python db_populate.py
```
To start the python app on localhost, run the script
```
python main.py
```
Open http://localhost:8080/

### TODOs

The following features make up a minimal viable product. Each is implemented at your own discretion.
The web application is based on Flask and SQL. We probably also need to make use of browser cache and use local copies of libraries. **No CDN links if possible. Latency is noticeable, particularly for UI elements.**

- [ ] UI

  - The UI is work-in-progress, but has been significantly improved from the one currently on github. I'll show it to you all at our next meeting. This is something that will be iteratively improved as we connect more of the backend.

- [ ] Database

  - Entities requiring models: User, Course, Review, Professor
  - Google Cloud appears to be the best option. We'll need to abandon the current database code, which won't be compatible     with gcloud.

    https://cloud.google.com/python/getting-started/hello-world

    https://cloud.google.com/appengine/docs/flexible/python/using-cloud-datastore


- [ ] Scrapers

  - We need to scrape the evaluation pages because currently there is no web feed available and there will not be one             coming from the Office of the Registrar any time soon. TigerApps has been working on getting a centralized data source         but it is still work in progress and definitely not applicable for the time-scale we have to work with.

- [ ] Rant Space

  - Dedicated space for Quizzes, Midterm, and Finals where people can talk about what happened, whine, etc.
    People can get a feel of what the curve is gonna be from that. Yak used to be an outlet for that before it died. Let's      give students an official place for that kind of stuff.

- [ ] Course Forum

  - Users should be able to post comments apart from the existing scraped reviews. Think Yak feeds for courses. There             should at least be a posting mechanism with replies, and an upvote/downvote system. It should be as simple as                 possible.

- [ ] Alternative Course Info Source

  - This is our opportunity to put up hilarious but truthful course description (like Urban Dictionary). (Courses that would benefit from this: Physics for Future Leaders, Clapping for Credit, rocks for jocks, ...). We could crowdsource this feature by allowing users to submit their own course descriptions. Of course, the official description must be available, but students can also switch between the real and urban version.
  - Also, links to [Principedia](http://principedia.princeton.edu/) would be beneficial.

- [ ] Fully functional Cart Checkout System

  - Users can add courses to their cart. At checkout, users should be able to sync their selected courses with their ReCal         queue. This will involve the ReCal team, so we will need to continue to reach out to get this feature enabled.

- [ ] Any additional features that I've missed.

### Spring Break
Let's plan on making at least the **UI, Database, Scrapers** during break. There actually isn't much time to finish a project of this scale if we don't frontload.

### We need to replicate every feature available on Course Offerings, and integrate Course Evaluations. By Sunday March 26 11:59pm, we should have a live site hosted on Google Cloud where people can do everything they can do on Course Offerings. Then, we'll start user testing when class starts again.

### After Break
We might be potentially looking at >= 5-10 hours a week of work on this project, which is barely anything if you've worked on large projects before. If this is your first time, this will be a rewarding experience. But keep in mind that even with 5 developers, it is difficult to launch a production-ready app. As I mentioned before, we will be "competing" with other teams, and it's possible that students aren't interested in this site at all.

To ensure that there is interest, we should be making good progress each week and getting new users to try out prototypes. I highly recommend that you guys watch this [presentation](https://developer.apple.com/videos/play/wwdc2014/223/) from WWDC 16 if you haven't before. You'll need to use Safari.


**The following are tentatively assigned roles. But feel free to swap or tackle each task together.**

**Bold** = application-critical, *Italics* = major feature

- **UI** (Integrate views with database) - Yun, Chris
- **Database** (gcloud datastore) - Thomas, Jordan, Yun
- **Course Evaluation Scrapers** (Scrape all data once and load it into models, then insert into database) - Alex, Thomas
- *Rant Space* - Anyone available
- *Course Forum* (this will involve collaboration with UI and Database.) - Chris, Jordan
- ReCal Integration - Anyone available
- Alternative Course Dictionary - Alex

Finally, we'll need a good website name. Ideally, we don't go with the overused "Tiger+something" naming scheme that plagues all university apps.
