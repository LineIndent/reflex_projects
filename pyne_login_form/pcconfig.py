import pynecone as pc


config = pc.Config(
    app_name="pyne_login_form",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
