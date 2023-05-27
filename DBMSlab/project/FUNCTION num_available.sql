CREATE OR REPLACE FUNCTION num_available(
    tno INTEGER,
    src VARCHAR(4),
    dst VARCHAR(4),
    doj TIMESTAMP,
    c_typ VARCHAR(5)
) RETURNS INTEGER
-- implement waiting list later  
LANGUAGE plpgsql
AS $$
DECLARE
cnt INTEGER;
rec_res record;
rec_stBtw record;
rec record;
flag BOOLEAN;
BEGIN
    cnt := 0;
    FOR rec_res in SELECT DISTINCT coach_no AS coach_no_,seat_no AS seat_no_ FROM Reservation WHERE src_date=DOJ AND train_no=tno AND coach_type=c_typ LOOP
        flag := false;
        IF (SELECT count(*) FROM station_between(tno,src,dst) WHERE station_id != dst)=0 THEN
            flag := true;
        END IF;
        FOR rec_stBtw in SELECT * FROM station_between(tno,src,dst) WHERE station_id != dst LOOP
            IF (SELECT is_booked FROM Reservation WHERE src_date=DOJ AND train_no=tno AND coach_no=rec_res.coach_no_ AND seat_no=rec_res.seat_no_ AND station=rec_stBtw.station_id)='Y' THEN
                flag := true;
            END IF;
        END LOOP;
        IF flag=false THEN
            cnt := cnt+1;
        END IF;
    END LOOP;
    return cnt;
END;
$$;
