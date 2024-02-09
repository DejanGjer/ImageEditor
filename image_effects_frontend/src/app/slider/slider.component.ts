

import { Component, Input, OnInit } from '@angular/core';
import { ImageEditorService } from '../services/image-editor.service';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.css']
})

export class SliderComponent implements OnInit{
  @Input() label: string = '';
  @Input() value: number = 0;
  @Input() min: number = 0;
  @Input() max: number = 100;

  constructor(private imageEditorService: ImageEditorService) {}

  ngOnInit(): void {
    this.onSliderChange({target: {valueAsNumber: this.value}});
  }

  onSliderChange(event: any): void {
    const newValue = event.target.valueAsNumber;
    this.value = newValue;
    this.imageEditorService.adjustImage(this.label, newValue).subscribe({
      next: (data) => {
        const reader = new FileReader();
        reader.onloadend = () => {
          console.log("Image data received from backend");
          console.log(reader.result);
          const imageData = reader.result as string;
          this.imageEditorService.setImageData(imageData);
          // this.imageData = reader.result;
        };
        reader.readAsDataURL(new Blob([data]));
        this.imageEditorService.updateHistogram().subscribe({
          next: (data) => {
            console.log("Histogram data received from backend");
            // console.log(data);
            this.imageEditorService.setHistogramData(data);
          },
          error: (error) => {
            console.error('Error updating histogram:', error);
          }
        });
      },
      error: (error) => {
        console.error('Error uploading image:', error);
      }
    });
  }
}
