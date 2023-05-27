CREATE OR REPLACE FUNCTION station_between(
    p_train_no INTEGER,
    p_start_stn VARCHAR(4),
    p_end_stn VARCHAR(4)
) RETURNS TABLE(station_id VARCHAR(4)) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT stn_id
    FROM Schedule
    WHERE train_no = p_train_no 
    AND (
            ( -- single day travel
                (
                    (
                        SELECT "Dayofjny"
                        FROM Schedule
                        WHERE train_no = p_train_no AND stn_id = p_start_stn
                    )
                    =
                    (
                        SELECT "Dayofjny"
                        FROM Schedule
                        WHERE train_no = p_train_no AND stn_id = p_end_stn
                    )
                ) AND (
                    "Dayofjny" = (
                        SELECT "Dayofjny"
                        FROM Schedule
                        WHERE train_no = p_train_no AND stn_id = p_start_stn
                    )
                ) AND (
                    dep_time >= (
                        SELECT dep_time
                        FROM Schedule
                        WHERE train_no = p_train_no AND stn_id = p_start_stn
                    )
                ) AND (
                    arr_time <= (
                        SELECT arr_time
                        FROM Schedule
                        WHERE train_no = p_train_no AND stn_id = p_end_stn
                    )
                )
            )
            OR
            ( -- multi day travel
                (
                    (
                        SELECT "Dayofjny"
                        FROM Schedule
                        WHERE train_no = p_train_no AND stn_id = p_start_stn
                    )
                    <
                    (
                        SELECT "Dayofjny"
                        FROM Schedule
                        WHERE train_no = p_train_no AND stn_id = p_end_stn
                    )
                ) AND 
                (
                    ( -- first doj
                        (
                            "Dayofjny" = (
                                SELECT "Dayofjny"
                                FROM Schedule
                                WHERE train_no = p_train_no AND stn_id = p_start_stn
                            )
                        ) AND (
                            dep_time >= (
                                SELECT dep_time
                                FROM Schedule
                                WHERE train_no = p_train_no AND stn_id = p_start_stn
                            )
                        )
                    )
                    OR
                    ( -- last doj
                        (
                            "Dayofjny" = (
                                SELECT "Dayofjny"
                                FROM Schedule
                                WHERE train_no = p_train_no AND stn_id = p_end_stn
                            )
                        ) AND (
                            arr_time <= (
                                SELECT arr_time
                                FROM Schedule
                                WHERE train_no = p_train_no AND stn_id = p_end_stn
                            )
                        )
                    )
                    OR
                    ( -- intermediate doj
                        (
                            "Dayofjny" > (
                                SELECT "Dayofjny"
                                FROM Schedule
                                WHERE train_no = p_train_no AND stn_id = p_start_stn
                            )
                        ) AND (
                            "Dayofjny" < (
                                SELECT "Dayofjny"
                                FROM Schedule
                                WHERE train_no = p_train_no AND stn_id = p_end_stn
                            )
                        )
                    )
                )
            )
        )
    ORDER BY "Dayofjny",dep_time;
END;
$$;