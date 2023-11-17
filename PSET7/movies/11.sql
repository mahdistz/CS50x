SELECT title
FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WHERE people.name LIKE 'Chadwick Boseman'
ORDER BY (SELECT rating FROM ratings) DESC
LIMIT 5;