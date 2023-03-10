import kfp
from kfp import components
import os

TESTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TESTS)


chicago_taxi_dataset_op = components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/e3337b8bdcd63636934954e592d4b32c95b49129/components/datasets/Chicago%20Taxi/component.yaml')
convert_csv_to_apache_parquet_op = components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/0d7d6f41c92bdc05c2825232afe2b47e5cb6c4b3/components/_converters/ApacheParquet/from_CSV/component.yaml')
xgboost_train_on_csv_op = components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/567c04c51ff00a1ee525b3458425b17adbe3df61/components/XGBoost/Train/component.yaml')
xgboost_predict_on_csv_op = components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/31939086d66d633732f75300ce69eb60e9fb0269/components/XGBoost/Predict/component.yaml')
xgboost_train_on_parquet_op = components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/0ae2f30ff24beeef1c64cc7c434f1f652c065192/components/XGBoost/Train/from_ApacheParquet/component.yaml')
xgboost_predict_on_parquet_op = components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/31939086d66d633732f75300ce69eb60e9fb0269/components/XGBoost/Predict/from_ApacheParquet/component.yaml')
data_quality_report_op = components.load_component_from_file(os.path.join(ROOT, 'component.yaml'))

@kfp.dsl.pipeline(name='xgboost')
def xgboost_pipeline():
    training_data_csv = chicago_taxi_dataset_op(
        where='trip_start_timestamp >= "2019-01-01" AND trip_start_timestamp < "2019-02-01"',
        select='tips,trip_seconds,trip_miles,pickup_community_area,dropoff_community_area,fare,tolls,extras,trip_total',
        limit=10000,
    ).output
    
    # # generate data quality report
    # data_quality_report_op(
    #     cur_data=training_data_csv
    # )

    # Training and prediction on dataset in CSV format
    model_trained_on_csv = xgboost_train_on_csv_op(
        training_data=training_data_csv,
        label_column=0,
        objective='reg:squarederror',
        num_iterations=200,
    ).outputs['model']

    xgboost_predict_on_csv_op(
        data=training_data_csv,
        model=model_trained_on_csv,
        label_column=0,
    )

    # # Training and prediction on dataset in Apache Parquet format
    # training_data_parquet = convert_csv_to_apache_parquet_op(
    #     training_data_csv
    # ).output

    # model_trained_on_parquet = xgboost_train_on_parquet_op(
    #     training_data=training_data_parquet,
    #     label_column_name='tips',
    #     objective='reg:squarederror',
    #     num_iterations=200,
    # ).outputs['model']

    # xgboost_predict_on_parquet_op(
    #     data=training_data_parquet,
    #     model=model_trained_on_parquet,
    #     label_column_name='tips',
    # )

    # # Checking cross-format predictions
    # xgboost_predict_on_parquet_op(
    #     data=training_data_parquet,
    #     model=model_trained_on_csv,
    #     label_column_name='tips',
    # )

    # xgboost_predict_on_csv_op(
    #     data=training_data_csv,
    #     model=model_trained_on_parquet,
    #     label_column=0,
    # )


if __name__ == '__main__':
    kfp_endpoint=None
    # kfp.Client(host=kfp_endpoint).create_run_from_pipeline_func(xgboost_pipeline, arguments={})
    kfp.compiler.Compiler().compile(xgboost_pipeline, __file__ + '.yaml')