CREATE OR REPLACE PROCEDURE reserve_seat(
    tno INTEGER,
    src VARCHAR(4),
    dst VARCHAR(4),
    doj TIMESTAMP,  -- doj is start date of train's src stn
    c_typ VARCHAR(5),
    usr_id INTEGER,
    trxn_id INTEGER,
    pass_ids TEXT
)
-- implement waiting list later
LANGUAGE plpgsql
AS $$
DECLARE
    rec_res record;
    rec_stBtw record;
    rec_pass record;
    flag BOOLEAN;
    pnr_no_ INTEGER;
    bkng_no INTEGER;
    totalFare INTEGER;
    pass_ids_arr INTEGER[];
BEGIN
    -- Convert the comma-separated string to an array
    pass_ids_arr := string_to_array(pass_ids, ',');

    IF (SELECT num_available(tno,src,dst,doj,c_typ)) < array_length(pass_ids_arr, 1) THEN
        RAISE NOTICE 'Not enough seats available';
        RETURN;
    END IF;

    -- generating pnr number and booking number
    SELECT count(*) INTO pnr_no_ FROM pass_tkt;
    pnr_no_ := pnr_no_ + 56734512;
    SELECT count(*) INTO bkng_no FROM Booking;
    bkng_no := bkng_no + 73772234;

    -- for each passenger
    FOR rec_pass IN SELECT unnest(pass_ids_arr) AS passr_id LOOP
        FOR rec_res IN SELECT DISTINCT coach_no AS coach_no_,seat_no AS seat_no_ FROM Reservation WHERE src_date=DOJ AND train_no=tno AND coach_type=c_typ LOOP
            flag := false;
            FOR rec_stBtw IN SELECT * FROM station_between(tno,src,dst) WHERE station_id != dst LOOP
                IF (SELECT is_booked FROM Reservation WHERE src_date=DOJ AND train_no=tno AND coach_no=rec_res.coach_no_ AND seat_no=rec_res.seat_no_ AND station=rec_stBtw.station_id)='Y' THEN
                    flag := true;
                END IF;
            END LOOP;

            -- when a suitable seat is found
            IF flag=false THEN
                -- INITIATE BOOKING PROCESS for the passenger 

                -- mark the seat booked for the entire duration (except dest) in Reservation table
                FOR rec_stBtw IN SELECT * FROM station_between(tno,src,dst) WHERE station_id != dst LOOP
                    UPDATE Reservation
                    SET is_booked='Y' WHERE src_date=DOJ AND train_no=tno AND coach_no=rec_res.coach_no_ AND seat_no=rec_res.seat_no_ AND station=rec_stBtw.station_id;
                END LOOP;

                -- add to pass_tkt table
                INSERT INTO pass_tkt ("pnr_no","src_date","pass_id","booking_id","train_no","coach_no","seat_no","food_order_id","src","dest","isConfirmed")
                VALUES
                (pnr_no_,doj,rec_pass.passr_id,bkng_no,tno,rec_res.coach_no_,rec_res.seat_no_,NULL,src,dst,'CNF');


                EXIT;
                -- BOOKING DONE
            END IF;
        END LOOP;
    END LOOP;

    totalFare := 35 + array_length(pass_ids_arr, 1)*(SELECT count(*) FROM station_between(tno,src,dst))*30 + 0;

    -- add to booking table
    INSERT INTO Booking ("booking_id","fare","txn_id","user_id","booking_date")
    VALUES
    (bkng_no,totalFare,trxn_id,usr_id,NOW());

END;
$$; 