import kfp
from kfp import components

chicago_taxi_dataset_op = components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/e3337b8bdcd63636934954e592d4b32c95b49129/components/datasets/Chicago%20Taxi/component.yaml')

@kfp.dsl.pipeline(name='test-pipeline')
def test_pipeline():
    training_data_csv = chicago_taxi_dataset_op(
        where='trip_start_timestamp >= "2019-01-01" AND trip_start_timestamp < "2019-02-01"',
        select='tips,trip_seconds,trip_miles,pickup_community_area,dropoff_community_area,fare,tolls,extras,trip_total',
        limit=10000,
    ).output
    
if __name__ == '__main__':
    kfp_endpoint=None
    kfp.compiler.Compiler().compile(test_pipeline, 'testPipeline.yaml')
