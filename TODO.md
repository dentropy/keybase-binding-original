## TODO

- [ ] Break Generate Analytics into more classes
- [ ] *Fix public/private scoping on class properties and methods.*
- [ ] Hook up the database to `graphql`
- [ ] *Create a bot that automatically appends data to the `.sqlite` database with each new message on text channels it "lives" in.*
- [ ] *Use something like the `plotly` package to turn existing `Jupyter` notebooks into embeddable (or linkable) dashboards, which can then be accessed from the **[wiki](https://wiki.dentropydaemon.io/Dashboards)**, embedded in a local application, or hosted elsewhere?*
- [ ] *Record in database if reaction, or edit message was deleted*
- [ ] **Real time export / Sync up without full export** using pykeybasebot

## Design

- Write more methods for gathering user meta data
  - Take generalized list
  - Write a method to get all follow and followers from a single user


## Analytics Questions

*Questions or tasks requiring interaction with the data to generate actionable insight.*

- [ ] Describe the distribution of number of URLs posted by user. 
- [ ] Script to Export all attachments, must use `Keybase` daemon
- [ ] Generate as many graphs as reasonable using **[`generate_graphs.ipynb`](generate_graphs.ipynb)**

### Time

- [ ] Graph Messages Per Day
- [ ] Messages per day of week
- [ ] Messages per month
- [ ] Time of message per hour
 
#### Graphics ####

_List of graphics/kinds of data we still need to visualize._

Graph of [*data*] [*type*] broken down by [*view*], where [*type*] is:

- [ ] Total
- [ ] Channel
- [ ] User
- [ ] User in Channel
- [ ] Day of week

##### Example of "Activity" proxy

Average message length per

- [ ] Channel
- [ ] User

### Development

*What remains to be done with respect to writing more code and other dev-ops tasks?*

* How does this code scale to analyze multiple teams
* Coming up with Bot ideas for all this data
* Analysis functions to write

  - [ ] `reaction_popularity_per_topic` 
  * [ ] `user_recieved_most_reactions` 
  * [ ] `reaction_type_popularity_per_user` 