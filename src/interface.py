import tempfile

import gradio as gr
import pandas as pd
import plotly.graph_objects as go

from src.database import get_sync_session
from src.model import Model
from src.repository.model_prediction import PredictionRepo
from src.repository.point import PointRepo
from src.settings import Settings


def filter_map() -> go.Figure:
    session = get_sync_session()
    points = PointRepo.get_points(session)
    latitude = [point.latitude for point in points]
    longitude = [point.longitude for point in points]
    m_latitude = sum(latitude) / len(latitude)
    m_longitude = sum(longitude) / len(longitude)

    points_str = []
    for point in points:
        animals = PredictionRepo.load_animals_at_point(point.id)
        point_str = f"<b>Name</b>: {point.name}<br><b>Animals</b>:<br>"
        for animal_name, count in animals:
            point_str += f"{animal_name}: {count}<br>"
        points_str.append(point_str)

    fig = go.Figure(
        go.Scattermapbox(
            customdata=points_str,
            lat=latitude,
            lon=longitude,
            mode="markers",
            marker=go.scattermapbox.Marker(size=6),
            hoverinfo="text",
            hovertemplate="%{customdata}",
        )
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        hovermode="closest",
        mapbox=dict(
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=m_latitude,
                lon=m_longitude,
            ),
            pitch=0,
            zoom=9,
        ),
    )

    return fig


settings = Settings()
model = Model(settings.model_path)


def process_image(images: list[tempfile._TemporaryFileWrapper], point: int, progress=gr.Progress()) -> pd.DataFrame:
    output_results = []
    for image in progress.tqdm(images):
        results = model.predict(image.name)
        PredictionRepo.create_model_prediction(results, point)
        for result in results:
            for box in result.boxes:
                prob = box.conf.tolist()[0]
                cls = box.cls.tolist()[0]
                class_name = result.names[cls]
                output_results.append(
                    {
                        "image": image.name.split("/")[-1],
                        "probability": prob,
                        "class": class_name,
                    }
                )
    return pd.DataFrame(output_results)


def dropdown_changed(point: int) -> pd.DataFrame:
    results = pd.DataFrame(PredictionRepo.load_predictions_at_point(point))
    results["filename"] = results["filename"].str.split("/").str[-1]
    return results


def create_interface() -> gr.Blocks:
    points = PointRepo.get_points()
    points_dropdown = [(point.name, point.id) for point in points]
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                files = gr.Files(label="Upload photo")
                point = gr.Dropdown(choices=points_dropdown)
            pred_table = gr.DataFrame(label="Loaded images")
        with gr.Row():
            submit = gr.Button(value="Submit photo", variant="primary")
            clear = gr.ClearButton(value="Clear photo", components=[files, pred_table])  # noqa: F841
        with gr.Row():
            map = gr.Plot()
            animals_at_point = gr.DataFrame(label="Animals at point")
        demo.load(filter_map, [], map)
        submit.click(process_image, [files, point], pred_table, show_progress=not settings.is_docker)
        point.select(dropdown_changed, [point], animals_at_point)
    return demo
