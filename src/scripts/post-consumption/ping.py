from paperless.postconsumption import PostConsumptionScript


class Script(PostConsumptionScript):
    def run(self):
        self.logger.info(f"Running f{self.name} post-consumption script")
        self.logger.info("pong")


if __name__ == "__main__":
    Script("ping").run()
