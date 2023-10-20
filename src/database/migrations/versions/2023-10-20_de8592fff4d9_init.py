"""init

Revision ID: de8592fff4d9
Revises:
Create Date: 2023-10-20 15:11:11.480982

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "de8592fff4d9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "model_prediction_class",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_model_prediction_class_id"), "model_prediction_class", ["id"], unique=False)
    op.create_table(
        "point",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_point_id"), "point", ["id"], unique=False)
    op.create_table(
        "picture",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("image", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("point_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["point_id"],
            ["point.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_picture_id"), "picture", ["id"], unique=False)
    op.create_table(
        "prediction",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("picture_id", sa.Integer(), nullable=False),
        sa.Column("prediction_class_id", sa.Integer(), nullable=False),
        sa.Column("probability", sa.Float(), nullable=False),
        sa.Column("box_x1", sa.Float(), nullable=False),
        sa.Column("box_y1", sa.Float(), nullable=False),
        sa.Column("box_x2", sa.Float(), nullable=False),
        sa.Column("box_y2", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["picture_id"],
            ["picture.id"],
        ),
        sa.ForeignKeyConstraint(
            ["prediction_class_id"],
            ["model_prediction_class.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_prediction_id"), "prediction", ["id"], unique=False)
    op.create_index(op.f("ix_prediction_picture_id"), "prediction", ["picture_id"], unique=False)
    op.create_index(op.f("ix_prediction_prediction_class_id"), "prediction", ["prediction_class_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_prediction_prediction_class_id"), table_name="prediction")
    op.drop_index(op.f("ix_prediction_picture_id"), table_name="prediction")
    op.drop_index(op.f("ix_prediction_id"), table_name="prediction")
    op.drop_table("prediction")
    op.drop_index(op.f("ix_picture_id"), table_name="picture")
    op.drop_table("picture")
    op.drop_index(op.f("ix_point_id"), table_name="point")
    op.drop_table("point")
    op.drop_index(op.f("ix_model_prediction_class_id"), table_name="model_prediction_class")
    op.drop_table("model_prediction_class")
    # ### end Alembic commands ###
