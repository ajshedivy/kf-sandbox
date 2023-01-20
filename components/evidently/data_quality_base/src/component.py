import argparse
from pathlib import Path
from typing import Any, Dict, Optional, Union, List
import json 

import evidently
import pandas as pd
from evidently.metric_preset import DataQualityPreset
from evidently.report import Report

DEFAULT_PRESETS = {
    'data_quality': DataQualityPreset
}

class PresetConfig(object):
    
    def __init__(self, preset: Union[Any, str] = None,
            output: Path = None, 
            reference_data: Union[str, Path] = None,
            current_data: Union[str, Path] = None,
            column_mapping: Optional[evidently.pipeline.column_mapping.ColumnMapping] = None, 
            op_params: Optional[Dict[str, Any]] = None) -> None:
        self.preset = DEFAULT_PRESETS[preset]()
        self.output = output
        self.ref_data = reference_data
        self.cur_data = current_data
        self.column_mapping = column_mapping
        self.op_params = op_params
        
    def get_preset(self) -> Any:
        return self.preset
        
    def run_report(self) -> Report:
        report = Report(metrics=[
            self.preset
        ])
        
        ref_data_df = None
        if self.ref_data:
            ref_data_df = pd.read_csv(self.ref_data)
        cur_data_df = pd.read_csv(self.cur_data)
        
        report.run(current_data=cur_data_df, reference_data=ref_data_df, column_mapping=self.column_mapping)
        self._report = report
        return report
    
    def save_report(self) -> None:
        if not self._report:
            raise ValueError('Report not run yet')
        self._report.save_html(self.output)
        
    def __str__(self) -> str:
        return f'PresetConfig(preset={self.preset}, output={self.output}, ref_data={self.ref_data}, cur_data={self.cur_data}, column_mapping={self.column_mapping}, op_params={self.op_params})'
    

def create_data_quality_report(
    output_path: Path, 
    cur_data: pd.DataFrame | List[Any | str] | Any, 
    ref_data: Optional[Path] = None, 
    column_mapping = None
 ) -> None:
    
    # df = pd.read_csv(cur_data)
    with open(cur_data, 'r') as f:
        data = json.load(f)
    
    data = json.loads(data)
    
    x_train = data['x_train']
    y_train = data['y_train']
    x_test = data['x_test']
    y_test = data['y_test']
    
    ref_df = None
    if ref_data:
        ref_df = pd.read_csv(ref_data)
        
    report = Report(metrics=[
        DataQualityPreset()
    ])

    report.run(current_data=x_train, reference_data=ref_df, column_mapping=column_mapping)
    
    report.save_html(output_path)
        
        
def main():
    
    parser = argparse.ArgumentParser(description='Evidently Presets for kubeflow')
    parser.add_argument('--output', type=str, default='report.html', help='Output file')
    parser.add_argument('--cur_data', type=pd.DataFrame, default=None, help='Current data')  
    parser.add_argument('--ref_data', type=str, default=None, help='Reference data')
    
    args = parser.parse_args()
    
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    
    create_data_quality_report(
        cur_data=args.cur_data
    )
    
    # report = PresetConfig(
    #     preset=args.preset,
    #     output=args.output,
    #     current_data=args.cur_data,
    #     reference_data=args.ref_data, 
    #     column_mapping=args.column_mapping,
    #     op_params=args.op_params
    # )
    
    # print(report)           
    
    # report.run_report()
    # report.save_report() 
    
if __name__ == '__main__':
    main()
    
    
    
    
    
        
        
        
                

                
                
        