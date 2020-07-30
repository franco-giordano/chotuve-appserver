
from resources.videos_routes import VideoRoute, UniqueVideoRoute
from resources.comments_routes import CommentRoute
from resources.reactions_route import ReactionRoute
from resources.user_routes import UniqueUserRoute, UniqueUserVidsRoute, UsersRoute, UsersAdmin

from resources.friends_routes import FriendsRoute, RequestsRoute, UniqueRequestRoute, UniqueFriendsRoute

from resources.extra_routes import PingRoute, AuthRoutes, PushTokensRoutes, ResetCodesRoute, ChangePwRoute

from resources.msg_routes import MessagesRoute

from resources.stats_routes import StatsRoutes

def register_routes(api):
    api.add_resource(VideoRoute, '/videos')
    api.add_resource(UniqueVideoRoute, '/videos/<int:vid_id>')
    api.add_resource(CommentRoute, '/videos/<int:vid_id>/comments')
    api.add_resource(ReactionRoute, '/videos/<int:vid_id>/reactions')

    api.add_resource(UniqueUserRoute, '/users/<int:user_id>')
    api.add_resource(UniqueUserVidsRoute, '/users/<int:user_id>/videos')
    api.add_resource(UsersRoute, '/users')
    api.add_resource(AuthRoutes, '/users/auth')
    api.add_resource(UsersAdmin, '/users/admin')
    api.add_resource(ResetCodesRoute, '/users/reset-codes')
    api.add_resource(ChangePwRoute, '/users/change-password')

    api.add_resource(FriendsRoute, '/users/<int:user_id>/friends')
    api.add_resource(UniqueFriendsRoute, '/users/<int:user_id>/friends/<int:friend_id>')

    api.add_resource(RequestsRoute, '/friend-requests')
    api.add_resource(UniqueRequestRoute, '/friend-requests/<int:sender_id>')

    api.add_resource(MessagesRoute, '/messages/<int:other_user_id>')

    api.add_resource(PushTokensRoutes, '/tokens')

    api.add_resource(PingRoute, '/ping')

    api.add_resource(StatsRoutes, '/stats')