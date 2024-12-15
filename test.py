from modules.pipelines import PlanPipeline, CodePipeline
from omegaconf import OmegaConf


def test(game_name: str):
    plan_pipeline = PlanPipeline()
    plan_pipeline.step(f"我想做一个{game_name}游戏")

    code_pipeline = CodePipeline(plan_pipeline.plan)
    code_pipeline.init_step()

    html = code_pipeline.code["index.html"]
    css = code_pipeline.code["style.css"]
    js = code_pipeline.code["script.js"]

    # TODO: Metrics

    return html, css, js


if __name__ == "__main__":
    game_list = OmegaConf.load("config.yaml")["game_list"]
    print(game_list)

    for game in game_list:
        html, css, js = test(game)
        print(html)
        print(css)
        print(js)