from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('team_leader', type=int, required=True)
parser.add_argument('job', required=True)
parser.add_argument('work_size', type=int, required=True)
parser.add_argument('collaborators', required=False)
parser.add_argument('is_finished', type=bool, required=False)
