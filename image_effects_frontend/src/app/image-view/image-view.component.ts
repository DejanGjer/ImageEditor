import { Component, Input, OnInit } from '@angular/core';
import { ImageEditorService } from '../services/image-editor.service';
import { take, takeUntil } from 'rxjs/operators';  // Import the take operator
import { Subject, timer } from 'rxjs';


@Component({
  selector: 'app-image-view',
  templateUrl: './image-view.component.html',
  styleUrls: ['./image-view.component.css']
})
export class ImageViewComponent implements OnInit{
  @Input() original: boolean = false;
  @Input() title: string = '';
  imageData: string | null = null;

  constructor(private imageEditorService: ImageEditorService) {}

  ngOnInit(): void {
    if (!this.original) {
      this.imageEditorService.getImageData().subscribe(
        imageData => {
          this.imageData = imageData;
        }
      );
    } 
  
    this.imageEditorService.getOriginalImage().pipe(takeUntil(timer(500))).subscribe({
      next: (data) => {
        console.log("PROCESSING ORIGINAL IMAGE")
        const reader = new FileReader();
        reader.onloadend = () => {
          if (reader.result != null) {
            this.imageData = reader.result.toString() as string;
          }
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
