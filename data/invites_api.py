import flask

from . import db_session
from .invite_codes import InviteCode

blueprint = flask.Blueprint(
    'invites__api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/invite_codes')
def get_codes():
    return "Обработчик в news_api"