from kfp.components import InputPath, OutputPath, create_component_from_func

def data_quality_report(
    cur_path: InputPath('CSV'),
    output_path: OutputPath('HTML'),
) -> None:

    import pandas as pd
    from evidently.metric_preset import DataQualityPreset
    from evidently.report import Report
    from pathlib import Path
    
    df = pd.read_csv(cur_path)

    report = Report(metrics=[
        DataQualityPreset()
    ])
    
    report.run(current_data=df, reference_data=None, column_mapping=None)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    report.save_html(output_path)
    

if __name__ == '__main__':
    data_quality_report_op = create_component_from_func(
        data_quality_report,
        output_component_file='component.yaml',
        base_image='quay.io/ibm/kubeflow-notebook-image-ppc64le:latest',
        packages_to_install=[
            'evidently==0.2.0',
        ],
        annotations={
            'author': 'Evidently AI'
        }
    )    
    
    