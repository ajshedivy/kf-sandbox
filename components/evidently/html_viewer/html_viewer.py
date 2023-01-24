from kfp.components import InputPath, OutputPath, create_component_from_func

def view_html(
    html_path: InputPath('HTML'),
    mlpipeline_ui_metadata_path: OutputPath(),
) -> None:

    import os
    import json

    html = os.path.abspath(html_path)
    html_content = open(html, 'r').read()
    
    
    metadata = {
        'outputs' : [{
        'type': 'web-app',
        'storage': 'inline',
        'source': html_content,
        }, {
        'type': 'web-app',
        'storage': 'inline',
        'source': '<h1>Hello, World!</h1>',
        }]
    }
    
    with open(mlpipeline_ui_metadata_path, 'w') as f:
        json.dump(metadata, f)
    
    

if __name__ == '__main__':
    data_quality_report_op = create_component_from_func(
        view_html,
        output_component_file='view_html_component.yaml',
        base_image='quay.io/ibm/kubeflow-notebook-image-ppc64le:latest',
        annotations={
            'author': 'Evidently AI'
        }
    )   