import gradio as gr
import numpy as np
import numpy.typing as npt
import plotly.graph_objects as go

from src.model import Model
from src.repository.model_prediction import PredictionRepo
from src.repository.point import PointRepo


def filter_map() -> go.Figure:
    points = PointRepo.get_points()
    name = [point.name for point in points]
    latitude = [point.latitude for point in points]
    longitude = [point.longitude for point in points]
    m_latitude = sum(latitude) / len(latitude)
    m_longitude = sum(longitude) / len(longitude)
    fig = go.Figure(
        go.Scattermapbox(
            customdata=name,
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


model = Model()


def process_image(image: npt.NDArray[np.int_], point: int) -> tuple[npt.NDArray[np.int_], list[tuple[tuple[int], str]]]:
    res = model.predict(image)
    PredictionRepo.create_model_prediction(res, point)
    res_image = res[0]
    boxes = res_image.boxes.xyxy.tolist()
    labels = res_image.boxes.cls.tolist()
    labels_names = [res_image.names[label] for label in labels]
    boxes = [tuple(int(b) for b in box) for box in boxes]
    box_label = [(box, label) for box, label in zip(boxes, labels_names)]
    return image, box_label


def create_interface() -> gr.Blocks:
    points = PointRepo.get_points()
    points_dropdown = [(point.name, point.id) for point in points]
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                loaded_image = gr.Image(type="numpy", label="Input Image", show_download_button=False)
                point = gr.Dropdown(choices=points_dropdown)
            predicted_image = gr.AnnotatedImage(label="Output Image")
        with gr.Row():
            submit = gr.Button(value="Submit photo", variant="primary")
            clear = gr.ClearButton(value="Clear photo", components=[loaded_image, predicted_image])  # noqa: F841
        map = gr.Plot()
        demo.load(filter_map, [], map)
        submit.click(process_image, [loaded_image, point], predicted_image)
    return demo
