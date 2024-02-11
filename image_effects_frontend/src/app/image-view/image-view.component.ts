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
    // this.imageEditorService.getAdjustedImage().pipe(takeUntil(timer(300))).subscribe({
    //   next: (data) => {
    //     const reader = new FileReader();
    //     reader.onloadend = () => {
    //       // console.log("Image data received from backend");
    //       // console.log(reader.result);
    //       const imageData = reader.result as string;
    //       this.imageEditorService.setImageData(imageData);
    //       // this.imageData = reader.result;
    //     };
    //     reader.readAsDataURL(new Blob([data]));
    //     this.imageEditorService.updateHistogram().subscribe({
    //       next: (data) => {
    //         console.log("Histogram data received from backend");
    //         // console.log(data);
    //         this.imageEditorService.setHistogramData(data);
    //       },
    //       error: (error) => {
    //         console.error('Error updating histogram:', error);
    //       }
    //     });
    //   },
    //   error: (error) => {
    //     console.error('Error uploading image:', error);
    //   }
    // });
    if (!this.original) {
      this.imageEditorService.getImageData().subscribe(
        imageData => {
          this.imageData = imageData;
        }
      );
    } 
      // this.imageEditorService.getImageData().pipe(takeUntil(timer(1000))).subscribe(
      //   imageData => {
      //     this.imageData = imageData;
      //   },
      // );

    this.imageEditorService.getOriginalImage().pipe(takeUntil(timer(500))).subscribe({
      next: (data) => {
        console.log("PROCESSING ORIGINAL IMAGE")
        const reader = new FileReader();
        reader.onloadend = () => {
          // console.log("Image data received from backend");
          // console.log(reader.result);
          // const imageData = reader.result.toString() as string;
          // this.imageEditorService.setImageData(imageData);
          if (reader.result != null) {
            this.imageData = reader.result.toString() as string;
            // console.log("Oroginal image data received from backend");
            // console.log(this.imageData);
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

  // convertToDataUrl(arrayBuffer: ArrayBuffer): string {
  //   const binary = String.fromCharCode(...new Uint8Array(arrayBuffer));
  //   return 'data:image/jpeg;base64,' + btoa(binary);
  // }
}
