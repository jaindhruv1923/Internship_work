-- answer 1.1 
SELECT
    status,
    COUNT(*) AS request_count
FROM chc_request
WHERE deleted = 0
GROUP BY status
ORDER BY request_count DESC;

-- answer 1.2
SELECT
    id,
    code,
    status,
    count_as_in
FROM gate_pass_status
ORDER BY id ASC;

-- answer 1.3 

SELECT
    occupant_ukid,
    infrastructure_id,
    child_infrastructure_id,
    allotment_start_date,
    allotment_end_date
FROM hostel_allotment
WHERE status = 'confirmed'
  AND child_infrastructure_id IS NOT NULL
ORDER BY allotment_start_date DESC;

-- answer 1.4

SELECT
    po.name AS organisation,
    pj.designation,
    pj.last_date,
    pj.vacancies
FROM placement_job pj
JOIN placement_organization po
    ON pj.organization_id = po.id
WHERE pj.is_published = 1
  AND pj.is_closed = 0
  AND pj.is_deleted = 0
ORDER BY pj.last_date DESC;

-- answer 1.5

SELECT
    booking_module,
    COUNT(*) AS total_bookings,
    SUM(CASE WHEN status = 'CANCELLED' THEN 1 ELSE 0 END) AS cancelled_bookings
FROM infra_booking
WHERE deleted = 0
GROUP BY booking_module
ORDER BY total_bookings DESC;

-- answer 2.1

SELECT
    cr.service_id,
    cs.title AS service_title,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN cr.status = 'closed' THEN 1 ELSE 0 END) AS closed,
    SUM(CASE WHEN cr.status IN ('submitted', 'pending') THEN 1 ELSE 0 END) AS open_requests,
    SUM(CASE WHEN cr.status = 'failed' THEN 1 ELSE 0 END) AS failed
FROM chc_request cr
JOIN chc_service cs
    ON cr.service_id = cs.id
WHERE cr.deleted = 0
GROUP BY cr.service_id, cs.title
ORDER BY total_requests DESC
LIMIT 10;

-- answer 2.2

SELECT
    gpl.ukid,
    gps.status AS status_label,
    gpl.out_entry,
    gpl.pass_type,
    TIMESTAMPDIFF(HOUR, gpl.out_entry, NOW()) AS hours_out
FROM gate_pass_log gpl
JOIN gate_pass_status gps
    ON gpl.status_id = gps.id
WHERE gpl.out_entry IS NOT NULL
  AND gpl.in_entry IS NULL
  AND gps.status IN ('Out of Campus', 'Out of Campus (Running Late)')
ORDER BY hours_out DESC;

-- answer 2.3

SELECT
    iv_bld.name AS building,
    COUNT(*) AS confirmed_allotments
FROM hostel_allotment ha
JOIN infrastructure_version iv_room
    ON ha.infrastructure_id = iv_room.id
JOIN infrastructure_version iv_bld
    ON iv_room.parent_id = iv_bld.id
WHERE ha.status = 'confirmed'
GROUP BY iv_bld.name
ORDER BY confirmed_allotments DESC;

-- answer 2.4

SELECT
    po.name AS organisation,
    pj.designation,
    COUNT(pa.id) AS applications,
    SUM(CASE WHEN pas.name LIKE '%Shortlist%' THEN 1 ELSE 0 END) AS shortlisted,
    SUM(CASE WHEN pas.name = 'Selected' THEN 1 ELSE 0 END) AS selected,
    SUM(CASE WHEN pos.name = 'Accept' THEN 1 ELSE 0 END) AS offers_accepted
FROM placement_application pa
JOIN placement_job pj
    ON pa.job_id = pj.id
JOIN placement_organization po
    ON pj.organization_id = po.id
LEFT JOIN placement_application_status pas
    ON pa.status_id = pas.id
LEFT JOIN placement_offer_status pos
    ON pa.offer_status_id = pos.id
WHERE pa.is_deleted = 0
GROUP BY pj.id, po.name, pj.designation
ORDER BY applications DESC
LIMIT 10;

-- answer 2.5

SELECT
    tr.name AS route,
    trpp.sequence AS stop_sequence,
    tpp.name AS pickup_point,
    COUNT(ta.id) AS confirmed_students
FROM transport_allotment ta
JOIN transport_route_pickup_point trpp
    ON ta.option_id = trpp.id
JOIN transport_route tr
    ON trpp.route_id = tr.id
JOIN transport_pickup_point tpp
    ON trpp.pickup_point_id = tpp.id
WHERE ta.status = 'CONFIRMED'
GROUP BY tr.name, trpp.sequence, tpp.name
ORDER BY route ASC, stop_sequence ASC;

