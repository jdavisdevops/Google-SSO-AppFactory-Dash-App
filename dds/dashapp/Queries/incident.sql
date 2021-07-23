   with student_inc as (
SELECT
   to_char(TRUNC(TO_DATE(cai.incident_ts, 'DD/MM/YY'))) as incident_date,
      CASE
        WHEN cai.incident_ts BETWEEN '01-JUL-17' AND '30-JUN-18'    THEN
            '17-18'
        WHEN cai.incident_ts BETWEEN '01-JUL-18' AND '30-JUN-19'    THEN
            '18-19'
        WHEN cai.incident_ts BETWEEN '14-AUG-19' AND '09-JUN-20'    THEN
            '19-20'
        WHEN cai.incident_ts BETWEEN '13-AUG-20' AND '03-JUN-21'    THEN
            '20-21'
    END          AS "School_Year",
   to_char(ip.incident_id) as incident_id,
   pb.incident_category as "Behavior",
   pba.incident_category as "Action",
   ip.role_code,
   to_char(ip.Grade_level) as incident_grade_level,
   --decode(cai.school_number,'1','AHS','51','BS','53','CG','54','HO','55','HA','56','HR','57','LW','61','DA','62','FA','63','FH','79','RLC')  as "Incident School",
   cai.school_name as "Incident School",
   pdur.duration_actual || ' ' || pdur.incident_category as "Duration",
   ip.participant_number
FROM psrw_incidentparticipant ip
   INNER JOIN psrw_participantbehavior pb
   ON pb.incident_person_role_id = ip.id
   FULL JOIN psrw_participantbehavioraction pba
   ON pba.id = pb.id
   LEFT JOIN psrw_participantbehactdur pdur
   ON pdur.id = pba.incident_action_id
   LEFT JOIN ca_incident cai
   ON cai.incident_id = ip.incident_id
WHERE
   ip.participant_type = 'Students'
   and ip.role_code = 'Offender'
   and cai.incident_ts >= '01-JUL-17'
order by cai.incident_ts desc)
SELECT
   s.first_name||' '||s.last_name as studentName,
   to_char(s.student_number) as student_number,
   S.gender,
   to_char(s.dob) as "DOB",
   x.elastatus,
   CASE WHEN x.primarydisability >= '200' THEN 'Y' ELSE 'N' END AS SPECIAL_ED_STUDENT,
   (SELECT case when ethnicity_name is null then 'Not Reported' else ethnicity_name end FROM pssis_adaadm_meeting_ptod PS WHERE PS.STUDENTID = S.ID AND ROWNUM = 1) AS ethnicity_name,
   si.*
from s_ca_stu_x x, students s
   LEFT JOIN STUDENT_INC SI
   ON S.STUDENT_NUMBER = si.participant_number
where s.dcid = x.studentsdcid 
   and si.incident_id is not null