import pynecone as pc

config = pc.Config(
    app_name="pc_animated_login",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
