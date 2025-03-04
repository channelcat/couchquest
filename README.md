Couch Quest App
===

Makes drinking games using subtitles + AI.

# How to run
 * `docker compose up`
 * `docker compose run --rm shell aerich upgrade`
 * Navigate to http://localhost:3000

# How to update the DB
 * `docker compose run --rm shell aerich migrate`
 * `docker compose run --rm shell aerich upgrade`

# How to update live
 * commit+push to main branch
 * Navigate to https://couchquest.app