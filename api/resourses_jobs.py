from data.db_session import create_session
from data.jobs import Jobs

from api.parsers.parser_jobs import parser

from flask import jsonify
from flask_restful import abort, Resource


def abort_if_job_not_found(jobs_id):
    session = create_session()
    job = session.query(Jobs).get(jobs_id)
    if not job:
        abort(404, message=f"Job {jobs_id} not found")


class JobsResourse(Resource):
    def get(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        session = create_session()
        job = session.query(Jobs).get(jobs_id)
        return jsonify(
            {
                'jobs': [job.to_dict(only=['id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished', 'user.name', 'user.surname'])]
            }
        )

    def put(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        args = parser.parse_args()
        session = create_session()
        job = session.query(Jobs).get(jobs_id)
        job.job = args['job']
        job.team_leader = args['team_leader']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        job.is_finished = args['is_finished']
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        session = create_session()
        job = session.query(Jobs).get(jobs_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResourse(Resource):
    def get(self):
        session = create_session()
        jobs = session.query(Jobs).all()
        return jsonify(
            {
                'jobs': [job.to_dict(only=['id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished', 'user.name', 'user.surname'])
                         for job in jobs]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = create_session()
        print(args)
        job = Jobs(
            job=args['job'],
            team_leader=args['team_leader'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
