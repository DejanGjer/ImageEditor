import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ImageEditorService {
  private apiUrl = 'http://localhost:8000/api/';
  private imageDataSubject: BehaviorSubject<string | null> = new BehaviorSubject<string | null>(null);
  private histogramDataSubject: BehaviorSubject<{ histogram_data: Array<number> } | null> = new BehaviorSubject<{ histogram_data: Array<number> } | null>(null);

  constructor(private http: HttpClient) {}

  getOriginalImage(): Observable<Blob> {
    // Adjust the URL and payload based on your backend API
    console.log("GET REQUEST FOR ORIGINAL IMAGE")
    const url = `${this.apiUrl}adjust-image/`;
    return this.http.get(url, { responseType: 'blob' });
  }

  adjustImage(effect_name: string, value: number): Observable<Blob> {
    // Adjust the URL and payload based on your backend API
    const url = `${this.apiUrl}adjust-image/`;
    console.log("Send post request to " + url);
    const payload = { [effect_name]: value };
    console.log(payload);

    return this.http.post(url, payload, {withCredentials: true, responseType: 'blob'});
  }

  updateHistogram(): Observable<{ histogram_data: Array<number> }> {
    // Adjust the URL and payload based on your backend API
    const url = `${this.apiUrl}histogram-data/`;
    return this.http.get<{ histogram_data: Array<number> }>(url);
  }

  // uploadImage(file: File): Observable<any> {
  //   // Adjust the URL and payload based on your backend API
  //   const url = `${this.apiUrl}upload-image`;
  //   const formData = new FormData();
  //   formData.append('image', file);
  //   console.log(file);
  //   return this.http.post(url, formData);
  // }



  setImageData(imageData: string | null): void {
    this.imageDataSubject.next(imageData);
  }

  getImageData(): Observable<string | null> {
    return this.imageDataSubject.asObservable();
  }

  setHistogramData(histogramData: { histogram_data: Array<number> } | null): void {
    this.histogramDataSubject.next(histogramData);
  }

  getHistogramData(): Observable<{ histogram_data: Array<number> } | null> {
    return this.histogramDataSubject.asObservable();
  }
}
