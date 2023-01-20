from kfp.components import InputPath, OutputPath, create_component_from_func

def data_quality_report(
    output_path: OutputPath('HTML'),
    cur_data: InputPath('CSV'),
    ref_data: InputPath('CSV') = None,
    column_mapping = None,
) -> None:

    import pandas as pd
    from evidently.metric_preset import DataQualityPreset
    from evidently.report import Report
    
    df = pd.read_csv(cur_data)
    
    ref_df = None
    if ref_data:
        ref_df = pd.read_csv(ref_data)

    report = Report(metrics=[
        DataQualityPreset()
    ])
    
    report.run(current_data=df, reference_data=ref_df, column_mapping=column_mapping)
    
    report.save_html(output_path)
    

if __name__ == '__main__':
    data_quality_report_op = create_component_from_func(
        data_quality_report,
        output_component_file='component.yaml',
        base_image='python:3.10.8',
        packages_to_install=['evidently', 'pandas'],
        annotations={
            'author': 'Evidently AI'
        }
    )    
    
    