WITH gpa_calc AS (
    SELECT
        st.id,
        CASE
            WHEN st.grade_level < 9    THEN
                (
                    SELECT
                        round(SUM(sg.gpa_points) / COUNT(sg.course_number), 2)
                    FROM
                        storedgrades sg
                    WHERE
                            sg.studentid = st.id
                        AND sg.grade_level IN (
                            6,
                            7,
                            8
                        )
                )
            WHEN st.grade_level > 8    THEN
                (
                    SELECT
                        round(SUM(sg.gpa_points) / COUNT(sg.course_number), 2)
                    FROM
                        storedgrades sg
                    WHERE
                            sg.studentid = st.id
                        AND sg.grade_level > 8
                        AND sg.excludefromgpa <> 1
                )
        END AS gpa
    FROM
        students st
    WHERE
        st.enroll_status = 0
)
SELECT
    to_char(s.student_number)                                                                                                                                               AS student_number,
    s.lastfirst,
    s.grade_level,
    (
        SELECT
            x.elastatus
        FROM
            s_ca_stu_x x
        WHERE
            x.studentsdcid = s.dcid
    ) AS "ELA Status",
    (
        SELECT
            CASE
                WHEN x.primarydisability IS NOT NULL THEN
                    'Y'
                ELSE
                    'N'
            END AS "SPECIAL_ED_STUDENT"
        FROM
            s_ca_stu_x x
        WHERE
            x.studentsdcid = s.dcid
    ) AS "SPED Status",
    (
        SELECT
            abbreviation
        FROM
            schools sch
        WHERE
            sch.school_number = s.schoolid
    )                                                                                             AS "SCHOOL",
    (
        SELECT
            CASE
                WHEN ethnicity_name IS NULL THEN
                    'Not Reported'
                ELSE
                    ethnicity_name
            END
        FROM
            pssis_adaadm_meeting_ptod ps
        WHERE
                ps.studentid = s.id
            AND ROWNUM = 1
    )        AS ethnicity_name,
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
    CASE
        WHEN to_char(gpa_calc.gpa) IS NULL THEN
            to_char('NA')
        ELSE
            to_char(gpa_calc.gpa)
    END AS gpa,
    pgfg.grade,
	t.last_name
    || ', '
    || substr(t.first_name, 1, 1)
    || '.' AS teachername,
    c.course_name,
    c.course_number,
        (
        SELECT
            regexp_replace(abbreviation, 'P', '')
        FROM
            period
        WHERE
                period_number = regexp_replace(sec.expression, '(-.*)?\(.*', '')
            AND schoolid = sec.schoolid
            AND year_id = substr(sec.termid, 1, 2)
    ) AS period,
    pgfg.citizenship,
    ps_customfields.getstudentscf(s.id, 'AUSD_Counselor')                                                                                                                   AS counselor,
    CASE
        WHEN sec.gradebooktype = 1 THEN
            (
                SELECT
                    actualgradeentered
                FROM
                    psm_reportcarditemgrade  rcig,
                    psm_sectionenrollment    se
                WHERE
                        rcig.sectionenrollmentid = se.id
                    AND se.sectionid = (
                        SELECT
                            psm_section.id
                        FROM
                            psm_section,
                            psm_term
                        WHERE
                                psm_section.schoolid = (
                                SELECT
                                    id
                                FROM
                                    psm_school
                                WHERE
                                    schoolnumber = sec.schoolid
                            )
                            AND psm_section.sectionidentifier = sec.section_number
                            AND psm_term.id = psm_section.termid
                            AND psm_term.schoolyear = '2021'
                            AND psm_section.schoolcourseid = (
                                SELECT
                                    id
                                FROM
                                    psm_schoolcourse
                                WHERE
                                        coursecode = sec.course_number
                                    AND schoolid = psm_section.schoolid
                            )
                            AND psm_term.termcode = (
                                SELECT
                                    abbreviation
                                FROM
                                    terms
                                WHERE
                                        id = sec.termid
                                    AND schoolid = sec.schoolid
                            )
                    )
                    AND rcig.reportcarditemid IN (
                        SELECT
                            id
                        FROM
                            psm_reportcarditem
                        WHERE
                                name = 'Work Habits'
                            AND reportingtermid IN (
                                SELECT
                                    id
                                FROM
                                    psm_reportingterm
                                WHERE
                                    name in ('Q4','S2')
                            )
                    )
                    AND se.studentid = (
                        SELECT
                            id
                        FROM
                            psm_student
                        WHERE
                            studentidentifier = s.student_number
                    )
            )
        ELSE
            (
                SELECT
                    standardgrade
                FROM
                    standardgradesection sgs
                WHERE
                        s.dcid = sgs.studentsdcid
                    AND yearid = 30
                    AND sgs.sectionsdcid = sec.dcid
                    AND sgs.storecode in ('Q4','S2')
                    AND ROWNUM <= 1
            )
    END AS workhabits,
    cc.currentabsences,
    cc.currenttardies,
    pgfg.comment_value,
    c.sched_department
FROM
    students       s,
    schools        sch,
    pgfinalgrades  pgfg,
    sections       sec,
    courses        c,
    teachers       t,
    cc,
    gpa_calc
WHERE
    ( ps_customfields.getstudentscf(s.id, 'AUSD_InstrSet') <> 'C'
      OR ps_customfields.getstudentscf(s.id, 'AUSD_InstrSet') IS NULL )
    AND sch.school_number = s.schoolid
    AND s.id = pgfg.studentid
    AND pgfg.finalgradename in ('Q4','S2')
    AND s.id = gpa_calc.id
    AND sec.id = pgfg.sectionid
    AND c.course_number = sec.course_number
    AND t.id = sec.teacher
    AND abs(cc.sectionid) = pgfg.sectionid
    AND cc.studentid = pgfg.studentid
    AND cc.termid LIKE 30 || '%%'
    AND pgfg.grade <> '--'
    AND pgfg.grade IS NOT NULL
ORDER BY
    grade_level,
    student_number,
    pgfg.grade