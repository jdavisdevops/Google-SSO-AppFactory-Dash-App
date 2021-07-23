SELECT
    s.student_number,
    ps.name                                                                                                                                                                                                                                                                               AS "LASTFIRST",
    ps.current_grade_level,
    ps.gender,
    (
        SELECT
            x.elastatus
        FROM
            s_ca_stu_x x
        WHERE
            x.studentsdcid = s.dcid
    ) AS "ELA Status",
    ps.special_ed_student,
    CASE
        WHEN s.enroll_status = 0 THEN
            'enrolled'
        ELSE
            'not enrolled'
    END AS "Enroll Status",
    (
        SELECT
            decode(u.ausd_permit_code, '1', '(1) Overflow from BS', '2', '(2) Overflow from CG',
                   '3', '(3) Overflow from HO', '4', '(4) Overflow from HA', '5',
                   '(5) Overflow from HR', '6', '(6) Overflow from LW', '7', '(7) Overflow from DA',
                   '8', '(8) Overflow from FA', 'PTR', 'Permission To Remain', 'PTR1',
                   'One Year PTR', 'INT1', 'One Year Inter District Permit', 'RTA', 'Remain Through Appeal',
                   'TPTR', 'Temoprary PTR', '9', '(9) Overflow from FH', 'A',
                   '(A) Inter District from Duarte', 'B', '(B) Inter District from El Monte', 'C', '(C) Inter District from Monrovia',
                   'D', '(D) Inter District from Pasadena', 'E', '(E) Inter District from San Gabriel', 'F',
                   '(F) Inter District from Temple City', 'TE', '(TE) Temporary Inter District', 'G', '(G) Intra from BS',
                   'H', '(H) Intra from CG', 'I', '(I) Intra from HO', 'J',
                   '(J) Intra from HA', 'K', '(K) Intra from HR', 'L', '(L) Intra from LW',
                   'M', '(M) Intra from DA', 'N', '(N) Intra from FA', 'O',
                   '(O) Intra from FH', 'P', '(P) Other Intra Dist', 'TA', '(TA) Temporary Intra District',
                   'Q', '(Q) Grandfathered from BS', 'R', '(R) Grandfathered from CG', 'S',
                   '(S) Grandfathered from HO', 'T', '(T) Grandfathered from HA', 'U', '(U) Grandfathered from HR',
                   'V', '(V) Grandfathered from LW', 'W', '(W) Grandfathered from DA', 'X',
                   '(X) Grandfathered from FA', 'Y', '(Y) Grandfathered from FH', 'Z', '(Z) Other Inter District Permits')
        FROM
            u_studentsuserfields u
        WHERE
            s.dcid = u.studentsdcid
    ) AS "Permit Code",
    ps.attendance_school_abbreviation as SCHOOL,
    case when ps.ethnicity_name is null then 'Not Reported' else ps.ethnicity_name end as ETHNICITY_NAME,
    ac.att_code,
    a.att_date,
    ac.description,
    ac.presence_status_cd,
    a.att_comment,
    CASE
        WHEN a.att_date BETWEEN '01-JUL-17' AND '30-JUN-18'    THEN
            '17-18'
        WHEN a.att_date BETWEEN '01-JUL-18' AND '30-JUN-19'    THEN
            '18-19'
        WHEN a.att_date BETWEEN '14-AUG-19' AND '03-JUN-20'    THEN
            '19-20'
        WHEN a.att_date BETWEEN '13-AUG-20' AND '03-JUN-21'    THEN
            '20-21'
    END          AS "School_Year"
FROM
    attendance                 a,
    attendance_code            ac,
    pssis_adaadm_meeting_ptod  ps,
    students                   s
WHERE
        a.attendance_codeid = ac.id
    AND ps.studentid = a.studentid
    AND ps.studentid = s.id
    AND a.studentid = s.id
    AND a.att_date = ps.calendardate
    AND a.att_date >= '01-JUL-17'
    and att_code is not null
ORDER BY
    ps.attendance_school_abbreviation, a.att_date, ps.current_grade_level, s.student_number