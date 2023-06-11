import pynecone as pc

class PcwebscrapConfig(pc.Config):
    pass

config = PcwebscrapConfig(
    app_name="pc_web_scrap",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)