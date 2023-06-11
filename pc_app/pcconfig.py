import pynecone as pc

config = pc.Config(
    app_name="pc_app",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
