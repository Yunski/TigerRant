# Project Tigershop

## Overview
This project is a dedicated course shopping site for Princeton University.

The goal is provide students with a supplemental information source, such as unfiltered student reviews, an urban dictionary with course descriptions, and a yak-like real-time posting mechanism to keep shoppers and enrolled students up to speed. Students have the option of following courses and getting notifications.

Our website still provides the official course offerings information, but students now have the opportunity to read exclusive content and contribute their own.

We hope that this will make course shopping more fun and informative.
The final feature of our website is a shopping cart that syncs with a user's ReCal calendar.

Timeline
- [x] 3/26: (Pre-alpha test) website should be live, complete with CAS login and supporting every search option (dept, distribution, professor, title, meeting times) that Course Offerings has with the addition of course ratings and student reviews. MySQL database is complete with all relevant tables and indices. No interaction features yet.
- [x] 4/10 - (Alpha Test) Revise UI based on user feedback. Fix any bugs. Brainstorm upcoming features.
- [x] 4/12 - (Prototype) Add REST api and update AngularJS code. Add review posting, rating, and thumbs-up functionality. Add Rant Space (posting and upvote/downvote feature). Add Course Urban Dictionary (posting and upvote/downvote feature).
- [X] 4/16 - The week before fall 2017 course selection period.
(Beta Test): Add cart and allow toggling between course offerings page content and student content.
ReCal integration may not be available due to ReCal's work schedule.
- [X] 4/24 - 5/3: (fall 2017 course selection period) Monitor app and fix issues. Add Dockerfile.
- [ ] 5/16: Dean’s Date and submission deadline

## Elevator Pitch
Imagine this. You’re on our new course shopping website. You prepare to be bored and think it’s just another one of “those” sites that always crop up every year in 333. You search for “COS 333” out of spite. Then you see what makes it different. 

Our shopping site is powered by user-generated content. You can leave “urban dictionary” style descriptions of courses like the classic “Stars for Stoners,” “Bridges,” or “Build a Product but not maintain when the semester’s over.”

You can leave rants at any time during the semester. See how people’s opinions of a course change over time! See why people dropped a class, people who normally wouldn’t be able to leave a course evaluation!

Or leave insightful comments long after you’ve taken a class like “I never expected to be asked coding interview questions straight from an ORF 309 pset” or “Wow one 333 assignment in Python taught me how to make TigerMenus” or “easy A” on PHY 205 (Death Mech). 

You can see student’s thoughts at all times during the semester, not just during the end like course evaluations. This data will be saved for posterity, unlike Yik Yak. And the data will be centrally located, unlike realTalkPrinceton. This is the next big thing in course shopping. This is TigerShop.
