import json
import asyncio
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiojobs.aiohttp import setup
import jinja2
import aiohttp_jinja2

from config import Config
from database import db, Database


def get_db(config: Config):
    # _db = db(config)
    # print('DB Initialized')
    # return _db
    return None


def template(name: str, **kwargs):
    return aiohttp_jinja2.template(f'{name}.html.jinja2', **kwargs)


def get_router(config: Config, db: Database):
    router = web.RouteTableDef()

    
    @router.get('/check-user')
    async def check_user(request: Request):
        # chat_id = request.query.get('chat_id', None)
        # if chat_id is None or not chat_id.isdigit():
        #     raise web.HTTPBadRequest(f'Bad chat_id parameter passed: {chat_id}')
        # user = db.get_user(chat_id)
        # print(user)
        return web.json_response({'status': 'ok'})
    
    @router.post('/save-user')
    async def save_user(request: Request):
        return web.json_response({'status': 'ok'})
    
    @router.post('/init-session')
    async def init_session(request: Request):
        return web.json_response({'status': 'ok'})
    
    @router.get('/')
    async def index(request: Request):
        return web.json_response({'status': 'ok'})
    
    @router.get('/boobs')
    @template('base')
    async def boobs(request: Request):
        return {'page_name': 'boobs'}
    
    @router.get('/leaderboard')
    @template('base')
    async def leaderboard(request: Request):
        return {'page_name': 'leaderboard'}
    
    @router.get('/boost')
    @template('base')
    async def boost(request: Request):
        return {'page_name': 'boost'}
    
    return router
    
    
def get_app(config: Config):
    app = web.Application(middlewares=[
        session_middleware(EncryptedCookieStorage(b'x' * 32))
    ])
    setup(app)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    app.add_routes(get_router(config, get_db(config)))
    return app


async def start(runner: web.AppRunner):
    print('Starting app...')
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    print(f'Started app on http://0.0.0.0:8080...')
    await site.start()


if __name__ == '__main__':
    config = Config()
    app = get_app(config)
    runner = web.AppRunner(app)
    loop = asyncio.new_event_loop()
    try:
        loop.create_task(start(runner))
        loop.run_forever()
    except KeyboardInterrupt:
        print('App closed manually')
    except Exception as e:
        print(e)
    finally:
        loop.run_until_complete(runner.cleanup())
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
