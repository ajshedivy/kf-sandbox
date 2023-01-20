from kfp.components import InputPath, OutputPath, create_component_from_func

def download_data(
    dataset: InputPath('String'),
    output: OutputPath('CSV')
) -> None:
    
    from sklearn.datasets import load_iris, load_breast_cancer, load_diabetes, load_wine
    from pathlib import Path
    
    DATASETS = {
        'load_iris': load_iris,
        'load_breast_cancer': load_breast_cancer,
        'load_diabetes': load_diabetes,
        'load_wine': load_wine
    }
    
    data = DATASETS[dataset](as_frame=True)
    
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    data.frame.to_csv(output, index=False)
    
if __name__ == '__main__':
    create_component_from_func(
        download_data,
        output_component_file='download_data_component.yaml',
        base_image='python:3.7',
        packages_to_install=[
            'scikit-learn==0.24.2',
            'pandas==1.3.3'
        ],
        annotations={
            'author': 'Evidently AI'
        }
    )
    
        