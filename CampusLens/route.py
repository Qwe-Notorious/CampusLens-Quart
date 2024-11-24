from random import randint
import logging
import os
from quart import Quart, render_template, redirect, url_for, ResponseReturnValue, session
from quart_wtf.csrf import CSRFProtect
from quart_auth import (
    AuthUser, current_user, login_required, login_user, logout_user, QuartAuth, Unauthorized
)
from quart_bcrypt import Bcrypt
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from CampusLens.models import Base, Media, User
from CampusLens.form import UploadFile, UserRegistration, LoginAuto
from CampusLens.config import Config


app = Quart(__name__, static_folder='static')
csfr = CSRFProtect(app)
login = QuartAuth(app)
login.init_app(app)
bcrypt = Bcrypt(app)
bcrypt.init_app(app)
app.config['UPLOAD_FOLDER'] = 'CampusLens/static/media/'
app.config['MAX_CONTENT_LENGTH'] = 20 * 3648 * 5472  # Установить лимит на 20 МБ
app.config.from_object(Config)
DATABASE_URL = "sqlite+aiosqlite:///media.db"  # Замените на ваши данные
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



@app.before_serving
async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def random_photo_login():
    photo_array = ("media/images/DJV-MAR-1011-08.jpg", "media/images/DJV-MAR-1011-04.jpg",
                   "media/images/6868ee58-ee96-4045-b066-75500abbd154.jpg",
                   "media/images/4024adb0-20f3-4ba0-a999-a819a326fe4b.jpg")

    random_result = randint(0, 3)
    result_tuple = photo_array[random_result]

    return result_tuple


@app.route("/")
async def index():
    async with SessionLocal() as session1:
        # Получаем все записи Media, отсортированные по timestamp
        media_requests = await session1.execute(select(Media).order_by(Media.timestamp.desc()))
        medias = media_requests.scalars().all()

        # Обновляем пути к файлам в одной строке
        for media in medias:
            media.filepath = media.filepath.replace("CampusLens/static/", "")

        await session1.commit()

    if await current_user.is_authenticated:
        username = session.get('user_id')

        if username:
            async with SessionLocal() as session2:
                user_requsts = await session2.execute(select(User).where(User.username == username))
                users = user_requsts.scalars().all()
                user_img = random_photo_login()
            return await render_template("index.html", medias=medias, users=users, imgUser=user_img)

    return await render_template("index.html", medias=medias)


@app.route("/form_media")
@login_required
async def form_media():
    form = await UploadFile().create_form()

    if await current_user.is_authenticated:
        username = session.get('user_id')

        if username:
            async with SessionLocal() as session2:
                user_requsts = await session2.execute(select(User).where(User.username == username))
                users = user_requsts.scalars().all()
                user_img = random_photo_login()
            return await render_template("formmedia.html", form=form, users=users, imgUser=user_img)

    return await render_template("formmedia.html", form=form)


@app.route("/media_handler", methods=['GET', 'POST'])
async def media_handler():
    form = await UploadFile().create_form()

    if await form.validate_on_submit():
        file = form.file.data
        title_card = form.titleCard.data

        if file.filename == '':
            print("Да блять")
            return 'No selected file'

        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        await file.save(filepath)

        async with SessionLocal() as session1:
            new_media = Media(filename=filename, filepath=filepath, namePicture=title_card)
            session1.add(new_media)
            await session1.commit()

        return redirect(url_for('index'))

    return redirect(url_for('form_media'))


@app.route('/authent_ication', methods=["POST", "GET"])
async def authent_ication():
    form = await UserRegistration().create_form()

    if await form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        async with SessionLocal() as session1:
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            session1.add(user)
            await session1.commit()
            return redirect(url_for('form_media'))

    return await render_template('authentication.html', form=form)


@app.route('/login', methods=["POST", "GET"])
async def login():
    form = await LoginAuto().create_form()

    if await form.validate_on_submit():
        email = form.email.data.strip()  # Убираем лишние пробелы
        password = form.password.data

        try:
            async with SessionLocal() as session1:
                user_requests = await session1.execute(select(User).where(User.email == email))
                user = user_requests.scalars().first()

            if user.email == "Admin@list.ru" and bcrypt.check_password_hash(user.password,
                                                                            password) == "4509812367Admin}":
                login_user(AuthUser(user))
                return redirect(url_for('admin'))

            if user is not None and bcrypt.check_password_hash(user.password, password):
                login_user(AuthUser("user"))
                logging.exception("Ошибка при входе: {}".format(user))
                session["user_id"] = user.username
                print(session)
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))  # Добавлено: ведем пользователя назад к форме
        except Exception as e:
            logging.exception("Ошибка при входе: {}".format(e))
            return redirect(url_for('login'))  # Добавлено: возвращаемся к форме в случае ошибки
    return await render_template('login.html', form=form)


@app.errorhandler(Unauthorized)
async def redirect_to_login(*_: Exception) -> ResponseReturnValue:
    return redirect(url_for("login"))

