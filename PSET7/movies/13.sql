SELECT name
FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE movies.id IN (
  SELECT movie_id
  FROM stars
  JOIN people ON stars.person_id = people.id
  WHERE people.name LIKE 'Kevin Bacon' AND people.birth LIKE 1958
) AND people.name != 'Kevin Bacon';