-- answer 3.1
WITH request_summary AS (
    SELECT
        cr.id AS request_id,
        cr.service_id,
        COUNT(cwra.id) AS action_count,
        TIMESTAMPDIFF(SECOND, cr.created_on, MAX(cwra.created_on)) / 3600.0 AS hours_to_close
    FROM chc_request cr
    JOIN chc_work_centre_request_action cwra
        ON cr.id = cwra.request_id
    WHERE cr.status = 'closed'
      AND cr.deleted = 0
    GROUP BY cr.id, cr.service_id, cr.created_on
)
SELECT
    cs.title AS service,COUNT(rs.request_id) AS closed_requests,
    ROUND(AVG(rs.action_count), 2) AS avg_actions,
    ROUND(AVG(rs.hours_to_close), 2) AS avg_hours_to_close
FROM request_summary rs
JOIN chc_service cs
    ON rs.service_id = cs.id
GROUP BY rs.service_id, cs.title
HAVING closed_requests >= 20
ORDER BY avg_hours_to_close DESC;

-- answer 3.2

SELECT
    gplp.ukid,
    cs.title AS service,
    cr.id AS chc_request_id,
    gplp.pass_start,
    gplp.pass_end,
    gpl.in_entry,
    TIMESTAMPDIFF(MINUTE, gplp.pass_end, gpl.in_entry) AS minutes_late
FROM gate_pass_long_pass gplp
JOIN gate_pass_log gpl
    ON gplp.log_id = gpl.id
JOIN chc_middleware cm
    ON gplp.middleware_id = cm.id
JOIN chc_request cr
    ON cm.request_id = cr.id
JOIN chc_service cs
    ON cr.service_id = cs.id
WHERE gpl.in_entry > gplp.pass_end
ORDER BY minutes_late DESC;

-- answer 3.3
SELECT
    ha.occupant_ukid AS ukid,
    iv_bld.name AS building,
    iv_room.name AS room,
    tr.name AS route,
    tpp.name AS pickup_point
FROM hostel_allotment ha
JOIN infrastructure_version iv_room
    ON ha.infrastructure_id = iv_room.id
JOIN infrastructure_version iv_bld
    ON iv_room.parent_id = iv_bld.id
JOIN transport_allotment ta
    ON ha.occupant_ukid = ta.ukid
JOIN transport_route_pickup_point trpp
    ON ta.option_id = trpp.id
JOIN transport_route tr
    ON trpp.route_id = tr.id
JOIN transport_pickup_point tpp
    ON trpp.pickup_point_id = tpp.id
WHERE ha.status = 'confirmed'
  AND ta.status = 'CONFIRMED'
ORDER BY ukid ASC;  

-- answer 3.4
WITH student_selections AS (
    SELECT
        pa.ukid,
        po.name AS best_offer_org,
        pj.designation,
        pj.ctc,
        COUNT(*) OVER (PARTITION BY pa.ukid) AS selections,
        ROW_NUMBER() OVER (
            PARTITION BY pa.ukid
            ORDER BY pj.ctc DESC, pj.id ASC
        ) AS rn
    FROM placement_application pa
    JOIN placement_application_status pas
        ON pa.status_id = pas.id
    JOIN placement_job pj
        ON pa.job_id = pj.id
    JOIN placement_organization po
        ON pj.organization_id = po.id
    WHERE pas.name = 'Selected'
      AND pa.is_deleted = 0
)
SELECT
    ukid,
    selections,
    best_offer_org,
    designation,
    ctc
FROM student_selections
WHERE selections > 1
  AND rn = 1
ORDER BY ctc DESC;

-- answer 3.5

WITH venue_stats AS (
    SELECT
        it.type AS venue_type,
        iv.name AS venue,
        COUNT(DISTINCT ib.id) AS bookings,
        ROUND(SUM(TIMESTAMPDIFF(SECOND, ibi.start_datetime, ibi.end_datetime) / 3600.0), 2) AS booked_hours,
        DENSE_RANK() OVER (
            PARTITION BY it.type
            ORDER BY SUM(TIMESTAMPDIFF(SECOND, ibi.start_datetime, ibi.end_datetime)) DESC
        ) AS rank_in_type
    FROM infra_booking ib
    JOIN infra_booking_item ibi
        ON ib.id = ibi.booking_id
    JOIN infrastructure_type it
        ON ibi.infrastructure_type_id = it.id
    JOIN infrastructure_version iv
        ON ibi.infrastructure_id = iv.id
    WHERE ib.booking_module = 'VENUE_BOOKING'
      AND ibi.item_status = 'ALLOTTED'
      AND ib.deleted = 0
      AND ibi.deleted = 0
      AND ibi.start_datetime >= '2026-01-01 00:00:00'
      AND ibi.start_datetime < '2027-01-01 00:00:00'
    GROUP BY it.type, iv.id, iv.name
)
SELECT
    venue_type,
    venue,
    bookings,
    booked_hours,
    rank_in_type
FROM venue_stats
WHERE rank_in_type <= 3
ORDER BY venue_type ASC, rank_in_type ASC;