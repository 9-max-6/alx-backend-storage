-- Creates a view called need_meeting that includes all students with a score below 80
-- and either no last_meeting or a last_meeting that occurred more than 1 month ago.
DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS
    SELECT name
        FROM students
        WHERE score < 80 AND
            (
                last_meeting IS NULL
                OR last_meeting < SUBDATE(CURRENT_DATE(), INTERVAL 1 MONTH)
            )
;