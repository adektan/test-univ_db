import pandas as pd
import psycopg2
import sqlalchemy
from pytz import timezone
from datetime import datetime


db_engine = sqlalchemy.create_engine('postgresql://postgres:password@host.docker.internal:5433/univ_db')

schema_raw = 'raw_layer'
schema_dataset = 'dataset'
schema_analytics = 'analytics'

query_course_attendance = """
select 
"ID"::int as id,
"STUDENT_ID"::int as student_id,
"SCHEDULE_ID"::int as schedule_id,
to_date("ATTEND_DT", 'dd-mon-yy') as attend_date
from {0}.course_attendance where insert_time = (select max(insert_time) from {0}.course_attendance)
""".format(schema_raw)

query_course = """
select 
"ID"::int as id,
trim("NAME"::varchar(150)) as course_name
from {0}.course  where insert_time = (select max(insert_time) from {0}.course)
""".format(schema_raw)

query_enrollment = """
select 
"ID"::int as id,
"STUDENT_ID"::int as student_id,
"SCHEDULE_ID"::int as schedule_id,
trim("ACADEMIC_YEAR"::varchar(20)) as academic_year,
"SEMESTER"::int as semester,
to_date("ENROLL_DT", 'dd-mon-yy') as enroll_date
from {0}.enrollment where insert_time = (select max(insert_time) from {0}.enrollment)
""".format(schema_raw)

query_schedule = """
select 
"ID"::int as id,
"COURSE_ID"::int as course_id,
"LECTURER_ID"::int as lecturer_id,
to_date("START_DT", 'dd-mon-yy') as start_date,
to_date("END_DT", 'dd-mon-yy') as end_date,
trim("COURSE_DAYS"::varchar(50)) as course_days
from {0}.schedule where insert_time = (select max(insert_time) from {0}.schedule)
""".format(schema_raw)

sources = {
    "course_attendance": {"url": "https://drive.google.com/file/d/1AnW-wClSUs5U8mIaewj-JV87iatObQZr/view?usp=sharing", "query_to_dataset": query_course_attendance},
    "course": {"url": "https://drive.google.com/file/d/1-oVKXggNIbEX9YDL_nFbRsR8FDn_G9o3/view?usp=sharing", "query_to_dataset": query_course},
    "enrollment": {"url": "https://drive.google.com/file/d/1uUEm3gSToAy9IACqOMYLy-Sno07xrQQ6/view?usp=sharing", "query_to_dataset": query_enrollment},
    "schedule": {"url": "https://drive.google.com/file/d/1I2UWWjcOaOnA6kE0LdQ4bp6WBhdzwByf/view?usp=sharing", "query_to_dataset": query_schedule}
}
####################


# for query to layer analytics in below

query_dim_course = """
with course as (
    select id as schedule_id, course_id, course_name, start_date, end_date, course_days, count(1) as course_day_per_weeks from (
    select 
        s.*, c.course_name , 
        regexp_split_to_table(s.course_days, ',') as days
    from {0}.schedule s 
    left join {0}.course c on s.course_id = c.id
    ) a
    group by 1,2,3,4,5,6
)
select c.*, e.academic_year, e.semester, e.user_enroll, current_timestamp as insert_time from course c  
left join (select schedule_id , academic_year, semester, count(distinct student_id) as user_enroll from {0}.enrollment group by 1,2,3) e
on c.schedule_id = e.schedule_id
""".format(schema_dataset)

query_dim_course_weeks = """
with weeks_check as (
	select 
	distinct 
	(to_char(attend_date, 'yyyymm') || '-' || extract(week from attend_date)::varchar(10)) as month_weeks, 
	to_char(attend_date, 'yyyymm')  as months,
	extract(week from attend_date) as weeks
	from {0}.course_attendance order by 1
)
	, weeks_check2 as (
	select 
	month_weeks ,
    months,
	weeks,
	case when rn = 2 then prev_week else month_weeks end month_weeks2 
	from (
		select *, row_number() over(partition by weeks order by month_weeks desc) as rn from (
			select *, lead(month_weeks) over() as prev_week from weeks_check order by 1
		) a
	) b order by 1
)
select  month_weeks, dense_rank () over(order by month_weeks2) as week_id , months, weeks, current_timestamp as insert_time from weeks_check2 order by month_weeks

""".format(schema_dataset)

query_fact = """
select 
dcw.week_id,
dcw.month_weeks,
dc.academic_year,
dc.semester, 
ca.student_id,
ca.schedule_id,
ca.attend_date,
dc.course_name,
dc.user_enroll
from {0}.course_attendance ca
left join {1}.dim_course_weeks dcw on dcw.month_weeks = (to_char(attend_date, 'yyyymm') || '-' || extract(week from attend_date)::varchar(10))
left join {1}.dim_course dc on dc.schedule_id = ca.schedule_id 
order by 1
""".format(schema_dataset, schema_analytics)

query_datamart = """
with total as (
	select 
	fa.semester as semester_id,
	week_id,
	dc.course_name,
	dc.course_day_per_weeks,
	dc.user_enroll,
	sum(case when fa.attend_date between dc.start_date and dc.end_date then 1 else 0 end) as total_attend_per_week
	from {0}.fact_attandence fa 
	left join {0}.dim_course dc on dc.schedule_id = fa.schedule_id 
	group by 1,2,3,4,5
)
select 
semester_id,
week_id,
course_name,
((total_attend_per_week)::numeric / (user_enroll * course_day_per_weeks)::numeric) as attendance_pct
from total
""".format(schema_analytics)

analytics_source = {
    "dim_course": query_dim_course,
    "dim_course_weeks": query_dim_course_weeks,
    "fact_attandence": query_fact,
    "datamart_agg_attandence": query_datamart
}