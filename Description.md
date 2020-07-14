## All serverside consists of two service: Authorization and Data Controll Apps.

# Authorization App usage:
1. Registration, login, logout
2. Modify user's data
3. Get data_id to user for Data Controll App, where data id lets user do get counterparty data
4. Store data_id for stored data by Data Controll App
5. Provide admin interface for Authorization App and for Data Controll App's database

Realization: Python3, Django + DRF and Postgres

# Data Controll App usage:
1. Store authorized user's data
2. Get acess to stored data only for authorized user and then remove this data

Realization: Python3, Tornado and MongoDB(maybe other NoSQL database or even Postgres)