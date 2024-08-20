# LilBot - A little bot project
<img src="https://github.com/user-attachments/assets/47b322a3-04bc-4afa-8fc6-58b59da61937" width="200">

Built using [discord.py](https://github.com/Rapptz/discord.py "discord.py GitHub") in Python  
Author: [Tan Yong Rui](https://www.linkedin.com/in/yong-rui-tan/)

---

## Features

| Music Player Features         | Command Group | Command      | Remarks                                        |
| :---------------------------- | :------------ | :----------- | :--------------------------------------------- |
| Play a YouTube video          | /youtube      | play         |                                                |
| Skip music                    | /youtube      | next OR skip |                                                |
| Pause music                   | /youtube      | pause        |                                                |
| Resume music                  | /youtube      | resume       |                                                |
| Repeat a track / queue        | /youtube      | repeat       | toggles between 3 repeat modes                 |
| Remove a track from queue     | /youtube      | remove       |                                                |
| Stop music player             | /youtube      | stop         |                                                |
| Clear queue                   | /youtube      | clear        | currently does not auto-clear after inactivity |
| Check current track           | /youtube      | current      |                                                |
| Go to specific track in queue | /youtube      | goto         |                                                |
| Shuffle queue                 | /youtube      | shuffle      | not implemented yet                            |
| Play a Spotify Track          | /spotify      | play         | assumes track exists on YouTube                |

| Vote/Poll Features                | Command Group | Command          | Remarks |
| :-------------------------------- | :------------ | :--------------- | :------ |
| Create yes-no vote                | /vote         | yes-no           |         |
| Create vote with multiple options | /vote         | multiple-options |         |

| Message Management Features      | Command Group | Command | Remarks |
| :------------------------------- | :------------ | :------ | :------ |
| Delete a number of messages      | /message      | delete  |         |
| Delete a number of bots messages | /message      | clean   |         |
| Make bot repeat a sentence       | /message      | say     |         |

| User Management Features       | Command Group | Command          | Remarks |
| :----------------------------- | :------------ | :--------------- | :------ |
| Register yourself with the bot | /user         | register_me      |         |
| Register user with the bot     | /user         | register_user    |         |
| Deregister user with the bot   | /user         | deregister_user  |         |
| Change registered user's role  | /user         | update_user_role |         |
| Check registered user's info   | /user         | user_info        |         |

---

## Features to implement

- [x] Youtube music player
  - [x] Repeat track / queue
  - [x] Manage music queue
  - [x] Search with keywords
  - [x] Search with URLs
  - [x] Insert entire playlists
  - [ ] Add shuffle functionality
  - [ ] Remove a range of songs from playlist
- [x] Spotify music player
  - [ ] Insert entire playlists
- [x] Message management
  - [x] Delete messages
  - [ ] Delete specific user messages
  - [x] Repeat after user
- [x] Registration of users
  - [x] Custom roles for users
- [x] Creation of votes / polls
- [ ] Ask OpenAI (or other AI bots) a question

---

## Installation

1. PLACEHOLDER
2.

---
