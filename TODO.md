## TODO

- [✅] Put all classes in modules folder
- [✅] Break Generate Analytics into more classes
- [✅] Rename GenerateAnalytics into KeybaseAnalytics and MessageAnalytics
- [ ] create_export_example.py should take a list of teams to export
- [ ] Document how to setup cron_export
- [ ] Add calmap to dependencies or replace it
- [ ] *Fix public/private scoping on class properties and methods.*
- [ ] Hook up the database to `graphql`
- [ ] *Create a bot that automatically appends data to the `.sqlite` database with each new message on text channels it "lives" in.*
- [ ] *Use something like the `plotly` package to turn existing `Jupyter` notebooks into embeddable (or linkable) dashboards, which can then be accessed from the **[wiki](https://wiki.dentropydaemon.io/Dashboards)**, embedded in a local application, or hosted elsewhere?*
- [ ] *Record in database if reaction, or edit message was deleted*
- [ ] **Real time export / Sync up without full export** using pykeybasebot

## Bugs

- [ ] Exporting User Metadata for complexweekend.oct2020 produced an error, use try and catch blocks and say that the user does not work

## Design

- Write more methods for gathering user meta data
  - Take generalized list
  - Write a method to get all follow and followers from a single user


## Analytics Questions

*Questions or tasks requiring interaction with the data to generate actionable insight.*
- [ ] Describe the distribution of number of URLs posted by user. 
- [ ] Script to Export all attachments, must use `Keybase` daemon

## Analysis TODO

- [ ] `reaction_popularity_per_topic` 
- [ ] `user_recieved_most_reactions` 
- [ ] `reaction_type_popularity_per_user` 
- [ ] Activity Proxy
  - [ ] Average message length per Channel
  - [ ] Average message length per User


### Time

- [ ] Graph Messages Per Day
  - Bug working across years
- [✅] Messages per day of week
- [✅] Time of message per hour
- [ ] Messages per month
 
#### Graphics ####

_List of graphics/kinds of data we still need to visualize._

Graph of [*data*] [*type*] broken down by [*view*], where [*type*] is:

- [ ] Total
- [ ] Channel
- [ ] User
- [ ] User in Channel
- [ ] Day of week


### Development

*What remains to be done with respect to writing more code and other dev-ops tasks?*

* Coming up with Bot ideas for all this data
* Analysis functions to write
