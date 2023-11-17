-- Keep a log of any SQL queries you execute as you solve the mystery.

--All you know is that the theft
--took place on July 28, 2021 and that it
--took place on Chamberlin Street.


-- Define a CTE to get the date of the theft
WITH theft_date AS (
  SELECT '2021-07-28' AS date
)


-- Start with crime_scene_reports table
SELECT * FROM crime_scene_reports;


-- Get the description of the theft
SELECT description FROM crime_scene_reports
WHERE date BETWEEN theft_date AND theft_date + INTERVAL 1 DAY

-- Get the names and transcripts of the witnesses
SELECT name, transcript FROM interviews
INNER JOIN theft_date ON interviews.date = theft_date.date
WHERE transcript LIKE '%bakery%'
ORDER BY name

-- Get the account number and amount of the ATM withdrawal
SELECT account_number, amount FROM atm_transactions
INNER JOIN theft_date ON atm_transactions.date = theft_date.date
WHERE atm_location = 'Leggett Street'
AND transaction_type = 'withdraw'

-- Get the names of the people associated with the account numbers
SELECT name, atm_transactions.amount FROM people
INNER JOIN bank_accounts ON people.id = bank_accounts.person_id
INNER JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
INNER JOIN theft_date ON atm_transactions.date = theft_date.date
WHERE atm_transactions.atm_location = 'Leggett Street'
AND atm_transactions.transaction_type = 'withdraw'

-- Get the flight information for the earliest flight on July 29 from the Fiftyville airport
SELECT flights.id, full_name, city, flights.hour, flights.minute FROM airports
INNER JOIN flights ON airports.id = flights.destination_airport_id
WHERE flights.origin_airport_id = (
  SELECT id
  FROM airports
  WHERE city = 'Fiftyville'
)
AND flights.date = theft_date.date + INTERVAL 1 DAY
ORDER BY flights.hour, flights.minute

-- Get the names of the passengers on the earliest flight on July 29 from the Fiftyville airport
SELECT passengers.flight_id, name, passengers.passport_number, passengers.seat FROM people
INNER JOIN passengers ON people.passport_number = passengers.passport_number
INNER JOIN flights ON passengers.flight_id = flights.id
WHERE flights.date = theft_date.date + INTERVAL 1 DAY
AND flights.hour = 8
AND flights.minute = 20
ORDER BY passengers.passport_number

-- Get the names of the people who made phone calls less than a minute long on the day of the theft
SELECT name, phone_calls.duration FROM people
INNER JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE phone_calls.date = theft_date.date
AND phone_calls.duration <= 60
ORDER BY phone_calls.duration

-- Get the names of the people who received phone calls less than a minute long on the day of the theft
SELECT name, phone_calls.duration FROM people
INNER JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE phone_calls.date = theft_date.date
AND phone_calls.duration <= 60
ORDER BY phone_calls.duration

-- Get the names of the people who exited the bakery within 10 minutes of the theft
SELECT name, bakery_security_logs.hour, bakery_security_logs.minute FROM people
INNER JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE bakery_security_logs.date = theft_date.date
AND bakery_security_logs.activity = 'exit'
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute BETWEEN 15 AND 25
ORDER BY bakery_security_logs.minute