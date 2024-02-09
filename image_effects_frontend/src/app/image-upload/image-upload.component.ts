// image-upload.component.ts

import { Component } from '@angular/core';
import { ImageEditorService } from '../services/image-editor.service';

@Component({
  selector: 'app-image-upload',
  templateUrl: './image-upload.component.html',
  styleUrls: ['./image-upload.component.css']
})
export class ImageUploadComponent {
  constructor(private imageEditorService: ImageEditorService) {}

  onFileChange(event: any): void {
    const file: File = event.target.files[0];
    // this.imageEditorService.uploadImage(file);
  }
}
