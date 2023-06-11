import pynecone as pc

config = pc.Config(
    app_name="pc_card",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
