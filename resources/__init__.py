
from resources.videos_routes import VideoRoute, UniqueVideoRoute
from resources.comments_routes import CommentRoute
from resources.reactions_route import ReactionRoute
from resources.user_routes import UniqueUserRoute, UniqueUserVidsRoute, UsersRoute, UsersAdmin

from resources.friends_routes import FriendsRoute, RequestsRoute, UniqueRequestRoute

from resources.extra_routes import PingRoute, AuthRoutes, PushTokensRoutes, ResetCodesRoute

from resources.msg_routes import MessagesRoute

def register_routes(api):
    api.add_resource(VideoRoute, '/videos')
    api.add_resource(UniqueVideoRoute, '/videos/<int:vid_id>')
    api.add_resource(CommentRoute, '/videos/<int:vid_id>/comments')
    api.add_resource(ReactionRoute, '/videos/<int:vid_id>/reactions')

    api.add_resource(UniqueUserRoute, '/users/<int:user_id>')
    api.add_resource(UniqueUserVidsRoute, '/users/<int:user_id>/videos')
    api.add_resource(UsersRoute, '/users')
    api.add_resource(UsersAdmin, '/users/admin')

    api.add_resource(FriendsRoute, '/users/<int:user_id>/friends')
    api.add_resource(RequestsRoute, '/users/<int:user_id>/friends/requests')

    api.add_resource(UniqueRequestRoute, '/users/<int:my_id>/friends/requests/<int:sender_id>')

    api.add_resource(MessagesRoute, '/messages/<int:other_user_id>')

    api.add_resource(PushTokensRoutes, '/tokens')

    api.add_resource(PingRoute, '/ping')
    api.add_resource(AuthRoutes, '/auth')
    api.add_resource(ResetCodesRoute, '/reset-codes')