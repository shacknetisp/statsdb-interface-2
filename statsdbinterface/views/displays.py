import config
from flask import Blueprint, render_template, send_from_directory, request

from ..database import models, extmodels
from . import templateutils

# displays blueprint
bp = Blueprint(__name__, __name__)


@bp.route('/static/<path:path>')
def static(path):
    return send_from_directory('static', path)


@bp.route("/")
def display_dashboard():
    games = models.Game.query.order_by(models.Game.id.desc()).limit(
        config.DISPLAY_RESULTS_RECENT).all()
    return render_template('displays/dashboard.html', games=games)


@bp.route("/games")
def display_games():
    pager = models.Game.query.order_by(models.Game.id.desc()).paginate(
            request.args.get("page", default=1, type=int),
            config.DISPLAY_RESULTS_PER_PAGE)

    return render_template('displays/games.html', pager=pager,
                           Game=models.Game)


@bp.route("/game/<int:gameid>")
@bp.route("/games/<int:gameid>")
def display_game(gameid):
    game = models.Game.query.filter_by(id=gameid).first_or_404()
    return render_template('displays/game.html', game=game)


@bp.route("/servers")
def display_servers():
    pager = extmodels.Server.paginate(
        request.args.get("page", default=1, type=int),
        config.DISPLAY_RESULTS_PER_PAGE)

    ret = render_template('displays/servers.html', pager=pager)
    return ret


@bp.route("/server/<string:handle>")
@bp.route("/servers/<string:handle>")
def display_server(handle):
    server = extmodels.Server.get_or_404(handle)
    return render_template('displays/server.html', server=server)


@bp.route("/server:games/<string:handle>")
def display_server_games(handle):
    server = extmodels.Server.get_or_404(handle)
    pager = models.Game.query.filter(
            models.Game.id.in_(server.game_ids)).order_by(
            models.Game.id.desc()).paginate(
            request.args.get("page", default=1, type=int),
            config.DISPLAY_RESULTS_PER_PAGE)
    return render_template('displays/server_games.html', server=server,
                           pager=pager)


@bp.route("/players")
def display_players():
    pager = extmodels.Player.paginate(
        request.args.get("page", default=1, type=int),
        config.DISPLAY_RESULTS_PER_PAGE)

    ret = render_template('displays/players.html', pager=pager)
    return ret


@bp.route("/player/<string:handle>")
@bp.route("/players/<string:handle>")
def display_player(handle):
    player = extmodels.Player.get_or_404(handle)
    return render_template('displays/player.html', player=player)


@bp.route("/player:games/<string:handle>")
def display_player_games(handle):
    player = extmodels.Player.get_or_404(handle)
    pager = models.Game.query.filter(
            models.Game.id.in_(player.game_ids)).order_by(
            models.Game.id.desc()).paginate(
            request.args.get("page", default=1, type=int),
            config.DISPLAY_RESULTS_PER_PAGE)
    return render_template('displays/player_games.html', player=player,
                           pager=pager)


@bp.route("/maps")
def display_maps():
    pager = extmodels.Map.paginate(
        request.args.get("page", default=1, type=int),
        config.DISPLAY_RESULTS_PER_PAGE)

    ret = render_template('displays/maps.html', pager=pager)
    return ret


@bp.route("/map/<string:name>")
@bp.route("/maps/<string:name>")
def display_map(name):
    map = extmodels.Map.get_or_404(name)
    return render_template('displays/map.html', map=map)


@bp.route("/map:games/<string:name>")
def display_map_games(name):
    map = extmodels.Map.get_or_404(name)
    pager = models.Game.query.filter(
            models.Game.id.in_(map.game_ids)).order_by(
            models.Game.id.desc()).paginate(
            request.args.get("page", default=1, type=int),
            config.DISPLAY_RESULTS_PER_PAGE)
    return render_template('displays/map_games.html', map=map,
                           pager=pager)


@bp.route("/modes")
def display_modes():
    ret = render_template('displays/modes.html',
                          modes=sorted(extmodels.Mode.all(),
                                       key=lambda m: len(m.game_ids),
                                       reverse=True))
    return ret


@bp.route("/mode/<string:name>")
@bp.route("/modes/<string:name>")
def display_mode(name):
    mode = extmodels.Mode.get_or_404(name)
    return render_template('displays/mode.html', mode=mode)


@bp.route("/mode:games/<string:name>")
def display_mode_games(name):
    mode = extmodels.Mode.get_or_404(name)
    pager = models.Game.query.filter(
            models.Game.id.in_(mode.game_ids)).order_by(
            models.Game.id.desc()).paginate(
            request.args.get("page", default=1, type=int),
            config.DISPLAY_RESULTS_PER_PAGE)
    return render_template('displays/mode_games.html', mode=mode,
                           pager=pager)

templateutils.setup(bp)
