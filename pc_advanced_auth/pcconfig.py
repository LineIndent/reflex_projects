import pynecone as pc

config = pc.Config(
    app_name="pc_advanced_auth",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
