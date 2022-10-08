-- Keep a log of any SQL queries you execute as you solve the mystery.
-- The only crime report within this search mentions that the crime took place at 10:15 and three interviews took place with all mentioning "courthouse"
SELECT * FROM crime_scene_reports WHERE year="2020" AND month="7" AND day="28" AND street="Chamberlin Street";
-- The first interview tells us that within a 10 minute timeframe after the crime, the thief got into a car at the parking lot. 
-- The second interview tells us that the thief withdrew money on Fifer street.
-- The third interview tells us thata s the thief was leaving the courthouse, he called his associate and told him to purchase the earlest plane ticket out of fiftyville.
SELECT transcript FROM interviews WHERE year="2020" AND month="7" AND day="28" AND transcript LIKE "%courthouse%";
-- To get a list of account_numbers of people who withdrew money on Fifer Street
SELECT account_number FROM atm_transactions WHERE year="2020" AND month="7" AND day="28" AND atm_location="Fifer Street" AND transaction_type="withdraw";
-- To get a list of licence plates that left the parking lot at the specified time (10;15 to 10:25)
SELECT license_plate FROM courthouse_security_logs WHERE year="2020" AND month="7" AND day="28" AND hour="10" AND minute >15 AND minute<25;
-- To get a list of phone numbers of people who called for less than a minute on the sepcified day
SELECT caller from phone_calls WHERE year="2020" AND month="7" AND day="28" AND duration<61;
-- To find out passport number of all passengers on the earliest flight out of fiftyville 
SELECT passport_number FROM passengers
JOIN flights ON flights.id = passengers.flight_id
WHERE flights.id=(SELECT flights.id from flights JOIN airports ON airports.id = flights.origin_airport_id WHERE year="2020" AND month="7" AND day="29" AND city="Fiftyville" ORDER BY hour LIMIT 1);
-- To get the persons name based on phone number, id, and license plate
SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE phone_number IN (SELECT caller from phone_calls WHERE year="2020" AND month="7" AND day="28" AND duration<61)
AND account_number IN (SELECT account_number FROM atm_transactions WHERE year="2020" AND month="7" AND day="28" AND atm_location="Fifer Street" AND transaction_type="withdraw")
AND license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year="2020" AND month="7" AND day="28" AND hour="10" AND minute >15 AND minute<25)
AND passport_number in (SELECT passport_number FROM passengers JOIN flights ON flights.id = passengers.flight_id WHERE flights.id=(SELECT flights.id from flights JOIN airports ON airports.id = flights.origin_airport_id WHERE year="2020" AND month="7" AND day="29" AND city="Fiftyville" ORDER BY hour LIMIT 1));
-- To get the name of the accomplace 
SELECT name FROM people WHERE phone_number=(SELECT receiver FROM phone_calls WHERE caller=(Select phone_number FROM people WHERE name=(SELECT name FROM people JOIN bank_accounts ON bank_accounts.person_id = people.id WHERE phone_number IN (SELECT caller from phone_calls WHERE year="2020" AND month="7" AND day="28" AND duration<61) AND account_number IN (SELECT account_number FROM atm_transactions WHERE year="2020" AND month="7" AND day="28" AND atm_location="Fifer Street" AND transaction_type="withdraw") AND license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year="2020" AND month="7" AND day="28" AND hour="10" AND minute >15 AND minute<25) AND passport_number in (SELECT passport_number FROM passengers JOIN flights ON flights.id = passengers.flight_id WHERE flights.id=(SELECT flights.id from flights JOIN airports ON airports.id = flights.origin_airport_id WHERE year="2020" AND month="7" AND day="29" AND city="Fiftyville" ORDER BY hour LIMIT 1)))) AND duration<60);
-- To get the thiefs flight destination
SELECT city FROM airports
JOIN flights ON flights.destination_airport_id = airports.id
WhERE airports.id=(SELECT destination_airport_id FROM flights WHERE id=(SELECT flights.id from flights JOIN airports ON airports.id = flights.origin_airport_id WHERE year="2020" AND month="7" AND day="29" AND city="Fiftyville" ORDER BY hour LIMIT 1)) LIMIT 1;