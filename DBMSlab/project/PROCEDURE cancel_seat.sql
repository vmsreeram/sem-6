CREATE OR REPLACE PROCEDURE cancel_seat(
    pnr_no_ INTEGER,
    usr_id INTEGER,     -- either the pass himself or some privileged user can initiate cancellation
    pass_ids TEXT
)
-- implement waiting list later
LANGUAGE plpgsql
AS $$
DECLARE
    rec_stBtw record;
    rec_pass record;
    bkng_no INTEGER;
    totalFare INTEGER;
    trxn_id_ INTEGER;
    pass_ids_arr INTEGER[];
    src_ VARCHAR(4);
    dst_ VARCHAR(4);
    coach_no_ VARCHAR(4);
    seat_no_ INTEGER;
    tno_ INTEGER;
    DOJ TIMESTAMP;
BEGIN
    -- Convert the comma-separated string to an array
    pass_ids_arr := string_to_array(pass_ids, ',');

    IF ((SELECT count(*) FROM pass_tkt where pnr_no=pnr_no_) = 0) THEN
        RAISE NOTICE 'No such booking found with specified pnr number';
        RETURN;
    END IF;
    -- fetching booking number, trxn_id, tno_
    SELECT booking_id INTO bkng_no FROM pass_tkt where pnr_no=pnr_no_;
    -- RAISE NOTICE 'bkng_no (%)', bkng_no;

    SELECT MAX(txn_id) INTO trxn_id_ FROM Booking where booking_id=bkng_no;        --select highest txn id; multiple part-cancellations allowed
    -- RAISE NOTICE 'MAX(txn_id) (%)', trxn_id_;
    
    SELECT train_no INTO tno_ FROM pass_tkt where pnr_no=pnr_no_;
    -- RAISE NOTICE 'tno_ (%)', tno_;

    SELECT src_date INTO DOJ FROM pass_tkt where pnr_no=pnr_no_;
    -- RAISE NOTICE 'DOJ (%)', DOJ;

    totalFare := 0;       -- base fare not to be refunded

    -- for each passenger who wish to be cancelled
    FOR rec_pass IN SELECT unnest(pass_ids_arr) AS passr_id LOOP
        -- getting src dst for that pass; general case
        SELECT src INTO src_ FROM pass_tkt where pnr_no=pnr_no_ AND pass_id=rec_pass.passr_id;
        SELECT dest INTO dst_ FROM pass_tkt where pnr_no=pnr_no_ AND pass_id=rec_pass.passr_id;
        SELECT coach_no INTO coach_no_ FROM pass_tkt where pnr_no=pnr_no_ AND pass_id=rec_pass.passr_id;
        SELECT seat_no INTO seat_no_ FROM pass_tkt where pnr_no=pnr_no_ AND pass_id=rec_pass.passr_id;

        UPDATE pass_tkt SET "isConfirmed"='CAN' WHERE pnr_no=pnr_no_ AND pass_id=rec_pass.passr_id;
        totalFare := totalFare + (SELECT count(*) FROM station_between(tno_,src_,dst_))*25 + 0;

        -- mark the seat unbooked for the entire duration (except dest) in Reservation table
        FOR rec_stBtw IN SELECT * FROM station_between(tno_,src_,dst_) WHERE station_id != dst_ LOOP
            UPDATE Reservation
            SET is_booked='N' WHERE src_date=DOJ AND train_no=tno_ AND coach_no=coach_no_ AND seat_no=seat_no_ AND station=rec_stBtw.station_id;
        END LOOP;
        RAISE NOTICE 'cancelled pass_id = %', (rec_pass.passr_id);
    END LOOP;

    totalFare := totalFare * -1;

    -- add to booking table
    INSERT INTO Booking ("booking_id","fare","txn_id","user_id","booking_date")
    VALUES
    (bkng_no,totalFare,(trxn_id_*2)+1,usr_id,NOW());
    RAISE NOTICE 'refund ₹%', (-1*totalFare);

END;
$$; 